"""
chatbot_service.py — Production-Grade AI Agent with Dynamic DB Access

Architecture:
  1. LLM Reasoning    → Groq (llama-3.3-70b-versatile)
  2. Tool Execution   → OpenAI-compatible function calling + inline fallback
  3. Database Engine   → Generic SQLAlchemy query builder from JSON spec
  4. Memory System     → Per-session short-term memory (last 10 turns)
  5. Intent Detection  → Regex-based fast-path for greetings, help, frustration
  6. Response Engine   → Clean, structured, no-markdown output
  7. Security          → Role-based row filtering, column blacklisting, input sanitization
  8. Anti-Hallucination→ All data MUST come from DB tool; never fabricated
  9. Caching           → LRU hash cache for repeated anonymous queries
  10. Error Handling   → Safe fallback on every failure path
"""

import os
import re
import json
import hashlib
import logging
from datetime import datetime, timezone, timedelta
from collections import OrderedDict

from groq import Groq

from app.extensions import db
from app.models.event import Event
from app.models.user import User
from app.models.registration import Registration
from app.models.payment import Payment
from app.models.escalation import EscalationTicket

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
#  1. DATABASE SCHEMA  (injected into system prompt for full AI awareness)
# ═══════════════════════════════════════════════════════════════════════════════

DATABASE_SCHEMA = """
TABLE: users
  Columns: id (PK int), name (str), email (str unique), password_hash (str HIDDEN),
           role (str: "user"|"organizer"|"admin"), city (str), budget_preference (str: "cheap"|"mid"|"premium"),
           preferred_sports (JSON array), referral_code (str unique),
           referred_by_id (FK -> users.id, nullable), created_at (datetime)

TABLE: events
  Columns: id (PK int), title (str), sport_category (str), description (text),
           venue_city (str), venue_address (str), event_date (datetime),
           capacity (int), price (float), price_tier (str: "cheap"|"mid"|"premium"),
           organizer_id (FK -> users.id), tags (JSON array), banner_url (str),
           is_active (bool), is_featured (bool), created_at (datetime)
  Computed properties (not direct columns, calculate via registrations):
    seats_sold = COUNT of confirmed registrations for this event
    seats_remaining = capacity - seats_sold
    fill_rate = (seats_sold / capacity) * 100
    revenue = seats_sold * price
    performance_label = LOW (<30% fill) | MEDIUM (30-70%) | HIGH (>70%)

TABLE: registrations
  Columns: id (PK int), user_id (FK -> users.id), event_id (FK -> events.id),
           status (str: "pending"|"confirmed"|"cancelled"), role (str default "athlete"),
           role_details (JSON), created_at (datetime)
  Constraint: UNIQUE(user_id, event_id)

TABLE: payments
  Columns: id (PK int), registration_id (FK -> registrations.id unique),
           razorpay_order_id (str), razorpay_payment_id (str),
           razorpay_signature (str HIDDEN), amount (float), platform_fee (float),
           organizer_payout (float), status (str: "created"|"captured"|"failed"),
           created_at (datetime)

TABLE: escalation_tickets
  Columns: id (PK int), user_id (FK -> users.id nullable),
           user_query (text), session_context (text),
           is_resolved (bool), created_at (datetime)

RELATIONSHIPS:
  users.id  <-> events.organizer_id       (one organizer -> many events)
  users.id  <-> registrations.user_id     (one user -> many registrations)
  events.id <-> registrations.event_id    (one event -> many registrations)
  registrations.id <-> payments.registration_id  (one-to-one)
  users.id  <-> users.referred_by_id      (self-referential referral chain)
  users.id  <-> escalation_tickets.user_id

NATURAL LANGUAGE MAPPINGS:
  "cheap"       -> price_tier = "cheap" OR price < 500
  "expensive"   -> price_tier = "premium" OR price > 2000
  "popular"     -> ORDER BY seats_sold DESC (join registrations, count confirmed)
  "recent"      -> created_at >= last 7 days
  "upcoming"    -> event_date >= now
  "past"        -> event_date < now
  "revenue"     -> SUM(payments.amount) or seats_sold * price
  "how many"    -> COUNT aggregation
  "total"       -> SUM aggregation
  "average"     -> AVG aggregation
  "highest"     -> MAX or ORDER DESC LIMIT 1
  "lowest"      -> MIN or ORDER ASC LIMIT 1
  "top N"       -> ORDER DESC LIMIT N
"""


# ═══════════════════════════════════════════════════════════════════════════════
#  2. SYSTEM PROMPT
# ═══════════════════════════════════════════════════════════════════════════════

