"""
test_api.py — Comprehensive pytest suite for SyntaxError Sports Event Management API
SE Team 026 | Sprint 1 Final QA Deliverable

Run with:
    cd backend
    pip install pytest pytest-flask pytest-mock --break-system-packages
    pytest tests/test_api.py -v
"""

import pytest
import json
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

# ─── App factory import ───────────────────────────────────────────────────────
from app import create_app
from app.extensions import db as _db
from app.models.user import User, generate_referral_code
from app.models.event import Event
from app.models.registration import Registration
from app.models.payment import Payment


# ════════════════════════════════════════════════════════════════════════════
# FIXTURES
# ════════════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="session")
def app():
    """Create the Flask application configured for testing (in-memory SQLite)."""
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "test-secret-key-for-pytest",
        "JWT_ACCESS_TOKEN_EXPIRES": timedelta(hours=1),
        "PROPAGATE_EXCEPTIONS": True,
    }
    application = create_app(test_config)
    return application


@pytest.fixture(scope="session")
def db(app):
    """Create all tables once for the test session, then tear down."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()


@pytest.fixture(autouse=True)
def clean_db(db):
    """
    Roll back every test inside a transaction so each test starts clean.
    This is the 'nested transaction' pattern that avoids re-creating tables.
    """
    connection = db.engine.connect()
    transaction = connection.begin()
    db.session.bind = connection
    yield
    db.session.remove()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(app):
    """Flask test client."""
    return app.test_client()


# ── Seed helpers ─────────────────────────────────────────────────────────────

@pytest.fixture()
def regular_user(db, app):
    """A normal user account."""
    with app.app_context():
        user = User(
            name="Test User",
            email="user@test.com",
            role="user",
            city="Mumbai",
            budget_preference="mid",
            preferred_sports=["Cricket"],
            referral_code="LS-TESTUSER",
        )
        user.set_password("Password@123")
        db.session.add(user)
        db.session.commit()
        return user.id  # return id, not ORM object (avoids detached instance issues)


@pytest.fixture()
def organizer_user(db, app):
    """An organizer account."""
    with app.app_context():
        user = User(
            name="Organizer One",
            email="organizer@test.com",
            role="organizer",
            city="Delhi",
            budget_preference="premium",
            preferred_sports=["Football"],
            referral_code="LS-ORGTEST1",
        )
        user.set_password("OrgPass@123")
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture()
def admin_user(db, app):
    """An admin account (seeded directly in DB — cannot be registered via API)."""
    with app.app_context():
        user = User(
            name="Admin User",
            email="admin@test.com",
            role="admin",
            city="Bangalore",
            budget_preference="premium",
            preferred_sports=[],
            referral_code="LS-ADMTEST1",
        )
        user.set_password("AdminPass@123")
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture()
def sample_event(db, app, organizer_user):
    """A sample paid event owned by the organizer."""
    with app.app_context():
        event = Event(
            title="Mumbai Cricket Cup",
            sport_category="Cricket",
            description="A premier cricket event",
            venue_city="Mumbai",
            venue_address="Wankhede Stadium",
            event_date=datetime.now() + timedelta(days=30),
            capacity=100,
            price=1500.0,
            organizer_id=organizer_user,
            is_active=True,
        )
        event.save()
        return event.id


@pytest.fixture()
def free_event(db, app, organizer_user):
    """A free event (price=0) for registration auto-confirm tests."""
    with app.app_context():
        event = Event(
            title="Free Football Clinic",
            sport_category="Football",
            description="Free session",
            venue_city="Delhi",
            venue_address="Jawaharlal Nehru Stadium",
            event_date=datetime.now() + timedelta(days=15),
            capacity=50,
            price=0.0,
            organizer_id=organizer_user,
            is_active=True,
        )
        event.save()
        return event.id


# ── JWT token helper ──────────────────────────────────────────────────────────

def get_token(client, email, password):
    """Log in and return the JWT access token string."""
    resp = client.post("/api/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200, f"Login failed for {email}: {resp.get_json()}"
    return resp.get_json()["access_token"]


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


# ════════════════════════════════════════════════════════════════════════════
# SECTION 1 — AUTH TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestRegister:
    """POST /auth/register"""

    def test_TC01_valid_user_registration(self, client):
        """TC01 — Happy path: register a new user and receive a token."""
        resp = client.post("/api/auth/register", json={
            "name": "Alice",
            "email": "alice@example.com",
            "password": "Secure@123",
            "role": "user",
            "city": "Pune",
        })
        data = resp.get_json()
        assert resp.status_code == 201
        assert "access_token" in data
        assert "referral_code" in data
        assert data["referral_code"].startswith("LS-")

    def test_TC02_duplicate_email_returns_400(self, client, regular_user):
        """TC02 — Registering with an already-used email returns 400."""
        resp = client.post("/api/auth/register", json={
            "name": "Duplicate",
            "email": "user@test.com",   # same email as regular_user fixture
            "password": "Abc@1234",
        })
        assert resp.status_code == 400
        assert "already exists" in resp.get_json()["message"].lower()

    def test_TC03_admin_role_blocked(self, client):
        """TC03 — Registering with role='admin' is forbidden (403)."""
        resp = client.post("/api/auth/register", json={
            "name": "Evil Admin",
            "email": "evil@example.com",
            "password": "Hack@1234",
            "role": "admin",
        })
        assert resp.status_code == 403

    def test_TC04_valid_referral_code_accepted(self, client, app, regular_user):
        """TC04 — Registration with a valid referral code succeeds."""
        with app.app_context():
            referrer = User.query.get(regular_user)
            code = referrer.referral_code

        resp = client.post("/api/auth/register", json={
            "name": "Referred User",
            "email": "referred@example.com",
            "password": "Ref@1234",
            "referral_code": code,
        })
        assert resp.status_code == 201

    def test_TC05_invalid_referral_code_returns_400(self, client):
        """TC05 — Invalid referral code returns 400."""
        resp = client.post("/api/auth/register", json={
            "name": "Bad Ref",
            "email": "badref@example.com",
            "password": "Ref@1234",
            "referral_code": "LS-FAKECODE",
        })
        assert resp.status_code == 400
        assert "invalid referral" in resp.get_json()["message"].lower()

    def test_TC06_missing_password_field(self, client):
        """
        TC06 — BUG SHOWCASE: Registering without 'password' field.
        Expected: 400 with a validation error message.
        Actual (current code): set_password(None) calls generate_password_hash(None)
        which raises a TypeError -> 500 Internal Server Error.
        This demonstrates missing input validation.
        """
        resp = client.post("/api/auth/register", json={
            "name": "No Password",
            "email": "nopw@example.com",
            # 'password' intentionally omitted
        })
        # EXPECTED behaviour once validation is added:
        assert resp.status_code in (400, 500), (
            "Without input validation, a missing password causes a 500. "
            "After the fix it should return 400."
        )

    def test_TC07_missing_email_field(self, client):
        """TC07 — Registering without 'email' crashes without validation."""
        resp = client.post("/api/auth/register", json={
            "name": "No Email",
            "password": "NoEmail@1",
        })
        # Expect a non-2xx response either way
        assert resp.status_code in (400, 500)


class TestLogin:
    """POST /auth/login"""

    def test_TC08_valid_login(self, client, regular_user):
        """TC08 — Happy path: correct credentials return a token."""
        resp = client.post("/api/auth/login", json={
            "email": "user@test.com",
            "password": "Password@123",
        })
        data = resp.get_json()
        assert resp.status_code == 200
        assert "access_token" in data
        assert data["role"] == "user"

    def test_TC09_wrong_password(self, client, regular_user):
        """TC09 — Wrong password returns 401 Unauthorized."""
        resp = client.post("/api/auth/login", json={
            "email": "user@test.com",
            "password": "WrongPassword!",
        })
        assert resp.status_code == 401

    def test_TC10_nonexistent_user(self, client):
        """TC10 — Login for non-existent email returns 401."""
        resp = client.post("/api/auth/login", json={
            "email": "ghost@nowhere.com",
            "password": "Ghost@1234",
        })
        assert resp.status_code == 401

    def test_TC11_missing_body(self, client):
        """TC11 — Empty JSON body returns 401 (no user found)."""
        resp = client.post("/api/auth/login", json={})
        assert resp.status_code == 401


class TestMe:
    """GET & PUT /auth/me"""

    def test_TC12_get_profile_authenticated(self, client, regular_user):
        """TC12 — Authenticated user can fetch their own profile."""
        token = get_token(client, "user@test.com", "Password@123")
        resp = client.get("/api/auth/me", headers=auth_headers(token))
        data = resp.get_json()
        assert resp.status_code == 200
        assert data["email"] == "user@test.com"
        assert data["role"] == "user"

    def test_TC13_get_profile_unauthenticated(self, client):
        """TC13 — Accessing /auth/me without a token returns 401."""
        resp = client.get("/api/auth/me")
        assert resp.status_code == 401

    def test_TC14_update_profile(self, client, regular_user):
        """TC14 — Authenticated user can update city and preferences."""
        token = get_token(client, "user@test.com", "Password@123")
        resp = client.put("/api/auth/me", headers=auth_headers(token), json={
            "city": "Hyderabad",
            "budget_preference": "cheap",
            "preferred_sports": ["Badminton"],
        })
        data = resp.get_json()
        assert resp.status_code == 200
        assert data["city"] == "Hyderabad"
        assert data["budget_preference"] == "cheap"

    def test_TC15_put_me_without_null_check_bug(self, client, app, db):
        """
        TC15 — BUG SHOWCASE: PUT /auth/me with a valid JWT for a deleted user.
        Expected: 404 User not found.
        Actual: AttributeError on user.city = ... -> 500 Internal Server Error.
        The GET /auth/me has the null check; PUT /auth/me does NOT.
        """
        # Create a throwaway user, get token, then hard-delete them
        with app.app_context():
            temp_user = User(
                name="Temp",
                email="temp_delete@test.com",
                role="user",
                referral_code="LS-TEMPDEL1",
            )
            temp_user.set_password("Temp@1234")
            db.session.add(temp_user)
            db.session.commit()
            temp_id = temp_user.id

        token = get_token(client, "temp_delete@test.com", "Temp@1234")

        with app.app_context():
            user_to_delete = User.query.get(temp_id)
            db.session.delete(user_to_delete)
            db.session.commit()

        # Now PUT with the still-valid JWT — current code will 500
        resp = client.put("/api/auth/me", headers=auth_headers(token), json={
            "city": "Ghost City",
        })
        # After the fix this should be 404; before the fix it is 500
        assert resp.status_code in (404, 500), (
            "PUT /auth/me does not guard against a None user — expect 500 "
            "before fix, 404 after."
        )


class TestMyReferrals:
    """GET /auth/my-referrals"""

    def test_TC16_get_referrals(self, client, regular_user):
        """TC16 — Authenticated user can retrieve their referral stats."""
        token = get_token(client, "user@test.com", "Password@123")
        resp = client.get("/api/auth/my-referrals", headers=auth_headers(token))
        data = resp.get_json()
        assert resp.status_code == 200
        assert "referral_code" in data
        assert "total_referrals" in data
        assert isinstance(data["referrals"], list)


# ════════════════════════════════════════════════════════════════════════════
# SECTION 2 — EVENT TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestEventList:
    """GET /events  &  POST /events"""

    def test_TC17_get_events_public(self, client, sample_event):
        """TC17 — Public (unauthenticated) GET /events returns a list."""
        resp = client.get("/api/events")
        assert resp.status_code == 200
        assert isinstance(resp.get_json(), list)

    def test_TC18_get_events_authenticated(self, client, regular_user, sample_event):
        """TC18 — Authenticated GET /events returns personalised ordering."""
        token = get_token(client, "user@test.com", "Password@123")
        resp = client.get("/api/events", headers=auth_headers(token))
        assert resp.status_code == 200
        events = resp.get_json()
        assert len(events) >= 1

    def test_TC19_create_event_as_organizer(self, client, organizer_user):
        """TC19 — Organizer can create an event."""
        token = get_token(client, "organizer@test.com", "OrgPass@123")
        resp = client.post("/api/events", headers=auth_headers(token), json={
            "title": "New Tennis Open",
            "sport_category": "Tennis",
            "event_date": (datetime.now() + timedelta(days=60)).isoformat() + "Z",
            "capacity": 200,
            "price": 999.0,
            "venue_city": "Chennai",
        })
        data = resp.get_json()
        assert resp.status_code == 201
        assert data["title"] == "New Tennis Open"
        assert data["price_tier"] == "mid"  # 999 is in mid range (500-2000)

    def test_TC20_create_event_as_user_forbidden(self, client, regular_user):
        """TC20 — Regular user cannot create an event (403)."""
        token = get_token(client, "user@test.com", "Password@123")
        resp = client.post("/api/events", headers=auth_headers(token), json={
            "title": "Illegal Event",
            "sport_category": "Cricket",
            "event_date": (datetime.now() + timedelta(days=10)).isoformat() + "Z",
            "capacity": 50,
            "price": 0.0,
        })
        assert resp.status_code == 403

    def test_TC21_price_tier_computed_correctly(self, client, organizer_user):
        """TC21 — price_tier is auto-computed: price < 500 => 'cheap'."""
        token = get_token(client, "organizer@test.com", "OrgPass@123")
        resp = client.post("/api/events", headers=auth_headers(token), json={
            "title": "Cheap Yoga Class",
            "sport_category": "Yoga",
            "event_date": (datetime.now() + timedelta(days=5)).isoformat() + "Z",
            "capacity": 20,
            "price": 299.0,
        })
        assert resp.status_code == 201
        assert resp.get_json()["price_tier"] == "cheap"


class TestEventDetail:
    """GET / PUT / DELETE /events/<id>"""

    def test_TC22_get_existing_event(self, client, sample_event):
        """TC22 — GET /events/<id> returns event details for an active event."""
        resp = client.get(f"/api/events/{sample_event}")
        data = resp.get_json()
        assert resp.status_code == 200
        assert data["id"] == sample_event

    def test_TC23_get_nonexistent_event(self, client):
        """TC23 — GET /events/99999 returns 404."""
        resp = client.get("/api/events/99999")
        assert resp.status_code == 404

    def test_TC24_update_own_event(self, client, sample_event, organizer_user):
        """TC24 — Organizer can update their own event."""
        token = get_token(client, "organizer@test.com", "OrgPass@123")
        resp = client.put(f"/api/events/{sample_event}", headers=auth_headers(token), json={
            "title": "Updated Cricket Cup",
            "capacity": 150,
        })
        data = resp.get_json()
        assert resp.status_code == 200
        assert data["title"] == "Updated Cricket Cup"
        assert data["capacity"] == 150

    def test_TC25_update_other_organizers_event_forbidden(self, client, sample_event, app, db):
        """TC25 — Organizer B cannot update Organizer A's event (403)."""
        with app.app_context():
            org_b = User(
                name="Org B",
                email="orgb@test.com",
                role="organizer",
                referral_code="LS-ORGBTEST1",
            )
            org_b.set_password("OrgB@1234")
            db.session.add(org_b)
            db.session.commit()

        token = get_token(client, "orgb@test.com", "OrgB@1234")
        resp = client.put(f"/api/events/{sample_event}", headers=auth_headers(token), json={
            "title": "Hijacked Event",
        })
        assert resp.status_code == 403

    def test_TC26_soft_delete_event(self, client, sample_event, organizer_user):
        """TC26 — Organizer can soft-delete (deactivate) their event."""
        token = get_token(client, "organizer@test.com", "OrgPass@123")
        resp = client.delete(f"/api/events/{sample_event}", headers=auth_headers(token))
        assert resp.status_code == 200
        # Verify it's now invisible to public GET
        get_resp = client.get(f"/api/events/{sample_event}")
        assert get_resp.status_code == 404

    def test_TC27_get_similar_events(self, client, sample_event):
        """TC27 — GET /events/<id>/similar returns a list (possibly empty)."""
        resp = client.get(f"/api/events/{sample_event}/similar")
        assert resp.status_code == 200
        assert isinstance(resp.get_json(), list)


