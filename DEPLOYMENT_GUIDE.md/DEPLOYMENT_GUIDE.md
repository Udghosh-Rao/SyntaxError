# SyntaxError Sports - Complete Deployment Guide

## 🚀 FULL STACK DEPLOYMENT WITH DATABASE

This guide will help you deploy the complete SyntaxError Sports Event Management platform with:
- ✅ Frontend (Vue.js) on Vercel
- ✅ Backend (Flask) on Render
- ✅ Database (PostgreSQL) on Render
- ✅ Admin/User/Vendor Management System

---

## 📋 Prerequisites

1. GitHub Account (already have)
2. Vercel Account (already set up)
3. Render Account (create at https://render.com)
4. Your backend is ready in `backend/` folder

---

## 🗄️ STEP 1: Setup PostgreSQL Database on Render

### 1.1 Create Database

1. Go to https://render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - Name: `syntaxerror-db`
   - Database: `syntaxerror`
   - User: (auto-generated)
   - Region: Singapore (closest to Jaipur)
   - Plan: Free
4. Click **"Create Database"**

### 1.2 Get Database URL

After creation, copy the **Internal Database URL**:
```
postgresql://user:password@hostname/database
```

Save this for Step 2.

---

## 🐍 STEP 2: Deploy Backend to Render

### 2.1 Create Web Service

1. In Render Dashboard, click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `23f1000932/SyntaxError`
3. Configure:
   - Name: `syntaxerror-backend`
   - Region: Singapore
   - Branch: `main`
   - Root Directory: `backend`
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn run:app`
   - Plan: Free

### 2.2 Add Environment Variables

In **Environment** tab, add:

```bash
FLASK_ENV=production
DATABASE_URL=<your-render-postgres-url-from-step-1>
JWT_SECRET_KEY=your-super-secret-key-change-this
RAZORPAY_KEY_ID=your_razorpay_key
RAZORPAY_KEY_SECRET=your_razorpay_secret
```

### 2.3 Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Your backend URL will be: `https://syntaxerror-backend.onrender.com`

### 2.4 Initialize Database

After deployment, open **Shell** tab and run:
```bash
python
>>> from app.extensions import db
>>> from app import create_app
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
...     print("Database initialized!")
>>> exit()
```

---

## 🎨 STEP 3: Update Frontend with Backend URL

### 3.1 Update API Service

In `frontend/src/services/api.ts`, change the base URL:

```typescript
const api = axios.create({
  baseURL: 'https://syntaxerror-backend.onrender.com/api',  // Your Render backend URL
  headers: {
    'Content-Type': 'application/json'
  }
});
```

### 3.2 Commit Changes

```bash
git add frontend/src/services/api.ts
git commit -m "feat: Connect frontend to production backend"
git push origin main
```

### 3.3 Vercel Auto-Deploy

Vercel will automatically redeploy with the new backend connection!

---

## 👤 STEP 4: Create Admin Account

### 4.1 Via Backend Shell

In Render backend Shell:

```python
from app.extensions import db
from app.models.user import User
from app import create_app

app = create_app()
with app.app_context():
    admin = User(
        username='admin',
        email='admin@syntaxerror.com',
        role='admin'
    )
    admin.set_password('Admin@123')
    db.session.add(admin)
    db.session.commit()
    print("Admin created!")
```

### 4.2 Login Credentials

```
Username: admin
Password: Admin@123
Role: Admin
```

---

## 🎯 STEP 5: Test Complete System

### 5.1 Test Login
1. Go to: https://syntax-error-ashy.vercel.app/login
2. Login with admin credentials
3. Should redirect to Admin Dashboard

### 5.2 Test Registration
1. Go to: https://syntax-error-ashy.vercel.app/register
2. Create a user account
3. Create an organizer account
4. Verify both roles work

### 5.3 Test Admin Functions
- View all users
- Manage events
- View payments
- Analytics dashboard

---

## 📊 ADMIN/USER/VENDOR MANAGEMENT

### Admin Can:
✅ View all users, organizers, and vendors
✅ Approve/reject vendor applications
✅ Manage all events (create, edit, delete)
✅ View all payments and refunds
✅ Ban/unban users
✅ View analytics and reports

### Organizers/Vendors Can:
✅ Create and manage their own events
✅ View registrations for their events
✅ Process refunds
✅ View their revenue analytics

### Regular Users Can:
✅ Browse and search events
✅ Register for events
✅ Make payments
✅ View their registration history
✅ Chat with event assistant

---

## 🔐 SECURITY CONFIGURATION

### Update JWT Secret

In Render environment variables:
```bash
JWT_SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
```

### Enable CORS

Backend already configured with CORS for Vercel domain.

---

## 🌐 FINAL URLS

**Frontend (Vercel):**
```
https://syntax-error-ashy.vercel.app
```

**Backend (Render):**
```
https://syntaxerror-backend.onrender.com
```

**Database (Render):**
```
Managed via Render Dashboard
```

---

## 📱 TESTING CHECKLIST

- [ ] Frontend loads on Vercel
- [ ] Backend health check: `https://syntaxerror-backend.onrender.com/health`
- [ ] Database connection works
- [ ] Admin login works
- [ ] User registration works
- [ ] Organizer registration works
- [ ] Event creation works
- [ ] Payment processing works (test mode)
- [ ] Search functionality works
- [ ] All dashboards accessible

---

## 🚨 TROUBLESHOOTING

### Backend won't start
- Check Render logs
- Verify all environment variables are set
- Check database URL is correct

### Database connection fails
- Verify DATABASE_URL in environment variables
- Check database is running in Render
- Run migrations

### Frontend can't connect to backend
- Check CORS configuration
- Verify backend URL in api.ts
- Check backend is deployed and running

---

## 📝 NEXT STEPS AFTER DEPLOYMENT

1. **Create Sample Data:**
   - Add some test events
   - Create sample users
   - Test payment flow

2. **Configure Razorpay:**
   - Get production API keys
   - Update environment variables
   - Test payment flow

3. **Custom Domain (Optional):**
   - Buy domain
   - Configure in Vercel
   - Update backend CORS

4. **Monitoring:**
   - Set up Render alerts
   - Monitor database usage
   - Track API performance

---

## ✅ PROJECT STATUS

### Completed:
- ✅ Full authentication system (JWT)
- ✅ Role-based access control (Admin/Organizer/User)
- ✅ Database models (User, Event, Registration, Payment)
- ✅ Frontend UI (Login, Register, Dashboards)
- ✅ Backend API endpoints
- ✅ Search and filtering
- ✅ Payment integration structure

### Ready for Production:
- ✅ Frontend deployed on Vercel
- ⏳ Backend deployment (follow Step 2)
- ⏳ Database setup (follow Step 1)
- ⏳ Admin account creation (follow Step 4)

---

## 🎉 CONGRATULATIONS!

Your complete full-stack application with admin/user/vendor management is ready for deployment!

**Support:** Create an issue on GitHub if you face any problems.

**Created by:** SyntaxError Team
**Date:** February 20, 2026