SYSTEM_PROMPT = """You are Sparky, an intelligent AI assistant for LiveSports, a sports event management platform in India.

You are a DATABASE AGENT — not a simple chatbot. You can access live data from the platform database.

YOUR CAPABILITIES:
1. Answer support/FAQ questions from your knowledge
2. Query the live database using the execute_db_query tool for ANY data question
3. Perform analytics: counts, totals, averages, rankings, comparisons
4. Handle follow-up questions using conversation context

""" + DATABASE_SCHEMA + """

HOW TO USE execute_db_query:
Pass a JSON query_spec string with these fields:

{
  "table": "events",
  "columns": ["id", "title", "venue_city"],
  "filters": [{"column": "venue_city", "op": "ilike", "value": "mumbai"}],
  "joins": [{"table": "registrations", "on": ["events.id", "registrations.event_id"]}],
  "aggregations": [{"func": "count", "column": "id", "alias": "total"}],
  "group_by": ["venue_city"],
  "order_by": [{"column": "total", "dir": "desc"}],
  "limit": 10
}

All fields except "table" are optional.
Filter operators: =, !=, <, >, <=, >=, ilike, like, in, not_in, is_null, is_not_null, between
Date values: use ISO format (2026-01-15) or relative words (today, yesterday, last_week, last_month, last_year)

CRITICAL RULES:
1. For ANY question about data (events, users, registrations, revenue, counts) -> ALWAYS use execute_db_query. NEVER guess.
2. For greetings -> respond warmly, ask how you can help.
3. For FAQ/support -> answer from your knowledge.
4. You can call the tool MULTIPLE TIMES in one turn for complex queries.
5. When user says "my" -> use their user_id from context. If no context, ask them to log in.
6. Follow-up questions: use conversation history to understand what "it", "those", "them", "only cheap ones" etc. refer to.
7. If no results -> say "No results found" clearly. Do not invent data.
8. If query seems invalid -> ask the user to clarify.

RESPONSE FORMAT:
- Short, clean answers. 2-4 sentences max.
- No markdown. No bullet points. No asterisks. No headers.
- Show key numbers clearly: "Total revenue: Rs.12,500" or "5 events found in Mumbai"
- For lists, use commas or numbered format in plain text.
- Never expose internal reasoning, tool names, or JSON to the user.

ROLE-BASED ACCESS (enforced by backend, but be aware):
- Users can only see their own registrations/payments and public events
- Organizers can see their own events and registrations for those events
- Admins have full access
- Anonymous users can only see public active events
"""


# ═══════════════════════════════════════════════════════════════════════════════
#  3. MODEL REGISTRY + SECURITY CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

MODEL_MAP = {
    "users":              User,
    "events":             Event,
    "registrations":      Registration,
    "payments":           Payment,
    "escalation_tickets": EscalationTicket,
}

BLACKLISTED_COLUMNS = {
    "users":    {"password_hash"},
    "payments": {"razorpay_signature"},
}

ROLE_TABLE_ACCESS = {
    "admin":     {"users", "events", "registrations", "payments", "escalation_tickets"},
    "organizer": {"users", "events", "registrations", "payments"},
    "user":      {"users", "events", "registrations", "payments"},
    "anonymous": {"events"},
}


# ═══════════════════════════════════════════════════════════════════════════════
#  4. DYNAMIC QUERY ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

def _resolve_column(col_name, primary_model):
    """Resolve a column reference like 'events.title' or 'title' to a SQLAlchemy column."""
    if "." in col_name:
        tbl, cn = col_name.split(".", 1)
        m = MODEL_MAP.get(tbl, primary_model)
    else:
        m = primary_model
        cn = col_name
    attr = getattr(m, cn, None)
    return attr


def _parse_date(val):
    """Parse date string or relative keyword into datetime."""
    if isinstance(val, datetime):
        return val
    if not isinstance(val, str):
        return val

    now = datetime.now(timezone.utc)
    mapping = {
        "today":      now.replace(hour=0, minute=0, second=0, microsecond=0),
        "now":        now,
        "yesterday":  (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0),
        "last_week":  now - timedelta(weeks=1),
        "last week":  now - timedelta(weeks=1),
        "last_month": now - timedelta(days=30),
        "last month": now - timedelta(days=30),
        "last_year":  now - timedelta(days=365),
        "last year":  now - timedelta(days=365),
        "this_week":  now - timedelta(days=now.weekday()),
        "this week":  now - timedelta(days=now.weekday()),
    }
    low = val.lower().strip()
    if low in mapping:
        return mapping[low]

    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ",
                "%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(val, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return val