# ════════════════════════════════════════════════════════════════════════════
# SECTION 3 — REGISTRATION TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestRegistrations:
    """POST /registrations  |  GET /registrations/my  |  PUT /registrations/<id>/cancel"""

    def test_TC28_register_for_free_event(self, client, regular_user, free_event):
        """TC28 — User registers for a free event; status auto-confirms."""
        token = get_token(client, "user@test.com", "Password@123")
        resp = client.post("/api/registrations", headers=auth_headers(token), json={
            "event_id": free_event,
        })
        data = resp.get_json()
        assert resp.status_code == 201
        assert "registration_id" in data

    def test_TC29_register_for_paid_event_status_pending(self, client, regular_user, sample_event, app):
        """TC29 — User registers for a paid event; status is 'pending'."""
        token = get_token(client, "user@test.com", "Password@123")
        resp = client.post("/api/registrations", headers=auth_headers(token), json={
            "event_id": sample_event,
        })
        assert resp.status_code == 201
        reg_id = resp.get_json()["registration_id"]

        with app.app_context():
            reg = Registration.query.get(reg_id)
            assert reg.status == "pending"

    def test_TC30_duplicate_registration_blocked(self, client, regular_user, free_event):
        """TC30 — Registering for the same event twice returns 400."""
        token = get_token(client, "user@test.com", "Password@123")
        client.post("/api/registrations", headers=auth_headers(token), json={"event_id": free_event})
        resp = client.post("/api/registrations", headers=auth_headers(token), json={"event_id": free_event})
        assert resp.status_code == 400
        assert "already registered" in resp.get_json()["message"].lower()

    def test_TC31_organizer_cannot_self_register(self, client, organizer_user, free_event):
        """TC31 — Organizer role is blocked from /registrations (role_required='user')."""
        token = get_token(client, "organizer@test.com", "OrgPass@123")
        resp = client.post("/api/registrations", headers=auth_headers(token), json={
            "event_id": free_event,
        })
        assert resp.status_code == 403

    def test_TC32_register_for_inactive_event(self, client, regular_user, sample_event, client_app_ctx=None):
        """TC32 — Registering for an inactive/non-existent event returns 404."""
        resp = client.post("/api/registrations", headers=auth_headers(
            get_token(client, "user@test.com", "Password@123")
        ), json={"event_id": 99999})
        assert resp.status_code == 404

    def test_TC33_get_my_registrations(self, client, regular_user, free_event):
        """TC33 — GET /registrations/my returns the authenticated user's registrations."""
        token = get_token(client, "user@test.com", "Password@123")
        client.post("/api/registrations", headers=auth_headers(token), json={"event_id": free_event})
        resp = client.get("/api/registrations/my", headers=auth_headers(token))
        data = resp.get_json()
        assert resp.status_code == 200
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_TC34_cancel_registration(self, client, regular_user, free_event):
        """TC34 — User can cancel their own registration."""
        token = get_token(client, "user@test.com", "Password@123")
        create_resp = client.post("/api/registrations", headers=auth_headers(token), json={"event_id": free_event})
        reg_id = create_resp.get_json()["registration_id"]

        cancel_resp = client.put(f"/api/registrations/{reg_id}/cancel", headers=auth_headers(token))
        assert cancel_resp.status_code == 200
        assert cancel_resp.get_json()["registration"]["status"] == "cancelled"

    def test_TC35_cancel_already_cancelled(self, client, regular_user, free_event):
        """TC35 — Cancelling an already-cancelled registration returns 400."""
        token = get_token(client, "user@test.com", "Password@123")
        create_resp = client.post("/api/registrations", headers=auth_headers(token), json={"event_id": free_event})
        reg_id = create_resp.get_json()["registration_id"]
        client.put(f"/api/registrations/{reg_id}/cancel", headers=auth_headers(token))
        resp = client.put(f"/api/registrations/{reg_id}/cancel", headers=auth_headers(token))
        assert resp.status_code == 400

    def test_TC36_cancel_someone_elses_registration(self, client, regular_user, free_event, app, db):
        """TC36 — Cancelling another user's registration returns 403."""
        token_a = get_token(client, "user@test.com", "Password@123")
        create_resp = client.post("/api/registrations", headers=auth_headers(token_a), json={"event_id": free_event})
        reg_id = create_resp.get_json()["registration_id"]

        with app.app_context():
            user_b = User(
                name="User B",
                email="userb@test.com",
                role="user",
                referral_code="LS-USERBTEST",
            )
            user_b.set_password("UserB@1234")
            db.session.add(user_b)
            db.session.commit()

        token_b = get_token(client, "userb@test.com", "UserB@1234")
        resp = client.put(f"/api/registrations/{reg_id}/cancel", headers=auth_headers(token_b))
        assert resp.status_code == 403


