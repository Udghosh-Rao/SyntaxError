# ⚽ SyntaxError — Sports Event Management Platform

> **SE Team 026** | Full-Stack MVP | Flask + Vue 3 + Tailwind CSS

A full-stack sports event management platform that connects **organizers**, **athletes**, and **admins** through intelligent recommendations, real-time analytics, and seamless payment processing.

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture & Pipeline](#-architecture--pipeline)
- [Project Structure](#-project-structure)
- [User Roles](#-user-roles)
- [API Endpoints](#-api-endpoints)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Running Tests](#-running-tests)
- [Seed Data (Demo Users)](#-seed-data-demo-users)

---

## 🌟 Project Overview

SyntaxError solves the fragmented sports event ecosystem by providing a **unified digital platform** where:

- **Organizers** can create, manage, and analyse their sports events
- **Athletes** can discover, register, and pay for events that match their city, budget, and sport preferences
- **Admins** get a bird's-eye view of the entire platform with real-time analytics

---

## ✨ Features

### 🔐 Authentication & Roles (4 Features)
| # | Feature |
|---|---------|
| 1 | User registration (user / organizer roles) |
| 2 | JWT-based login with role-encoded tokens |
| 3 | View & update user profile |
| 4 | Role-based access control (RBAC) on every endpoint |

### 🗓️ Events & Smart Recommendations (5 Features)
| # | Feature |
|---|---------|
| 1 | **Sport preference match** — events matching user's preferred sports scored higher (+40 pts) |
| 2 | **City-based filtering** — local events prioritised (+30 pts) |
| 3 | **Budget tier matching** — cheap / mid / premium filter (+20 pts) |
| 4 | **Upcoming in 7 days** — time-sensitive events boosted (+10 pts) |
| 5 | **Similar events** — same sport + city recommendations |

### 💳 Payments (2 Features)
| # | Feature |
|---|---------|
| 6 | Razorpay order creation with platform fee calculation (15%) |
| 7 | Payment signature verification & automatic registration confirmation |

### 🏢 Organizer Dashboard (5 Features)
| # | Feature |
|---|---------|
| 8  | Event list with KPIs (registrations, revenue, fill-rate) |
| 9  | Performance badges: LOW / MEDIUM / HIGH fill rate labels |
| 10 | Daily registration trend data (line-chart ready) |
| 11 | Ticket sales summary across all events |
| 12 | Sport category breakdown (registrations per sport) |

### 📊 Admin Analytics (6 Features)
| # | Feature |
|---|---------|
| 13 | Unified platform dashboard (total users, events, registrations, revenue) |
| 14 | Most popular sport categories |
| 15 | User distribution by city |
| 16 | Platform-wide event fill-rate tracking |
| 17 | Monthly registration trend |
| 18 | Organizer performance comparison |

### 🤖 AI Chatbot (1 Feature)
| # | Feature |
|---|---------|
| 19 | Keyword-based FAQ chatbot with escalation ticket creation for unresolved queries |

### 🔍 Search (1 Feature)
| # | Feature |
|---|---------|
| 20 | Algolia-powered typo-tolerant search (mock-ready, real keys pluggable) |

---

## 🛠️ Tech Stack

### Backend
| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.8+ | Runtime |
| Flask | 3.0.3 | Web framework |
| Flask-RESTx | 1.3.0 | REST API + Swagger UI |
| Flask-JWT-Extended | 4.6.0 | JWT authentication |
| Flask-SQLAlchemy | 3.1.1 | ORM |
| Flask-Migrate | 4.0.7 | DB migrations |
| Flask-CORS | 4.0.1 | Cross-origin requests |
| SQLite (dev) / PostgreSQL (prod) | — | Database |
| Razorpay SDK | 1.4.1 | Payment processing |
| Algolia | 3.0.0 | Search indexing |
| LangChain + OpenAI/Gemini | 0.2.x | AI chatbot RAG pipeline |
| Werkzeug | 3.0.4 | Password hashing |

### Frontend
| Tool | Version | Purpose |
|------|---------|---------|
| Vue 3 | ^3.3.4 | UI framework (Composition API) |
| TypeScript | ^5.1.6 | Type safety |
| Vite | ^4.4.5 | Build tool & dev server |
| Vue Router | ^4.2.4 | Client-side routing |
| Pinia | ^2.1.4 | State management |
| Tailwind CSS | ^3.3.3 | Utility-first styling |
| Chart.js | ^4.5.1 | Analytics charts |
| Axios | ^1.4.0 | HTTP client |

---

## 🏗️ Architecture & Pipeline

```
┌──────────────────────────────────────────────────────┐
│                     Browser (Vue 3 SPA)               │
│  ┌──────────┐  ┌──────────────┐  ┌─────────────────┐ │
│  │  Auth &  │  │   Events &   │  │    Dashboards   │ │
│  │ Register │  │ Registration │  │  Admin/Organizer │ │
│  └────┬─────┘  └──────┬───────┘  └────────┬────────┘ │
└───────┼───────────────┼──────────────────-┼──────────┘
        │  Axios (JWT Bearer Token headers)  │
        ▼                                   ▼
┌──────────────────────────────────────────────────────┐
│               Flask REST API  (/api/*)                │
│  ┌───────┐ ┌────────┐ ┌─────────────┐ ┌──────────┐  │
│  │ auth  │ │ events │ │ organizer/  │ │ payments │  │
│  │       │ │        │ │    admin    │ │          │  │
│  └───────┘ └────────┘ └─────────────┘ └──────────┘  │
│           Flask-JWT-Extended (RBAC)                   │
│           Flask-SQLAlchemy (ORM)                      │
└────────────────┬─────────────────────────────────────┘
                 │
        ┌────────▼────────┐
        │  SQLite / PgSQL  │
        │   (via ORM)      │
        └────────┬─────────┘
                 │ (External Services — Keys optional for dev)
        ┌────────▼──────────────────┐
        │  Razorpay  │  Algolia     │
        │  Payments  │  Search      │
        └────────────┴──────────────┘

Request Pipeline:
  Client → Vue Router → Pinia Store → Axios → Flask Blueprint
         → JWT Validation → role_required() decorator
         → Resource Handler → SQLAlchemy → DB → JSON Response
```

---

## 📁 Project Structure

```
SyntaxError/
├── backend/
│   ├── app/
│   │   ├── __init__.py              # Flask app factory
│   │   ├── config.py                # Dev / Prod config
│   │   ├── extensions.py            # db, jwt, cors, migrate
│   │   ├── api/
│   │   │   ├── __init__.py          # Blueprint + API registration
│   │   │   ├── auth.py              # /api/auth/*
│   │   │   ├── events.py            # /api/events/*
│   │   │   ├── registrations.py     # /api/registrations/*
│   │   │   ├── payments.py          # /api/payments/*
│   │   │   ├── organizer.py         # /api/organizer/*
│   │   │   ├── admin.py             # /api/admin/*
│   │   │   └── chatbot.py           # /api/chatbot/*
│   │   ├── models/
│   │   │   ├── user.py              # User model (3 roles)
│   │   │   ├── event.py             # Event + computed KPIs
│   │   │   ├── registration.py      # User ↔ Event link
│   │   │   ├── payment.py           # Razorpay payment record
│   │   │   └── escalation.py        # Chatbot escalation tickets
│   │   ├── services/
│   │   │   ├── recommendation.py    # Scored event recommendations
│   │   │   ├── algolia_sync.py      # Search index sync
│   │   │   ├── razorpay_service.py  # Payment order + verification
│   │   │   └── chatbot_service.py   # FAQ + escalation logic
│   │   └── utils/
│   │       └── decorators.py        # role_required() RBAC decorator
│   ├── tests/
│   │   ├── test_app.py              # Basic smoke tests (3 tests)
│   │   └── test_comprehensive.py    # Full CRUD tests, 47 tests
│   ├── migrations/                  # Flask-Migrate DB migrations
│   ├── seed_db.py                   # Seed demo users, events, payments
│   ├── requirements.txt
│   ├── run.py                       # Entry point → port 8000
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── main.ts                  # Vue app entry
│   │   ├── App.vue                  # Root component
│   │   ├── router/                  # Vue Router (role-based guards)
│   │   ├── stores/                  # Pinia state stores
│   │   ├── views/                   # Page-level components
│   │   └── components/              # Reusable UI components
│   ├── index.html
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── package.json
│
└── README.md
```

---

## 👥 User Roles

| Role | Access |
|------|--------|
| **user** | Browse events, register & pay, view own registrations, cancel registrations, use chatbot |
| **organizer** | All of above + Create / Edit / Delete own events, view organizer analytics dashboard |
| **admin** | All platform access — view all analytics, delete any event, resolve escalation tickets |

---

## 🌐 API Endpoints

All endpoints are prefixed with `/api`. Swagger UI available at **http://localhost:8000/api/docs**

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register` | Public | Register new user or organizer |
| POST | `/auth/login` | Public | Login → returns JWT token |
| GET | `/auth/me` | Any role | Get own profile |
| PUT | `/auth/me` | Any role | Update own profile |
| GET | `/events` | Public | List recommended events |
| POST | `/events` | Organizer | Create new event |
| GET | `/events/<id>` | Public | Get event details |
| PUT | `/events/<id>` | Organizer (own) | Update event |
| DELETE | `/events/<id>` | Organizer/Admin | Soft-delete event |
| GET | `/events/<id>/similar` | Public | Get similar events |
| POST | `/registrations` | User | Register for an event |
| GET | `/registrations/my` | User | View my registrations |
| PUT | `/registrations/<id>/cancel` | User | Cancel a registration |
| POST | `/payments/create-order` | User | Create Razorpay order |
| POST | `/payments/verify` | User | Verify payment signature |
| GET | `/organizer/dashboard` | Organizer | Event KPIs |
| GET | `/organizer/trend/<event_id>` | Organizer | Daily registration trend |
| GET | `/organizer/ticket-summary` | Organizer | Sales summary |
| GET | `/organizer/category-insight` | Organizer | Registrations by sport |
| POST | `/organizer/events/<id>/feature` | Organizer/Admin | Toggle featured status |
| GET | `/admin/dashboard` | Admin | Platform-wide metrics |
| GET | `/admin/popular-sport` | Admin | Most popular sports |
| GET | `/admin/city-distribution` | Admin | Users by city |
| GET | `/admin/fill-rate` | Admin | Event fill rates |
| GET | `/admin/monthly-trend` | Admin | Monthly registrations |
| GET | `/admin/organizer-performance` | Admin | Organizer comparison |
| GET | `/admin/escalations` | Admin | Unresolved chatbot tickets |
| PUT | `/admin/escalations/<id>/resolve` | Admin | Resolve a ticket |
| POST | `/chatbot/message` | Any role | Send chatbot message |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** — [Download](https://www.python.org/downloads/)
- **Node.js 18+** — [Download](https://nodejs.org/)
- **Git** — [Download](https://git-scm.com/)

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/<your-username>/SyntaxError.git
cd SyntaxError
```

---

### Step 2 — Backend Setup

```bash
# Navigate into the backend folder
cd backend

# (Recommended) Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install all Python dependencies
pip install -r requirements.txt
```

---

### Step 3 — Configure Environment Variables

```bash
# Copy the example env file
cp .env.example .env
```

Then open `backend/.env` and fill in your values (see [Environment Variables](#-environment-variables) below). For local development the defaults work out of the box.

---

### Step 4 — Seed the Database

This creates the SQLite database and populates it with demo users, events, and registrations:

```bash
python seed_db.py
```

You'll see output like:
```
Clearing database...
Seeding Users...
Seeding Events...
Seeding Registrations & Payments...
Database seeding complete!
```

---

### Step 5 — Start the Backend Server

```bash
python run.py
```

✅ API is live at: **http://localhost:8000**  
📄 Swagger UI at: **http://localhost:8000/api/docs**

---

### Step 6 — Frontend Setup

Open a **new terminal** and run:

```bash
cd frontend

# Install Node dependencies
npm install

# Start the development server
npm run dev
```

✅ App is live at: **http://localhost:5173**

---

## 🔑 Environment Variables

Create `backend/.env` with the following keys:

```env
# Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Payments (Razorpay — test keys work fine for dev)
RAZORPAY_KEY_ID=rzp_test_xxxxxxxx
RAZORPAY_KEY_SECRET=your_razorpay_secret
PLATFORM_FEE=0.15

# Search (Algolia — optional, mocked without keys)
ALGOLIA_APP_ID=XXXXXXXXXX
ALGOLIA_API_KEY=your_algolia_admin_key
ALGOLIA_INDEX=events

# AI Chatbot (optional)
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=your-gemini-key
```

> **Note:** The app runs perfectly in development **without** Razorpay, Algolia, or AI keys. Those services are mocked gracefully when keys are missing.

---

## 🧪 Running Tests

With the backend virtual environment active:

```bash
cd backend

# Install pytest (one time)
pip install pytest

# Run all tests (50 tests)
python -m pytest tests/ -v
```

Expected output:
```
tests/test_app.py::test_register_user              PASSED
tests/test_app.py::test_login                      PASSED
tests/test_app.py::test_admin_cannot_register_publicly PASSED
tests/test_comprehensive.py::TestAuth ...          PASSED (10 tests)
tests/test_comprehensive.py::TestEvents ...        PASSED (12 tests)
tests/test_comprehensive.py::TestRegistrations ... PASSED (8 tests)
tests/test_comprehensive.py::TestAdmin ...         PASSED (10 tests)
tests/test_comprehensive.py::TestOrganizer ...     PASSED (7 tests)

========= 50 passed =========
```

---

## 🌱 Seed Data (Demo Users)

After running `python seed_db.py`, the following accounts are available:

| Name | Email | Password | Role |
|------|-------|----------|------|
| Admin Boss | `admin@example.com` | `123456` | admin |
| Sports Authority | `org1@example.com` | `123456` | organizer |
| Active Life Org | `org2@example.com` | `123456` | organizer |
| Rahul Sharma | `user1@example.com` | `123456` | user |
| Priya Patel | `user2@example.com` | `123456` | user |

**Seeded Events:**
- 🏃 Delhi Monsoon Marathon (Running, ₹500)
- ⚽ Corporate Football League (Football, ₹2500)
- 🚴 Mumbai Midnight Cycling (Cycling, ₹300)
- 🎾 Pro Tennis Workshop (Tennis, ₹5000)

---

## 📝 License

Confidential — For Internal Use Only (SE Team 026 — Syntax Error)