def _apply_single_filter(query, model, f):
    """Apply one filter clause to a SQLAlchemy query."""
    col = _resolve_column(f.get("column", ""), model)
    if col is None:
        return query

    op    = f.get("op", "=").lower().strip()
    value = f.get("value")

    # Auto-parse dates for date columns
    col_name = f.get("column", "").split(".")[-1]
    if col_name in ("event_date", "created_at") and value is not None:
        if isinstance(value, list):
            value = [_parse_date(v) for v in value]
        else:
            value = _parse_date(value)

    ops = {
        "=":           lambda c, v: c == v,
        "==":          lambda c, v: c == v,
        "!=":          lambda c, v: c != v,
        "<":           lambda c, v: c < v,
        ">":           lambda c, v: c > v,
        "<=":          lambda c, v: c <= v,
        ">=":          lambda c, v: c >= v,
        "ilike":       lambda c, v: c.ilike("%" + str(v) + "%"),
        "like":        lambda c, v: c.like("%" + str(v) + "%"),
        "in":          lambda c, v: c.in_(v if isinstance(v, list) else [v]),
        "not_in":      lambda c, v: ~c.in_(v if isinstance(v, list) else [v]),
        "is_null":     lambda c, v: c.is_(None),
        "is_not_null": lambda c, v: c.isnot(None),
        "between":     lambda c, v: c.between(v[0], v[1]) if isinstance(v, list) and len(v) == 2 else c == v,
    }

    fn = ops.get(op)
    if fn:
        try:
            query = query.filter(fn(col, value))
        except Exception as e:
            logger.warning(f"[QueryEngine] Filter failed: {f} -> {e}")
    return query


def _serialize(val):
    """Make any value JSON-safe."""
    if isinstance(val, datetime):
        return val.strftime("%d %b %Y, %I:%M %p")
    if isinstance(val, (int, float, str, bool)):
        return val
    if val is None:
        return None
    return str(val)