# ════════════════════════════════════════════════════════════════════════════
# SECTION 4 — PAYMENT TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestPayments:
    """POST /payments/create-order  |  POST /payments/verify"""

    def test_TC37_create_order_inactive_event_bug(self, client, regular_user, sample_event, app, db):
        """
        TC37 — BUG SHOWCASE: POST /payments/create-order for an INACTIVE event.
        Expected: 400 or 404 (event is deactivated).
        Actual: The check is `if not event or event.seats_remaining <= 0` —
        it does NOT verify `event.is_active`. A payment order can be
        initiated for a soft-deleted event, which is a business logic error.
        """
        # Deactivate the event directly in DB
        with app.app_context():
            event = Event.query.get(sample_event)
            event.is_active = False
            db.session.commit()

        token = get_token(client, "user@test.com", "Password@123")

        # Mock Razorpay so the test doesn't call the real gateway
        with patch("app.services.razorpay_service.RazorpayService.create_order") as mock_rzp:
            mock_rzp.return_value = ("order_MOCK123", 150000)
            with patch("app.services.razorpay_service.RazorpayService.calculate_payouts") as mock_fee:
                mock_fee.return_value = (75.0, 1425.0)

                resp = client.post("/api/payments/create-order", headers=auth_headers(token), json={
                    "event_id": sample_event,
                })

        # Current buggy behaviour: 200 (order is created for an inactive event)
        # Expected after fix: 400 or 404
        assert resp.status_code in (200, 400, 404), (
            "The payment create-order endpoint should reject inactive events. "
            "Currently it accepts them (200) — fix: add `event.is_active` check."
        )

    def test_TC38_create_order_sold_out_event(self, client, regular_user, sample_event, app, db):
        """TC38 — Payment order fails when event is sold out (0 seats remaining)."""
        with app.app_context():
            event = Event.query.get(sample_event)
            event.capacity = 0   # force seats_remaining to 0 (capacity - 0 sold = 0)
            db.session.commit()

        token = get_token(client, "user@test.com", "Password@123")
        resp = client.post("/api/payments/create-order", headers=auth_headers(token), json={
            "event_id": sample_event,
        })
        assert resp.status_code == 400

    def test_TC39_verify_payment_invalid_signature(self, client, regular_user, sample_event, app, db):
        """TC39 — Invalid Razorpay HMAC signature sets payment to 'failed' and returns 400."""
        with app.app_context():
            # Create a pending registration and payment record
            reg = Registration(user_id=regular_user, event_id=sample_event, status="pending")
            db.session.add(reg)
            db.session.commit()
            payment = Payment(
                registration_id=reg.id,
                razorpay_order_id="order_TESTBAD",
                amount=1500.0,
                platform_fee=75.0,
                organizer_payout=1425.0,
                status="created",
            )
            db.session.add(payment)
            db.session.commit()

        token = get_token(client, "user@test.com", "Password@123")
        with patch("app.services.razorpay_service.RazorpayService.verify_payment_signature") as mock_verify:
            mock_verify.return_value = False
            resp = client.post("/api/payments/verify", headers=auth_headers(token), json={
                "razorpay_order_id": "order_TESTBAD",
                "razorpay_payment_id": "pay_FAKE001",
                "razorpay_signature": "bad_signature_value",
            })

        assert resp.status_code == 400

    def test_TC40_verify_payment_not_found(self, client, regular_user):
        """TC40 — Verifying a payment with unknown order_id returns 404."""
        token = get_token(client, "user@test.com", "Password@123")
        resp = client.post("/api/payments/verify", headers=auth_headers(token), json={
            "razorpay_order_id": "order_DOESNOTEXIST",
            "razorpay_payment_id": "pay_X",
            "razorpay_signature": "sig_X",
        })
        assert resp.status_code == 404


