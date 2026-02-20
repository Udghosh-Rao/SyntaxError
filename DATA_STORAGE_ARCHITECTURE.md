# SyntaxError Sports - Data Storage Architecture

## Overview

The SyntaxError Sports Event Management platform uses a comprehensive data storage solution with the following components:

---

## 📊 Database Architecture

### Database Technology
- **SQLAlchemy ORM** - Object-Relational Mapping for Python
- **SQLite (Development)** - Local development database (`dev.db`)
- **PostgreSQL (Production)** - Production-grade relational database

### Database Connection
```
Development: sqlite:///dev.db
Production: ${DATABASE_URL} (Environment Variable)
```

---

## 👥 USER DATA STORAGE

### User Table Structure
```
Table: users
├── id (Primary Key, Integer)
├── name (String, 100 chars, Required)
├── email (String, 150 chars, Unique, Required)
├── password_hash (String, 256 chars, Hashed)
├── role (String, 20 chars) → Values: 'user', 'organizer', 'admin'
├── city (String, 100 chars) → Location preference
├── budget_preference (String, 20) → 'cheap', 'mid', 'premium'
├── preferred_sports (JSON) → Array of sport categories
└── created_at (DateTime, Auto-generated)
```

### User Roles & Permissions

#### 1. **Regular User** (role='user')
- Browse and search events
- Register for events
- View payment history
- Update profile information
- Access to chatbot support

#### 2. **Organizer** (role='organizer')
- Create and manage events
- View event registrations
- Manage event details and pricing
- Send notifications to participants
- View analytics and attendance

#### 3. **Admin** (role='admin')
- Full system access
- Manage all users and organizers
- Approve/reject organizer accounts
- View platform analytics
- Configure system settings
- Manage payment settlements
- Moderate content

### User Password Security
- Passwords hashed using **Werkzeug PBKDF2**
- Never stored in plain text
- Hash verification on login

---

## 🎯 EVENT DATA STORAGE

### Event Table Structure
```
Table: events
├── id (Primary Key)
├── title (String, Required)
├── description (Text)
├── category (String) → 'cricket', 'football', 'badminton', etc.
├── organizer_id (Foreign Key) → Links to User(organizer)
├── location (String)
├── city (String)
├── start_date (DateTime)
├── end_date (DateTime)
├── price (Float) → Entry fee
├── max_participants (Integer)
├── image_url (String) → Event banner/thumbnail
├── status (String) → 'published', 'cancelled', 'completed'
├── created_at (DateTime)
└── updated_at (DateTime)
```

### Event Management
- **Search & Filtering** - Algolia integration for fast searching
- **Pagination** - Handle large event lists
- **Image Storage** - Cloud storage for event images
- **Status Tracking** - Monitor event lifecycle

---

## 💳 PAYMENT DATA STORAGE

### Payment Table Structure
```
Table: payments
├── id (Primary Key)
├── user_id (Foreign Key) → User making payment
├── registration_id (Foreign Key) → Associated registration
├── amount (Float) → Payment amount
├── currency (String) → 'INR', 'USD', etc.
├── payment_method (String) → 'razorpay', 'upi', 'card'
├── payment_id (String) → Razorpay transaction ID
├── status (String) → 'pending', 'completed', 'failed', 'refunded'
├── refund_id (String) → Razorpay refund ID (if applicable)
├── refund_amount (Float) → Amount refunded
├── created_at (DateTime)
└── updated_at (DateTime)
```

### Payment Processing
- **Razorpay Integration** - Secure payment gateway
- **Refund Management** - Track refunds and chargebacks
- **Transaction History** - Complete audit trail
- **Platform Fees** - Configurable commission percentage

---

## 📋 REGISTRATION DATA STORAGE

### Registration Table Structure
```
Table: registrations
├── id (Primary Key)
├── user_id (Foreign Key) → Participant user
├── event_id (Foreign Key) → Registered event
├── registration_date (DateTime)
├── status (String) → 'registered', 'cancelled', 'attended'
├── team_name (String, Optional) → For team events
├── participant_details (JSON) → Additional info
└── cancel_requested (Boolean) → Cancellation flag
```

### Registration Features
- **Participant Management** - Track all registrations
- **Cancellation Handling** - Process refunds
- **Attendance Tracking** - Mark participants as attended
- **Team Registration** - Support for team-based events

---

## 🔗 Database Relationships

```
User (1) ──→ (Many) Events (as organizer)
User (1) ──→ (Many) Registrations
Event (1) ──→ (Many) Registrations
Registration (1) ──→ (1) Payment
User (1) ──→ (Many) Payments
```