def execute_db_query(query_spec_json, caller_role="anonymous", caller_id=None):
    """
    Dynamic database query engine.
    Converts a JSON spec into a SQLAlchemy query, applies role-based security,
    executes, and returns structured results.
    """
    try:
        spec = json.loads(query_spec_json) if isinstance(query_spec_json, str) else query_spec_json

        table_name   = spec.get("table", "").strip().lower()
        columns      = spec.get("columns", [])
        filters      = spec.get("filters", [])
        joins        = spec.get("joins", [])
        aggregations = spec.get("aggregations", [])
        group_by     = spec.get("group_by", [])
        order_by     = spec.get("order_by", [])
        limit        = min(int(spec.get("limit", 25)), 50)

        # ── Validate table ────────────────────────────────────────────
        if table_name not in MODEL_MAP:
            available = ", ".join(MODEL_MAP.keys())
            return {"error": "Unknown table '{}'. Available tables: {}".format(table_name, available)}

        model = MODEL_MAP[table_name]
        blacklisted = BLACKLISTED_COLUMNS.get(table_name, set())

        # ── Role-based table access ───────────────────────────────────
        allowed = ROLE_TABLE_ACCESS.get(caller_role, ROLE_TABLE_ACCESS["anonymous"])
        if table_name not in allowed:
            return {"error": "Access denied. Your role ({}) cannot access '{}'.".format(caller_role, table_name)}

        # ── Build query ───────────────────────────────────────────────
        if aggregations:
            select_parts = []

            # Group-by columns first
            for gb in group_by:
                gb_col = _resolve_column(gb, model)
                if gb_col is not None:
                    select_parts.append(gb_col)

            # Aggregation expressions
            for agg in aggregations:
                func_name = agg.get("func", "count").lower()
                col_ref   = agg.get("column", "id")
                alias     = agg.get("alias", "{}_{}".format(func_name, col_ref))

                col = _resolve_column(col_ref, model)
                if col is None:
                    continue

                agg_map = {
                    "count": db.func.count,
                    "sum":   db.func.sum,
                    "avg":   db.func.avg,
                    "min":   db.func.min,
                    "max":   db.func.max,
                }
                fn = agg_map.get(func_name, db.func.count)
                select_parts.append(fn(col).label(alias))

            if not select_parts:
                return {"error": "No valid columns/aggregations found."}
            query = db.session.query(*select_parts)

        elif columns:
            safe = [c for c in columns if c not in blacklisted and hasattr(model, c)]
            if not safe:
                safe = [c.name for c in model.__table__.columns if c.name not in blacklisted]
            query = db.session.query(*[getattr(model, c) for c in safe])
        else:
            query = db.session.query(model)

        # ── Joins ─────────────────────────────────────────────────────
        joined_models = set()
        for j in joins:
            jt = j.get("table", "")
            jm = MODEL_MAP.get(jt)
            if not jm or jt in joined_models:
                continue
            on_pair = j.get("on", [])
            if len(on_pair) == 2:
                left  = _resolve_column(on_pair[0], model)
                right = _resolve_column(on_pair[1], jm)
                if left is not None and right is not None:
                    query = query.join(jm, left == right, isouter=j.get("outer", False))
                    joined_models.add(jt)
                    continue
            query = query.join(jm)
            joined_models.add(jt)

        # ── Row-level security ────────────────────────────────────────
        if caller_role == "user" and caller_id:
            if table_name == "users":
                query = query.filter(User.id == caller_id)
            elif table_name == "registrations":
                query = query.filter(Registration.user_id == caller_id)
            elif table_name == "payments":
                if "registrations" not in joined_models:
                    query = query.join(Registration, Payment.registration_id == Registration.id)
                    joined_models.add("registrations")
                query = query.filter(Registration.user_id == caller_id)
            elif table_name == "events":
                query = query.filter(Event.is_active == True)

        elif caller_role == "organizer" and caller_id:
            if table_name == "registrations":
                if "events" not in joined_models:
                    query = query.join(Event, Registration.event_id == Event.id)
                    joined_models.add("events")
                query = query.filter(Event.organizer_id == caller_id)
            elif table_name == "payments":
                if "registrations" not in joined_models:
                    query = query.join(Registration, Payment.registration_id == Registration.id)
                    joined_models.add("registrations")
                if "events" not in joined_models:
                    query = query.join(Event, Registration.event_id == Event.id)
                    joined_models.add("events")
                query = query.filter(Event.organizer_id == caller_id)
            elif table_name == "users":
                query = query.filter(User.id == caller_id)

        elif caller_role == "anonymous":
            if table_name == "events":
                query = query.filter(Event.is_active == True)

        # ── User-specified filters ────────────────────────────────────
        for f in filters:
            query = _apply_single_filter(query, model, f)

        # ── Group by ─────────────────────────────────────────────────
        if aggregations and group_by:
            for gb in group_by:
                gb_col = _resolve_column(gb, model)
                if gb_col is not None:
                    query = query.group_by(gb_col)

        # ── Order by ─────────────────────────────────────────────────
        agg_aliases = {a.get("alias", "") for a in aggregations}
        for ob in order_by:
            ob_name = ob.get("column", "")
            ob_dir  = ob.get("dir", "asc").lower()

            if ob_name in agg_aliases:
                direction = "DESC" if ob_dir == "desc" else "ASC"
                query = query.order_by(db.text("{} {}".format(ob_name, direction)))
            else:
                ob_col = _resolve_column(ob_name, model)
                if ob_col is not None:
                    query = query.order_by(ob_col.desc() if ob_dir == "desc" else ob_col.asc())

        # ── Limit + Execute ──────────────────────────────────────────
        query = query.limit(limit)
        results = query.all()

        if not results:
            return {"rows": [], "count": 0, "message": "No results found matching your criteria."}

        # ── Format results ───────────────────────────────────────────
        rows = []
        for row in results:
            if hasattr(row, "to_dict"):
                d = row.to_dict()
                for bl in blacklisted:
                    d.pop(bl, None)
                d.pop("password_hash", None)
                rows.append(d)
            elif hasattr(row, "_asdict"):
                rows.append({k: _serialize(v) for k, v in row._asdict().items()})
            elif hasattr(row, "_fields"):
                rows.append({f: _serialize(getattr(row, f)) for f in row._fields})
            elif isinstance(row, tuple):
                if aggregations:
                    keys = list(group_by) + [a.get("alias", "col_{}".format(i)) for i, a in enumerate(aggregations)]
                elif columns:
                    keys = columns
                else:
                    keys = ["col_{}".format(i) for i in range(len(row))]
                rows.append(dict(zip(keys, [_serialize(v) for v in row])))
            else:
                rows.append({"value": _serialize(row)})

        return {"rows": rows, "count": len(rows)}

    except json.JSONDecodeError as e:
        logger.error("[QueryEngine] JSON error: %s", e)
        return {"error": "Invalid query specification format."}
    except Exception as e:
        logger.error("[QueryEngine] Error: %s", e, exc_info=True)
        return {"error": "Query execution failed: {}".format(str(e))}