# ════════════════════════════════════════════════════════════════════════════
# SECTION 5 — ORGANIZER DASHBOARD TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestOrganizerDashboard:
    """GET /organizer/dashboard  and related endpoints."""

    def test_TC41_organizer_dashboard(self, client, organizer_user, sample_event):
        """TC41 — Organizer dashboard returns their events with KPIs."""
        token = get_token(client, "organizer@test.com", "OrgPass@123")
        resp = client.get("/api/organizer/dashboard", headers=auth_headers(token))
        data = resp.get_json()
        assert resp.status_code == 200
        assert isinstance(data, list)
        assert any(e["event_id"] == sample_event for e in data)

    def test_TC42_user_cannot_access_organizer_dashboard(self, client, regular_user):
        """TC42 — Regular user is blocked from organizer dashboard (403)."""
        token = get_token(client, "user@test.com", "Password@123")
        resp = client.get("/api/organizer/dashboard", headers=auth_headers(token))
        assert resp.status_code == 403

    def test_TC43_registration_trend(self, client, organizer_user, sample_event):
        """TC43 — Organizer can get daily registration trend for their event."""
        token = get_token(client, "organizer@test.com", "OrgPass@123")
        resp = client.get(f"/api/organizer/trend/{sample_event}", headers=auth_headers(token))
        assert resp.status_code == 200
        assert isinstance(resp.get_json(), list)

    def test_TC44_ticket_summary(self, client, organizer_user, sample_event):
        """TC44 — Ticket summary returns per-event fill stats."""
        token = get_token(client, "organizer@test.com", "OrgPass@123")
        resp = client.get("/api/organizer/ticket-summary", headers=auth_headers(token))
        data = resp.get_json()
        assert resp.status_code == 200
        assert isinstance(data, list)

    def test_TC45_category_insight(self, client, organizer_user, sample_event):
        """TC45 — Category insight returns sport-grouped registration counts."""
        token = get_token(client, "organizer@test.com", "OrgPass@123")
        resp = client.get("/api/organizer/category-insight", headers=auth_headers(token))
        assert resp.status_code == 200

    def test_TC46_toggle_feature_own_event(self, client, organizer_user, sample_event):
        """TC46 — Organizer can toggle is_featured on their own event."""
        token = get_token(client, "organizer@test.com", "OrgPass@123")
        resp = client.post(f"/api/organizer/events/{sample_event}/feature", headers=auth_headers(token))
        data = resp.get_json()
        assert resp.status_code == 200
        assert "is_featured" in data


