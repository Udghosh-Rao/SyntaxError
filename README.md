# SyntaxError - Sports Event Management MVP

A comprehensive sports event management platform with intelligent recommendations, real-time analytics, and seamless payment processing.

## Project Overview

SyntaxError is a full-stack application built for SE Team 026 that solves the gap in sports event industry by providing:

- **Unified Digital Platform**: Connects event organizers with participants
- **Intelligent Recommendations**: Rule-based and AI-assisted event suggestions
- **Business Intelligence**: Dashboards for organizers and admins
- **Secure Payments**: Razorpay integrated checkout
- **24/7 AI Chatbot**: LangChain-powered conversational support
- **Fast Search**: Typo-tolerant search via Algolia

## Technology Stack

### Backend
- **Framework**: Flask 3.0.3 with Flask-RESTful
- **Database**: PostgreSQL/SQLite with SQLAlchemy ORM
- **Authentication**: JWT (Flask-JWT-Extended)
- **Database Migration**: Flask-Migrate
- **API Documentation**: RESTful endpoints with full CORS support

### Frontend
- **Framework**: Vue 3 with Composition API
- **Routing**: Vue Router for SPA navigation
- **State Management**: Pinia
- **Build Tool**: Vite CLI

### External Integrations
- **Payments**: Razorpay for secure payment processing
- **Search**: Algolia for instant, typo-tolerant event search
- **GenAI**: OpenAI, Google Gemini, HuggingFace with LangChain
- **Version Control**: GitHub
- **Project Management**: Jira

## Project Structure

```
SyntaxError/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── config.py            # Configuration management
│   │   ├── extensions.py        # Flask extensions setup
│   │   ├── models/              # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   ├── event.py
│   │   │   ├── registration.py
│   │   │   └── payment.py
│   │   ├── api/                 # REST API endpoints
│   │   │   ├── auth.py
│   │   │   ├── events.py
│   │   │   ├── payments.py
│   │   │   ├── chatbot.py
│   │   │   ├── organizer.py
│   │   │   └── admin.py
│   │   └── services/            # Business logic
│   │       ├── recommendation.py
│   │       ├── chatbot_service.py
│   │       ├── algolia_sync.py
│   │       └── razorpay_service.py
│   ├── run.py                   # Application entry point
│   ├── requirements.txt         # Python dependencies
│   └── .env.example            # Environment variables template
│
├── frontend/                    # Vue 3 SPA (to be implemented)
└── README.md                    # This file
```

## Database Models

### User
- Authentication with hashed passwords
- Three roles: user, organizer, admin
- City and budget preferences for recommendations
- Preferred sports for personalization

### Event
- Core event information (title, sport, location, date)
- Pricing tiers (cheap, mid, premium)
- Event tags (outdoor, team, night)
- Computed properties: seats_remaining, fill_rate, performance_label

### Registration
- Links users to events
- Status tracking: pending, confirmed, cancelled
- Audit trail with timestamps

### Payment
- Razorpay integration with order tracking
- Platform fees and organizer payouts
- Payment status management

## API Features

### Authentication (4 features)
1. User registration
2. Login with JWT token generation
3. Token refresh
4. Role-based access control

### Events & Recommendations (5 features)
1. List recommended events with personalization
2. Nearby events by city
3. Upcoming events (7-day window)
4. Budget filtering
5. Similar events suggestions

### Payments (2 features)
1. Razorpay order creation
2. Webhook signature verification

### Organizer Dashboard (5 features)
8. Event list with KPIs
9. Performance summary badges
10. Registration trend graphs
11. Category insights
12. Ticket sales summary

### Admin Analytics (5 features)
13. Platform-wide analytics
14. Popular sport categories
15. User distribution by city
16. Event fill-rate tracking
17. Monthly registration trends
18. Organizer performance comparison

### AI Chatbot (1 feature)
7. LangChain-powered FAQ assistant with context retrieval

### Search (1 feature)
6. Algolia full-text search with instant results

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL (for production) or SQLite (for development)
- Node.js 16+ (for frontend)
- Git

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database
flask db upgrade
flask init-db

# Run development server
python run.py
```

Server will be available at http://localhost:5000

### Frontend Setup (Coming Soon)

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

Create a `.env` file in the backend directory:

```
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost/sportsdb
RAZORPAY_KEY_ID=your-razorpay-key
RAZORPAY_KEY_SECRET=your-razorpay-secret
ALGOLIA_APP_ID=your-algolia-app-id
ALGOLIA_API_KEY=your-algolia-api-key
OPENAI_API_KEY=your-openai-key
GEMINI_API_KEY=your-gemini-key (optional)
```

## Release Timeline

- **February 17, 2026**: MVP Release v1.0
- **Sprint Duration**: 4 weeks
- **18 Core Features**: Delivered across 4 sprints

## Key Achievements

✅ Complete Flask REST API with JWT authentication
✅ SQLAlchemy database models with relationships
✅ Multi-role authorization (user, organizer, admin)
✅ Razorpay payment integration
✅ Algolia search integration
✅ LangChain chatbot with RAG
✅ CORS-enabled for frontend integration
✅ Comprehensive error handling
✅ Database migration support

## Next Steps

1. Implement Vue 3 frontend with all features
2. Complete API endpoints for all 18 features
3. Add comprehensive test coverage
4. Deploy to production (Render, AWS, or GCP)
5. Setup CI/CD pipeline with GitHub Actions

## License

Confidential - For Internal Use Only (SE Team 026)

## Contact

For questions or issues, contact SE Team 026 (Syntax Error)
Backend (Flask)
The backend manages the database, search, and AI services.

bash
cd backend
source venv/bin/activate
# Optional: Reset & seed the database
# Start the server
python run.py
API URL: http://localhost:8000
2. Frontend (Vue 3 + Vite)
The frontend provides the user interface.

bash
cd frontend
# Install dependencies (if not already done)
# Start development server
npm run dev
App URL: http://localhost:5173