# ═══════════════════════════════════════════════════════════════════════════════
#  5. TOOL DEFINITIONS  (sent to Groq for function calling)
# ═══════════════════════════════════════════════════════════════════════════════

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "execute_db_query",
            "description": (
                "Execute a dynamic database query. Use this for ANY data question about events, "
                "users, registrations, payments, or platform stats. You can filter, join, aggregate, "
                "group, sort, and limit. Pass a JSON query_spec string. "
                "Supported tables: users, events, registrations, payments, escalation_tickets. "
                "Supported filter ops: =, !=, <, >, <=, >=, ilike, like, in, not_in, is_null, "
                "is_not_null, between. "
                "Supported aggregations: count, sum, avg, min, max. "
                "Date values: ISO format or relative words (today, yesterday, last_week, last_month). "
                "You can call this tool multiple times for complex multi-step queries."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query_spec": {
                        "type": "string",
                        "description": (
                            "JSON string with: table (required), columns (optional array), "
                            "filters (optional array of {column, op, value}), "
                            "joins (optional array of {table, on: [left_col, right_col]}), "
                            "aggregations (optional array of {func, column, alias}), "
                            "group_by (optional array), order_by (optional array of {column, dir}), "
                            "limit (optional int, max 50)."
                        ),
                    },
                },
                "required": ["query_spec"],
            },
        },
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
#  6. FAQ RAG  (local sentence-transformers + FAISS)
# ═══════════════════════════════════════════════════════════════════════════════

FAQ_ENTRIES = [
    {"t": "Registration",       "a": "To register for an event, go to the event detail page and click 'Register & Pay'. Complete the Razorpay checkout. A confirmation email is sent once payment succeeds."},
    {"t": "Payment Methods",    "a": "LiveSports accepts credit cards, debit cards, UPI, Paytm, PhonePe, Google Pay, and net banking through Razorpay."},
    {"t": "Cancellation",       "a": "To cancel, go to 'My Registrations' in your profile and click Cancel. Refund eligibility depends on the organizer's cancellation policy."},
    {"t": "Refunds",            "a": "Submit a refund request within 48 hours of cancellation. Refunds are processed within 5-7 business days to your original payment method."},
    {"t": "My Registrations",   "a": "Log in and go to 'My Registrations' from the profile dropdown in the top navigation bar to see all your registered events."},
    {"t": "Support",            "a": "Use this chatbot for instant answers. For unresolved issues, our human support team follows up within 24 hours."},
    {"t": "Group Registration", "a": "Each account registers one participant. For groups, each member must create their own account and register individually."},
    {"t": "Event Cancelled",    "a": "If an organizer cancels an event, all registered participants receive a full automatic refund and an email notification."},
    {"t": "Organizer Payouts",  "a": "Razorpay pays out organizers after the event. LiveSports deducts a 15% platform fee before the payout is processed."},
    {"t": "Become Organizer",   "a": "Select the 'Organizer' role when creating your account to create and manage events from your organizer dashboard."},
    {"t": "Event Discovery",    "a": "Search for events by sport, location, or date from the homepage search bar."},
    {"t": "Account & Login",    "a": "Sign up with email/password or Google OAuth. Use 'Forgot Password' on the login page to reset your password."},
    {"t": "Platform Fees",      "a": "LiveSports charges a 15% platform fee on registrations, deducted before organizer payout. The price you see is the final price."},
    {"t": "Referral Credits",   "a": "Earn referral credits by sharing your referral link from your profile. Credits are applied on your next registration."},
]


class FAQRetriever:
    """Offline FAQ search using sentence-transformers + FAISS inner-product index."""

    def __init__(self):
        try:
            import numpy as np
            import faiss
            from sentence_transformers import SentenceTransformer
            self._np = np
            self._faiss = faiss
            self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
            self.texts = ["[{}] {}".format(e["t"], e["a"]) for e in FAQ_ENTRIES]
            vecs = self.encoder.encode(self.texts, convert_to_numpy=True, normalize_embeddings=True)
            self.index = faiss.IndexFlatIP(vecs.shape[1])
            self.index.add(vecs.astype(np.float32))
            self._ready = True
            logger.info("[FAQRetriever] Loaded %d FAQ entries with FAISS index.", len(self.texts))
        except ImportError as e:
            logger.warning("[FAQRetriever] ML dependencies not installed (%s). FAQ retrieval disabled.", e)
            self._ready = False

    def retrieve(self, query, k=3):
        if not self._ready:
            return ""
        vec = self.encoder.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        scores, idxs = self.index.search(vec.astype(self._np.float32), k)
        parts = []
        for score, idx in zip(scores[0], idxs[0]):
            if idx < len(self.texts) and score > 0.25:
                parts.append(self.texts[idx])
        return "\n".join(parts) if parts else ""


# ═══════════════════════════════════════════════════════════════════════════════
#  7. INTENT DETECTION  (fast-path before LLM call)
# ═══════════════════════════════════════════════════════════════════════════════