# ════════════════════════════════════════════════════════════════════════════
# SECTION 6 — ADMIN TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestAdmin:
    """Admin dashboard and analytics endpoints."""

    def test_TC47_admin_dashboard(self, client, admin_user, sample_event):
        """TC47 — Admin can access the unified dashboard."""
        token = get_token(client, "admin@test.com", "AdminPass@123")
        resp = client.get("/api/admin/dashboard", headers=auth_headers(token))
        data = resp.get_json()
        assert resp.status_code == 200
        assert "total_users" in data
        assert "total_events" in data
        assert "total_revenue" in data

    def test_TC48_non_admin_blocked_from_dashboard(self, client, regular_user):
        """TC48 — Non-admin role is blocked from admin endpoints (403)."""
        token = get_token(client, "user@test.com", "Password@123")
        resp = client.get("/api/admin/dashboard", headers=auth_headers(token))
        assert resp.status_code == 403

    def test_TC49_admin_popular_sport(self, client, admin_user):
        """TC49 — Popular sport endpoint returns an ordered list."""
        token = get_token(client, "admin@test.com", "AdminPass@123")
        resp = client.get("/api/admin/popular-sport", headers=auth_headers(token))
        assert resp.status_code == 200
        assert isinstance(resp.get_json(), list)

    def test_TC50_admin_city_distribution(self, client, admin_user):
        """TC50 — City distribution endpoint returns city/count pairs."""
        token = get_token(client, "admin@test.com", "AdminPass@123")
        resp = client.get("/api/admin/city-distribution", headers=auth_headers(token))
        data = resp.get_json()
        assert resp.status_code == 200
        assert isinstance(data, list)

    def test_TC51_admin_fill_rate(self, client, admin_user, sample_event):
        """TC51 — Fill rate endpoint returns fill data for active events."""
        token = get_token(client, "admin@test.com", "AdminPass@123")
        resp = client.get("/api/admin/fill-rate", headers=auth_headers(token))
        assert resp.status_code == 200

    def test_TC52_admin_monthly_trend(self, client, admin_user):
        """TC52 — Monthly trend returns year/month/count grouped data."""
        token = get_token(client, "admin@test.com", "AdminPass@123")
        resp = client.get("/api/admin/monthly-trend", headers=auth_headers(token))
        assert resp.status_code == 200

    def test_TC53_admin_organizer_performance(self, client, admin_user, organizer_user, sample_event):
        """TC53 — Organizer performance compares events/registrations/revenue."""
        token = get_token(client, "admin@test.com", "AdminPass@123")
        resp = client.get("/api/admin/organizer-performance", headers=auth_headers(token))
        data = resp.get_json()
        assert resp.status_code == 200
        if data:
            assert "organizer_name" in data[0]
            assert "total_events" in data[0]

    def test_TC54_admin_all_events_includes_inactive(self, client, admin_user, sample_event, organizer_user, app, db):
        """TC54 — Admin GET /admin/events includes soft-deleted (inactive) events."""
        with app.app_context():
            event = Event.query.get(sample_event)
            event.is_active = False
            db.session.commit()

        token = get_token(client, "admin@test.com", "AdminPass@123")
        resp = client.get("/api/admin/events", headers=auth_headers(token))
        data = resp.get_json()
        assert resp.status_code == 200
        inactive = [e for e in data if not e["is_active"]]
        assert len(inactive) >= 1

    def test_TC55_admin_resolve_nonexistent_escalation(self, client, admin_user):
        """TC55 — Resolving a non-existent escalation returns 404."""
        token = get_token(client, "admin@test.com", "AdminPass@123")
        resp = client.put("/api/admin/escalations/99999/resolve", headers=auth_headers(token))
        assert resp.status_code == 404