---

## 🔐 Data Security & Protection

### Security Measures
1. **Password Hashing** - PBKDF2 with Werkzeug
2. **JWT Authentication** - Secure API access tokens
3. **CORS Protection** - Cross-Origin Resource Sharing configured
4. **SQL Injection Prevention** - SQLAlchemy ORM parameterized queries
5. **Rate Limiting** - API endpoint throttling
6. **HTTPS Only** - Encrypted data transmission
7. **Environment Variables** - Sensitive data not in code

---

## 📂 WHERE DATA IS SAVED

### Development Environment
```
📁 backend/
  ├── app.db (SQLite database file)
  └── Contains all user, event, payment, and registration data
```

### Production Environment
```
☁️ Cloud Database (PostgreSQL)
  └── Connected via DATABASE_URL environment variable
  └── Managed by hosting provider (e.g., Railway, Heroku, AWS RDS)
```

### Admin Data Locations
- **User with role='admin'** → Stored in `users` table
- **Admin Dashboard** → Frontend at `/admin` route
- **Admin Actions** → Logged in audit tables (future)

---

## 🚀 API ENDPOINTS FOR DATA

### Authentication (User Registration & Login)
```
POST   /api/auth/register      → Create new user
POST   /api/auth/login         → Authenticate user
GET    /api/auth/profile       → Get user profile
PUT    /api/auth/profile       → Update user profile
```

### Events (Event Management)
```
GET    /api/events             → List all events
GET    /api/events/<id>        → Get event details
POST   /api/events             → Create event (organizer)
PUT    /api/events/<id>        → Update event
DELETE /api/events/<id>        → Delete event
GET    /api/events/search      → Search with Algolia
```

### Registrations
```
POST   /api/registrations      → Register for event
GET    /api/registrations      → List user registrations
DELETE /api/registrations/<id> → Cancel registration
```

### Payments
```
POST   /api/payments           → Process payment
GET    /api/payments           → Payment history
POST   /api/payments/refund    → Request refund
```

---

## 📊 Data Flow Diagram

```
┌─────────────────┐
│   Frontend      │
│  (Vue.js/React) │
└────────┬────────┘
         │ HTTPS API Calls
         ↓
┌──────────────────────┐
│   Flask Backend      │
│  (Python API Server) │
└────────┬─────────────┘
         │ SQLAlchemy ORM
         ↓
┌──────────────────────┐
│   Database Layer     │
│  SQLite / PostgreSQL │
└──────────────────────┘
         ↓
┌──────────────────────┐
│   Data Tables        │
│  users               │
│  events              │
│  payments            │
│  registrations       │
└──────────────────────┘
```

---

## ⚙️ Configuration Files

### Development Configuration
```
# backend/app/config.py
DEVELOPMENT:
  - SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
  - DEBUG = True
  - TESTING = False
```

### Production Configuration
```
# backend/app/config.py
PRODUCTION:
  - SQLALCHEMY_DATABASE_URI = ${DATABASE_URL}
  - DEBUG = False
  - TESTING = False
```

---

## 🔄 Data Migration & Backup

### Database Migrations (Flask-Migrate)
```bash
# Create migration
flask db migrate -m "Add new column"

# Apply migration
flask db upgrade

# Rollback migration
flask db downgrade
```

### Backup Strategy
1. **Daily Backups** - Automated database dumps
2. **Weekly Archives** - Long-term storage
3. **Point-in-Time Recovery** - PostgreSQL WAL archiving
4. **Disaster Recovery Plan** - Failover procedures

---

## 📈 Data Analytics & Reporting

### Admin Metrics
- Total users registered
- Events created and completed
- Total revenue from payments
- Popular event categories
- User engagement statistics
- Refund rates and patterns

---

## 🛠️ NEXT STEPS TO DEPLOY

1. **Backend Deployment**
   ```bash
   # Deploy Flask backend to Render/Railway/Heroku
   git push heroku main
   ```

2. **Database Setup**
   ```bash
   # Run migrations in production
   flask db upgrade --database-url=$DATABASE_URL
   ```

3. **Connect Frontend to Backend**
   ```typescript
   // Update API_BASE_URL in frontend
   const API_BASE_URL = 'https://your-backend-url.com'
   ```

4. **Test Complete Flow**
   - Register user → Stored in users table
   - Create event → Stored in events table
   - Register for event → Stored in registrations table
   - Process payment → Stored in payments table

---

## 📞 Support & Documentation

For detailed API documentation, see `/backend/docs/API.md`

For database schema details, see `/backend/docs/DATABASE.md`