_RE_GREETING = re.compile(
    r"^\s*(hi+|hello|hey|howdy|yo|sup|good\s*(morning|afternoon|evening|day|night)|"
    r"what'?s\s*up|namaste|hola)\s*[!?.]*\s*$",
    re.I,
)
_RE_THANKS = re.compile(
    r"^\s*(thanks?|thank\s*you|thx|ty|appreciated?|great|awesome|perfect|cool)\s*[!?.]*\s*$",
    re.I,
)
_RE_HELP = re.compile(
    r"^\s*(help|what can you do|options|menu|commands?|features?)\s*[?!.]*\s*$",
    re.I,
)
_RE_FRUSTRATED = re.compile(
    r"\b(angry|frustrated|ridiculous|terrible|worst|useless|stupid|scam|cheated|"
    r"pathetic|horrible|disgusting|outrageous|unacceptable|rip.?off|waste)\b",
    re.I,
)
_RE_URGENT = re.compile(
    r"\b(urgent|asap|immediately|right now|emergency|critical|blocking)\b",
    re.I,
)

GREETING_RESPONSE = "Hey there! I'm Sparky, your LiveSports assistant. I can help you find events, check registrations, view stats, and answer any platform questions. What would you like to know?"

THANKS_RESPONSE = "You're welcome! Let me know if there's anything else I can help with."

HELP_RESPONSE = (
    "I can help you with: finding events by city, sport, or price -- "
    "checking your registrations -- viewing event details and stats -- "
    "revenue and analytics for organizers -- platform-wide statistics for admins -- "
    "and answering any questions about how LiveSports works. Just ask!"
)


def _sanitize(text):
    """Strip control characters and collapse whitespace."""
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", " ", text)
    return " ".join(text.split()).strip()


# ═══════════════════════════════════════════════════════════════════════════════
#  8. MEMORY SYSTEM  (per-session, in-memory, capped at 10 turns)
# ═══════════════════════════════════════════════════════════════════════════════

class SessionMemory:
    """Simple in-memory per-session conversation store."""

    MAX_SESSIONS = 500
    MAX_TURNS    = 10

    def __init__(self):
        self._store = OrderedDict()

    def _session_key(self, user_id):
        return str(user_id) if user_id else "anon"

    def get_history(self, user_id):
        key = self._session_key(user_id)
        return list(self._store.get(key, []))

    def add_turn(self, user_id, role, content):
        key = self._session_key(user_id)
        if key not in self._store:
            if len(self._store) >= self.MAX_SESSIONS:
                self._store.popitem(last=False)
            self._store[key] = []
        self._store[key].append({"role": role, "content": content})
        if len(self._store[key]) > self.MAX_TURNS * 2:
            self._store[key] = self._store[key][-(self.MAX_TURNS * 2):]
        self._store.move_to_end(key)

    def clear(self, user_id):
        key = self._session_key(user_id)
        self._store.pop(key, None)


# ═══════════════════════════════════════════════════════════════════════════════
#  9. RESPONSE CACHE  (LRU for repeated anonymous queries)
# ═══════════════════════════════════════════════════════════════════════════════

class LRUCache:
    """Fixed-size LRU cache using OrderedDict."""

    def __init__(self, max_size=200):
        self._cache = OrderedDict()
        self._max = max_size

    def get(self, key):
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache[key]
        return None

    def set(self, key, value):
        if key in self._cache:
            self._cache.move_to_end(key)
        else:
            if len(self._cache) >= self._max:
                self._cache.popitem(last=False)
        self._cache[key] = value

    @staticmethod
    def hash_key(msg):
        return hashlib.md5(msg.lower().strip().encode()).hexdigest()


# ═══════════════════════════════════════════════════════════════════════════════
#  10. INLINE TOOL CALL PARSER  (fallback when Groq outputs text instead of structured calls)
# ═══════════════════════════════════════════════════════════════════════════════

_INLINE_TOOL_RE = re.compile(r'<function=(\w+)>(.*?)</function>', re.DOTALL)


def _extract_inline_calls(text):
    """Extract inline function calls from LLM text output."""
    matches = _INLINE_TOOL_RE.findall(text)
    clean_text = _INLINE_TOOL_RE.sub("", text).strip()
    return matches, clean_text