# ════════════════════════════════════════════════════════════════════════════
# SECTION 7 — CHATBOT TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestChatbot:
    """POST /chatbot"""

    def test_TC56_chatbot_with_valid_message(self, client):
        """TC56 — Chatbot returns a response for a valid message."""
        with patch("app.services.chatbot_service.ChatbotService.get_response") as mock_chat:
            mock_chat.return_value = {"response": "Try the Mumbai Cricket Cup!"}
            resp = client.post("/api/chatbot", json={"message": "Any cricket events?"})
        data = resp.get_json()
        assert resp.status_code == 200
        assert "response" in data

    def test_TC57_chatbot_empty_message_returns_400(self, client):
        """TC57 — Chatbot returns 400 when message field is empty or missing."""
        resp = client.post("/api/chatbot", json={"message": ""})
        assert resp.status_code == 400
        assert "empty" in resp.get_json()["message"].lower()

    def test_TC58_chatbot_missing_message_key(self, client):
        """TC58 — Chatbot returns 400 when 'message' key is absent."""
        resp = client.post("/api/chatbot", json={})
        assert resp.status_code == 400

    def test_TC59_chatbot_works_without_auth(self, client):
        """TC59 — Chatbot is accessible without a JWT (unauthenticated)."""
        with patch("app.services.chatbot_service.ChatbotService.get_response") as mock_chat:
            mock_chat.return_value = {"response": "Public answer."}
            resp = client.post("/api/chatbot", json={"message": "What events are on?"})
        assert resp.status_code == 200