# ═══════════════════════════════════════════════════════════════════════════════
#  11. MAIN SERVICE CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class ChatbotService:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY", "")
        self.client = Groq(api_key=api_key) if api_key else None
        if not api_key:
            logger.warning("[ChatbotService] GROQ_API_KEY not set. Escalation-only mode.")

        self.faq    = FAQRetriever()
        self.memory = SessionMemory()
        self.cache  = LRUCache(max_size=200)
        self.model  = "llama-3.3-70b-versatile"

    # ─── PUBLIC ENTRY POINT ───────────────────────────────────────────────
    def get_response(self, user_message, context=None, chat_history=None):
        """
        Process a user message and return {"response": str, "escalated": bool}.

        Args:
            user_message: raw user text
            context: "user_id:5,role:organizer,name:John" or None
            chat_history: [{"role": "user"|"bot", "content": "..."}] from frontend
        """
        if not self.client:
            return self._escalate(user_message, context)

        msg = _sanitize(user_message)
        if not msg:
            return {"response": "I didn't catch that. Could you rephrase?", "escalated": False}

        caller_role, caller_id, caller_name = self._parse_context(context)

        # ── Intent Detection (fast paths) ─────────────────────────────
        if _RE_GREETING.match(msg):
            self.memory.add_turn(caller_id, "user", msg)
            self.memory.add_turn(caller_id, "assistant", GREETING_RESPONSE)
            return {"response": GREETING_RESPONSE, "escalated": False}

        if _RE_THANKS.match(msg):
            return {"response": THANKS_RESPONSE, "escalated": False}

        if _RE_HELP.match(msg):
            return {"response": HELP_RESPONSE, "escalated": False}

        if _RE_FRUSTRATED.search(msg) and _RE_URGENT.search(msg):
            return self._escalate(msg, context, priority="high")

        # ── Cache check (anonymous, no history) ───────────────────────
        cache_key = self.cache.hash_key(msg)
        if not context and not chat_history:
            cached = self.cache.get(cache_key)
            if cached:
                return cached

        # ── Build conversation messages ───────────────────────────────
        faq_context = self.faq.retrieve(msg)
        system_body = SYSTEM_PROMPT
        if faq_context:
            system_body += "\n\nFAQ Knowledge (for support questions):\n" + faq_context
        if context:
            system_body += "\n\nCurrent user: " + context

        messages = [{"role": "system", "content": system_body}]

        # Merge memory + incoming history (prefer incoming, fallback to memory)
        history_turns = chat_history if chat_history else self.memory.get_history(caller_id)
        for turn in (history_turns or [])[-10:]:
            role = turn.get("role", "user")
            if role == "bot":
                role = "assistant"
            elif role not in ("user", "assistant", "system"):
                role = "user"
            messages.append({"role": role, "content": turn.get("content", "")})

        # Add current message with intent annotations
        enriched = msg
        if _RE_FRUSTRATED.search(msg):
            enriched = "[User seems frustrated] " + enriched
        if _RE_URGENT.search(msg):
            enriched = "[Urgent] " + enriched
        messages.append({"role": "user", "content": enriched})

        # ── LLM Call with Tool Use ────────────────────────────────────
        try:
            answer = self._run_agent(messages, caller_role, caller_id)
        except Exception as ex:
            logger.error("[ChatbotService] Agent error: %s", ex, exc_info=True)
            answer = "I'm having a technical issue right now. Please try again in a moment."

        # ── Post-process ──────────────────────────────────────────────
        if "ESCALATE_TO_HUMAN" in answer:
            return self._escalate(msg, context)

        # Save to memory
        self.memory.add_turn(caller_id, "user", msg)
        self.memory.add_turn(caller_id, "assistant", answer)

        result = {"response": answer, "escalated": False}

        # Cache only anonymous, stateless queries
        if not context and not chat_history:
            self.cache.set(cache_key, result)

        return result

    # ─── AGENT EXECUTION (handles structured + inline + error-recovery) ──
    def _run_agent(self, messages, caller_role, caller_id, depth=0):
        """
        Execute the LLM agent loop.
        Supports up to 3 rounds of tool calls for multi-step reasoning.
        Catches Groq BadRequestError when model outputs malformed tool calls.
        """
        if depth > 3:
            return "I ran into complexity limits. Could you simplify your question?"

        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                temperature=0.3,
                max_tokens=1024,
            )
        except Exception as api_err:
            # ── Groq BadRequestError: model sent malformed tool call ───
            # The error body contains `failed_generation` with the raw
            # inline function call, e.g.:
            #   <function=execute_db_query>{"table":"events",...}</function>
            # We extract it, execute the query, and ask for a plain summary.
            err_str = str(api_err)
            if "failed_generation" in err_str or "tool_use_failed" in err_str:
                logger.warning("[Agent] Groq tool-call validation failed. Recovering from failed_generation.")
                return self._recover_from_failed_generation(err_str, messages, caller_role, caller_id)
            raise

        choice = resp.choices[0]

        # ── Structured tool calls ─────────────────────────────────────
        if choice.finish_reason == "tool_calls" and choice.message.tool_calls:
            messages.append(choice.message)

            for tc in choice.message.tool_calls:
                fn_args = json.loads(tc.function.arguments or "{}")
                # Handle both: {"query_spec": "{...}"} and {"table": "events", ...}
                if "query_spec" in fn_args:
                    query_spec = fn_args["query_spec"]
                else:
                    # Model passed query fields directly instead of nesting
                    query_spec = fn_args

                result = execute_db_query(query_spec, caller_role, caller_id)
                logger.info("[Agent] Tool call -> %d rows", result.get("count", 0))

                messages.append({
                    "tool_call_id": tc.id,
                    "role": "tool",
                    "content": json.dumps(result, default=str),
                })

            # Recurse: the model may want to call more tools or generate final answer
            return self._run_agent(messages, caller_role, caller_id, depth + 1)

        # ── Direct answer ─────────────────────────────────────────────
        answer = (choice.message.content or "").strip()

        # ── Handle inline tool calls (Groq fallback format) ───────────
        inline_calls, clean_text = _extract_inline_calls(answer)
        if inline_calls:
            return self._execute_inline_calls(inline_calls, clean_text, messages, caller_role, caller_id)

        if not answer:
            answer = "I couldn't generate a response. Could you try rephrasing your question?"

        return answer

    def _recover_from_failed_generation(self, err_str, messages, caller_role, caller_id):
        """
        Extract the inline function call from Groq's failed_generation error,
        execute the query, and generate a summary response without tools.
        """
        # Try to extract JSON from the failed_generation field
        # Pattern: <function=execute_db_query>{...}</function>
        inline_calls, _ = _extract_inline_calls(err_str)

        # Also try to find raw JSON between 'failed_generation': '...'
        if not inline_calls:
            json_match = re.search(r'"failed_generation":\s*"(.*?)"', err_str, re.DOTALL)
            if json_match:
                raw = json_match.group(1).replace('\\"', '"')
                inline_calls, _ = _extract_inline_calls(raw)

        if not inline_calls:
            # Last resort: find any JSON that looks like a query spec
            json_match = re.search(r'\{["\']table["\'].*?\}', err_str, re.DOTALL)
            if json_match:
                inline_calls = [("execute_db_query", json_match.group(0))]

        if inline_calls:
            return self._execute_inline_calls(inline_calls, "", messages, caller_role, caller_id)

        return "I'm having trouble processing that query. Could you try rephrasing it?"

    def _execute_inline_calls(self, inline_calls, clean_text, messages, caller_role, caller_id):
        """
        Execute extracted inline function calls and get a summarized response.
        """
        tool_results = []
        for fn_name, fn_args_raw in inline_calls:
            if fn_name == "execute_db_query":
                try:
                    fn_args = json.loads(fn_args_raw)
                    # Handle both nested and direct format
                    qs = fn_args.get("query_spec", fn_args)
                    result = execute_db_query(qs, caller_role, caller_id)
                    logger.info("[Agent] Recovered tool -> %d rows", result.get("count", 0))
                    tool_results.append(json.dumps(result, default=str))
                except Exception as e:
                    logger.error("[Agent] Inline tool error: %s", e)
                    tool_results.append(json.dumps({"error": str(e)}))

        if tool_results:
            messages.append({
                "role": "assistant",
                "content": clean_text or "Let me look that up for you.",
            })
            messages.append({
                "role": "user",
                "content": "Here are the database results. Summarize them clearly for the user. "
                           "Keep it short, plain text, no markdown:\n" +
                           "\n---\n".join(tool_results),
            })

            resp2 = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=1024,
            )
            return (resp2.choices[0].message.content or "").strip()

        return clean_text or "I couldn't find the data you're looking for. Could you rephrase?"

    # ─── CONTEXT PARSER ───────────────────────────────────────────────
    def _parse_context(self, context):
        role = "anonymous"
        uid = None
        name = None
        if context:
            parts = {}
            for p in context.split(","):
                if ":" in p:
                    k, v = p.split(":", 1)
                    parts[k.strip()] = v.strip()
            role = parts.get("role", "anonymous")
            try:
                uid = int(parts.get("user_id", "0"))
                if uid == 0:
                    uid = None
            except (ValueError, TypeError):
                uid = None
            name = parts.get("name")
        return role, uid, name

    # ─── ESCALATION ───────────────────────────────────────────────────
    def _escalate(self, user_message, context=None, priority="normal"):
        ticket = EscalationTicket(
            user_query=user_message,
            session_context="priority={} | {}".format(priority, context or "anonymous"),
        )
        try:
            db.session.add(ticket)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("[ChatbotService] Escalation DB error: %s", e)

        if priority == "high":
            return {
                "response": (
                    "I can see this is urgent and frustrating. I've flagged this as high priority "
                    "and a support agent will reach out to you as soon as possible."
                ),
                "escalated": True,
            }
        return {
            "response": (
                "That's outside what I can answer directly. I've passed it to our support team "
                "and they'll get back to you within 24 hours!"
            ),
            "escalated": True,
        }