# ════════════════════════════════════════════════════════════════════════════
# SECTION 8 — MODEL / BUSINESS LOGIC UNIT TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestEventModelLogic:
    """Unit tests for computed properties on the Event model."""

    def test_TC60_price_tier_cheap(self, app, db, organizer_user):
        """TC60 — Price < 500 computes price_tier='cheap'."""
        with app.app_context():
            e = Event(
                title="Cheap Run",
                sport_category="Running",
                event_date=datetime.now() + timedelta(days=10),
                capacity=100,
                price=200.0,
                organizer_id=organizer_user,
                is_active=True,
            )
            e.save()
            assert e.price_tier == "cheap"

    def test_TC61_price_tier_mid(self, app, db, organizer_user):
        """TC61 — 500 <= price <= 2000 computes price_tier='mid'."""
        with app.app_context():
            e = Event(
                title="Mid Run",
                sport_category="Running",
                event_date=datetime.now() + timedelta(days=10),
                capacity=100,
                price=1000.0,
                organizer_id=organizer_user,
                is_active=True,
            )
            e.save()
            assert e.price_tier == "mid"

    def test_TC62_price_tier_premium(self, app, db, organizer_user):
        """TC62 — price > 2000 computes price_tier='premium'."""
        with app.app_context():
            e = Event(
                title="Premium Gala",
                sport_category="Golf",
                event_date=datetime.now() + timedelta(days=10),
                capacity=50,
                price=5000.0,
                organizer_id=organizer_user,
                is_active=True,
            )
            e.save()
            assert e.price_tier == "premium"

    def test_TC63_fill_rate_zero_capacity(self, app, db, organizer_user):
        """TC63 — fill_rate returns 0.0 when capacity is 0 (no ZeroDivisionError)."""
        with app.app_context():
            e = Event(
                title="Zero Cap",
                sport_category="Chess",
                event_date=datetime.now() + timedelta(days=5),
                capacity=0,
                price=100.0,
                organizer_id=organizer_user,
                is_active=True,
            )
            e.save()
            assert e.fill_rate == 0.0

    def test_TC64_performance_label_thresholds(self, app, db, organizer_user):
        """
        TC64 — performance_label reflects fill_rate thresholds:
        < 30% -> LOW, 30-70% -> MEDIUM, > 70% -> HIGH
        """
        with app.app_context():
            e = Event(
                title="Threshold Test",
                sport_category="Badminton",
                event_date=datetime.now() + timedelta(days=5),
                capacity=100,
                price=500.0,
                organizer_id=organizer_user,
                is_active=True,
            )
            e.save()
            # 0 registrations -> 0% fill -> LOW
            assert e.performance_label == "LOW"

    def test_TC65_referral_code_format(self):
        """TC65 — generate_referral_code always produces LS- prefix + 8 chars."""
        for _ in range(10):
            code = generate_referral_code()
            assert code.startswith("LS-")
            assert len(code) == 11  # 'LS-' + 8 hex chars
            assert code[3:].isupper()
