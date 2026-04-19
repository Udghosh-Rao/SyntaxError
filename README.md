# ⚽ SyntaxError — Sports Event Management Platform

> **SE Team 026** | Full-Stack MVP | Flask + Vue 3 + Tailwind CSS

# 🏟️ LiveSports — Sports Event Management Platform

A full-stack web application for discovering, managing, and booking sports events. Built with **Vue 3 + TypeScript** on the frontend and a **REST API** backend. Supports three distinct user roles — **User**, **Organizer**, and **Admin** — each with a completely separate experience, dashboard, and set of features.

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Tech Stack](#-tech-stack)
- [Folder Structure](#-folder-structure)
- [User Roles](#-user-roles)
- [Features by Role](#-features-by-role)
  - [All Users (Public)](#all-users-public)
  - [User Role](#user-role)
  - [Organizer Role](#organizer-role)
  - [Admin Role](#admin-role)
- [Pages & Routes](#-pages--routes)
- [Key Components](#-key-components)
- [API Services](#-api-services)
- [Authentication](#-authentication)
- [Payment Integration](#-payment-integration)
- [Referral System](#-referral-system)
- [Wallet System](#-wallet-system)
- [Recommendation Engine](#-recommendation-engine)
- [Chatbot](#-chatbot)
- [Charts & Analytics](#-charts--analytics)
- [Theme System](#-theme-system)
- [State Management](#-state-management)
- [Routing & Guards](#-routing--guards)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)

---

## 🧭 Project Overview

**LiveSports** is a sports event ticketing and management platform that connects three types of users:

- **Users** browse personalized events, purchase tickets via Razorpay or wallet balance, use referral codes for discounts, and track their bookings.
- **Organizers** create and manage events, track registrations, monitor fill rates, and view revenue analytics through interactive dashboards.
- **Admins** have a platform-wide command center with aggregate analytics, organizer leaderboards, and full event control across the entire platform.

All three roles coexist in a single application with role-based routing, a shared navbar, and a floating AI chatbot available on every page.

---

## 🛠️ Tech Stack

### Frontend

| Technology | Purpose |
|---|---|
| **Vue 3** | Core framework (Composition API) |
| **TypeScript** | Type safety across all components and stores |
| **Vite** | Build tool and dev server |
| **Vue Router 4** | Client-side routing with meta-based role guards |
| **Pinia** | Global state management (auth store, events store) |
| **TailwindCSS** | Utility-first CSS framework |
| **Chart.js 4** | All analytics charts (line, bar, donut, etc.) |
| **Axios** | HTTP client with JWT interceptors |
| **Razorpay SDK** | Payment gateway for ticket booking and wallet top-up |
| **motion-v** | Animations and transitions |

### Backend (API)

The frontend communicates with a REST API at the `/api` base URL. All requests are authenticated via JWT Bearer tokens in the `Authorization` header. The backend handles authentication, event management, registrations, payments, wallet operations, admin analytics, chatbot responses, and referral validation.

---

## 📁 Folder Structure

```
se_project/
├── package.json                   # Root scripts (build)
└── frontend/
    ├── index.html
    ├── vite.config.ts
    ├── tsconfig.json
    ├── tailwind.config.js
    ├── postcss.config.js
    ├── .env                       # Environment variables
    └── src/
        ├── main.ts                # App entry point
        ├── App.vue                # Root component (Navbar, Footer, ChatbotWidget)
        ├── assets/
        │   └── index.css          # Global CSS variables (dark/light theme tokens)
        ├── router/
        │   └── index.ts           # All routes with meta (requiresAuth, role, guestOnly)
        ├── stores/
        │   ├── auth.ts            # Pinia auth store (token, role, user object)
        │   └── events.ts          # Pinia events store
        ├── services/
        │   └── api.ts             # Axios instance + all API service functions
        ├── composables/
        │   └── useToast.ts        # Toast notification composable
        ├── types/
        │   └── index.ts           # TypeScript interfaces and types
        ├── views/
        │   ├── LandingPage.vue          # Public homepage (/)
        │   ├── LoginView.vue            # Login + Google OAuth (/login)
        │   ├── RegisterView.vue         # Registration with role selector (/register)
        │   ├── HomePage.vue             # User event feed (/home)
        │   ├── EventDetail.vue          # Full event + booking flow (/events/:id)
        │   ├── MyRegistrations.vue      # User's booked events (/my-registrations)
        │   ├── UserDashboardView.vue    # Referral dashboard (/dashboard)
        │   ├── WalletView.vue           # Wallet balance + transactions (/wallet)
        │   ├── ProfileView.vue          # Edit profile + referral code (/profile)
        │   ├── OrganizerDashboard.vue   # Organizer analytics (/organizer)
        │   ├── OrganizerDashboardView.vue # Alternate organizer analytics
        │   ├── OrganizerEventsView.vue  # Organizer event list (/organizer/events)
        │   ├── CreateEvent.vue          # Create event form (/organizer/create)
        │   ├── EditEvent.vue            # Edit event form (/organizer/edit/:id)
        │   ├── AdminDashboard.vue       # Admin command center (/admin)
        │   ├── AdminEventForm.vue       # Admin create/edit events (/admin/events/*)
        │   └── UserEventsView.vue       # Browse all events (/events)
        └── components/
            ├── ChatbotWidget.vue             # Floating AI chatbot (all pages)
            ├── RecommendationRow.vue         # Infinite event slider
            ├── EventCard.vue                 # Single event preview card
            ├── GoogleOnboarding.vue          # Post-Google-login onboarding modal
            ├── ToastNotification.vue         # Global toast system
            ├── BarChart.vue                  # Generic bar chart wrapper
            ├── payment/
            │   └── RazorpayCheckout.vue      # Razorpay modal integration
            └── charts/
                ├── RegistrationTrend.vue     # Line chart: registrations over time
                ├── CategoryBarChart.vue      # Bar chart: sport categories
                ├── CapacityChart.vue         # Capacity vs registrations
                ├── FillRateChart.vue         # Fill rate bar chart
                ├── FillRateTable.vue         # Fill rate as table
                ├── MonthlyTrendChart.vue     # Monthly revenue/registration trend
                ├── SportDonutChart.vue       # Donut: most popular sports
                ├── CityDistributionChart.vue # City-wise event breakdown
                ├── OrganizerComparisonChart.vue  # Organizer revenue comparison
                └── RevenuePerEventChart.vue  # Revenue breakdown per event
```

---

## 👥 User Roles

The platform has three roles. Each role gets its own routing, dashboard, and feature set.

| Role | How Created | Default Redirect After Login |
|---|---|---|
| **User** | Public registration (`/register` → role: user) or Google OAuth | `/home` |
| **Organizer** | Public registration (`/register` → role: organizer) | `/organizer` |
| **Admin** | Provisioned directly via backend (not via UI) | `/admin` |

> **Note:** There is also a `founder` role in the auth store which is treated as a super-organizer with the same access as an organizer.

---

## ✅ Features by Role

### All Users (Public)

- **Landing Page** — animated hero with container scroll effect, feature cards, footer with Terms and Privacy Policy.
- **Register** — choose role (User or Organizer), sport preferences selection for users.
- **Login** — email/password with show/hide toggle, Google OAuth single sign-on.
- **Dark / Light Mode** — system-wide theme toggle in the navbar, persisted across sessions.
- **Floating Chatbot** — always visible at bottom-right, accessible before and after login.

---

### User Role

#### 🏠 Home Page (`/home`)
- **Curated For You** section — personalized events recommended based on sport preferences selected at registration.
- **Search bar** — real-time search by event name, city, or sport category.
- **Budget filter** — General Admission (< ₹500), VIP Access (₹500–₹2000), Backstage Pass (> ₹2000).
- Events displayed as interactive cards showing sport, city, date, price, and seats remaining.

#### 🎟️ Event Detail Page (`/events/:id`)
- Sport badge, event title, Access Tier label, venue city, full address, and event date.
- Event description block.
- Live stats: Ticket Price and Seats Remaining out of total capacity.
- **Real-time polling**: page re-fetches event data every 30 seconds to keep seat count live.
- **Registration Form** (logged-in users only):
  - Role selector: Athlete/Fan or Service Provider (Referee / Medical / Sub-vendor).
  - If Service Provider: dropdown for service type (Catering, Medical, Audio/Lighting).
  - If Athlete: optional Squad/Crew name field.
  - **Referral Code** field with debounced real-time validation (600ms delay) — shows ✓ or ✗ inline.
  - **Wallet toggle** — if the user has wallet balance, they can apply it to reduce the amount due.
  - **Price Summary breakdown**: Base Price → Referral Discount (5%) → Wallet Credit → Final Amount.
  - Book button text is dynamic: "Register Free" when final price is ₹0, otherwise "Pay ₹X".
- **Payment flow**: paid events go through Razorpay checkout modal. On success, ticket is confirmed instantly.
- **Payment failure handling**: if Razorpay fails, registration is marked `payment_failed` and wallet amount is automatically refunded.
- **Cancel Ticket**: confirmed bookings show a cancel button with an inline confirmation prompt. On cancel, the refund is applied immediately to wallet balance and the navbar wallet badge updates live.
- **Pending payment state**: if payment is initiated but not completed, a "Payment Pending" state appears with a Retry button.
- **Sold Out state**: when seats run out, a "Gate Closed — Sold Out" banner replaces the booking form.
- **Similar Events**: recommendation row at the bottom showing related events by sport category.

#### 📋 My Registrations (`/my-registrations`)
- Lists all events the user has registered for.
- Status badges per registration: `confirmed` (green), `cancelled` (red).

#### 📊 User Dashboard (`/dashboard`)
- Shows the user's personal **Referral Code** with a one-click copy button.
- Stats: Total Referrals made, Total Referral Earnings (in ₹).
- List of people who joined using the user's referral code — name and join date.

#### 🪙 Wallet (`/wallet`)
- Current wallet balance displayed prominently.
- **Add Funds** panel: quick-select preset amounts or custom input → Razorpay payment → verified and credited.
- **Transaction History**: full list of all debits and credits with timestamps.
- Summary stats: total money added vs. total spent.
- Wallet balance is also visible in the navbar profile dropdown and updates live via a custom browser event (`wallet-updated`).

#### 👤 Profile (`/profile`)
- Edit name, email, and other personal details.
- **Referral Code display** with clipboard copy — share to earn wallet credits.

---

### Organizer Role

#### 📊 Organizer Dashboard (`/organizer`)
The main dashboard shows two sections side by side:

**Platform Overview KPIs** (from admin API):
- Total Users on platform
- Total Events on platform
- Total Registrations on platform
- Most Popular Sport on platform

**My Events KPIs**:
- Total Capacity (across all organizer events)
- Total Registrations (across all organizer events)
- Aggregate Fill Rate (%)
- Total Revenue (₹)

**Charts**:
- **Registration Trend** — line chart; select any event from dropdown to see how registrations grew over time.
- **Category Breakdown** — bar chart showing sport category distribution of the organizer's attendees.

#### 📅 Organizer Events (`/organizer/events`)
- Table of all events the organizer has created.
- Columns: Title, Date, City, Registrations, Capacity, Revenue (₹), Performance Label, Actions.
- **Performance Label badge**: color-coded (e.g., Hot, Good, Low) based on fill rate.
- Cancelled events show a "Cancelled" badge and the Edit button is disabled.
- Action buttons: **View** (opens event detail page), **Edit** (opens edit form).
- **Create Event** button links to `/organizer/create`.

#### ➕ Create Event (`/organizer/create`)
Form fields:
- Event Title (required)
- Description (textarea)
- Date & Time (datetime-local picker, required)
- Entry Fee in ₹ (min: 0 for free events)
- City and Venue Address
- Sport Category (dropdown: Football, Basketball, Cricket, Tennis, Badminton, Athletics, Swimming, Cycling, Others)
- Max Participants / Capacity (required)

#### ✏️ Edit Event (`/organizer/edit/:id`)
Same form as Create, pre-populated with existing event data. Updates are sent via `PUT /events/:id`.

---

### Admin Role

#### 🖥️ Admin Dashboard (`/admin`)

Two tabs: **Analytics** and **Events**.

**Analytics Tab**

Platform-wide stats (top KPI cards):
- Total Users
- Total Events
- Total Revenue (₹)

Five analytics charts displayed in a grid:
1. **Monthly Trend Chart** — line chart of registrations/revenue month over month.
2. **Sport Donut Chart** — which sports are most popular by registration count.
3. **City Distribution Chart** — how events and attendees are spread across cities.
4. **Fill Rate Chart** — bar chart showing each event's fill rate.
5. **Organizer Comparison Chart** — bar chart comparing organizers by revenue.

**Organizer Leaderboard Table**: Organizer Name, Total Events, Total Revenue — sorted by performance.

**Re-Sync Platform button** — manually triggers a fresh data fetch for all analytics.

**Events Tab**
- Full table of every event across the entire platform.
- Columns: Title, Organizer ID, Sport Category, City, Date, Capacity, Price.
- **Search bar** — filter by title, city, or sport in real time.
- Edit button per event → navigates to Admin Event Form in edit mode.
- Cancelled/deleted events show a disabled Edit button.
- **Create Event button** → Admin Event Form in create mode.

#### 📝 Admin Event Form (`/admin/events/create` and `/admin/events/edit/:id`)
Same fields as the Organizer create form, plus:
- **Organizer User ID** field — admins can assign an event to any organizer by ID.
- **Banner URL** field — link to the event's banner/cover image.

---

## 🛣️ Pages & Routes

| Path | View | Access |
|---|---|---|
| `/` | LandingPage | Public |
| `/login` | LoginView | Guest only |
| `/register` | RegisterView | Guest only |
| `/home` | HomePage | Authenticated |
| `/events` | UserEventsView | Authenticated |
| `/events/:id` | EventDetail | Public |
| `/my-registrations` | MyRegistrations | User only |
| `/dashboard` | UserDashboardView | Authenticated |
| `/wallet` | WalletView | Authenticated |
| `/profile` | ProfileView | Authenticated |
| `/organizer` | OrganizerDashboard | Organizer only |
| `/organizer/events` | OrganizerEventsView | Organizer only |
| `/organizer/create` | CreateEvent | Organizer only |
| `/organizer/edit/:id` | EditEvent | Organizer only |
| `/organizer/analytics` | OrganizerDashboardView | Organizer only |
| `/admin` | AdminDashboard | Admin only |
| `/admin/events/create` | AdminEventForm | Admin only |
| `/admin/events/edit/:id` | AdminEventForm | Admin only |

Routes with `meta: { requiresAuth: true }` redirect to `/login` if the user is not authenticated.  
Routes with `meta: { guestOnly: true }` redirect to the user's dashboard if already logged in.  
Routes with `meta: { role: 'organizer' }` redirect unauthorized roles away from organizer pages.

---

## 🧩 Key Components

### `App.vue` — Root Layout
- **Navbar**: floating pill-style navbar at the top. Shows role-aware links in the profile dropdown.
  - **Theme Toggle**: dark/light mode button.
  - **Profile Dropdown**: shows avatar (first letter of name), display name, email, role-specific links (Home, Profile, Wallet for users, Events, Dashboard, Logout).
  - **Wallet Badge**: live wallet balance shown in the dropdown for users, updates via `wallet-updated` custom event.
- **Footer**: platform description, Terms of Service, Privacy Policy.
- **ChatbotWidget**: always rendered at root level so it persists across all page navigations.
- **ToastNotification**: global toast container.
- Handles `auth-expired` event (fired by Axios interceptor on 401) to auto-logout users.

### `ChatbotWidget.vue`
- **Floating Action Button (FAB)**: fixed at bottom-right, glowing on hover.
- **Chat Window**: 340px wide, 520px max height, scrollable message list.
- **Session ID**: unique per browser tab (`session_${Date.now()}_${random}`), sent with every message for conversation continuity.
- **Quick Suggestions**: four preset chips shown only at the start of a conversation.
- **Typing Indicator**: animated three-dot bounce while waiting for bot response.
- **Escalation**: if the bot cannot resolve an issue, response includes an escalation flag and shows "⚠ Transferred to a human agent".
- **Clear Chat**: trash icon in header resets to the initial greeting.
- Sends JWT token in `Authorization` header if user is logged in.
- Respects dark and light theme.

### `RecommendationRow.vue`
- Infinite-loop horizontal event slider with left/right arrow navigation and dot indicators.
- Events are duplicated internally to create a seamless infinite loop effect.
- Smooth `cubic-bezier` CSS transition on track movement.
- Badge shows "✨ Personalized for You" for authenticated users, "🔥 Trending Now" for guests.

### `GoogleOnboarding.vue`
- Full-screen overlay modal triggered after a new user signs in via Google OAuth.
- **Step 1**: role selection — User ("Browse Events") or Organizer ("Host Events").
- **Step 2**: sport preferences — grid of sport buttons with emoji; multiple selections allowed; supports custom tags via "Others" option.
- On submit, posts to `/api/auth/oauth/google/complete` and redirects to the appropriate dashboard.

### `RazorpayCheckout.vue`
- Modal component that initializes the Razorpay payment widget.
- Accepts order data from the backend (`order_id`, `amount`, `currency`, `key`).
- Emits `success`, `cancel`, and `error` events back to the parent (EventDetail or WalletView).

### `ToastNotification.vue`
- Composable `useToast()` provides `toast.success()`, `toast.error()`, `toast.info()` methods.
- Toasts appear as sliding notifications and auto-dismiss.

---

## 🔌 API Services

All API calls are defined in `src/services/api.ts` using an Axios instance with baseURL `/api`.

```
userApi       → /auth/login, /auth/register, /auth/me, /users/*
eventApi      → /events, /events/:id (CRUD)
registrationApi → /registrations/my, /registrations (create), /registrations/:id/cancel
paymentApi    → /payments/create-order, /payments/fail
adminApi      → /admin/dashboard, /admin/monthly-trend, /admin/city-distribution,
                /admin/fill-rate, /admin/organizer-performance, /admin/popular-sport,
                /admin/events
organizerApi  → /organizer/dashboard, /organizer/category-insight,
                /organizer/events/:id/feature, /organizer/trend/:id
walletApi     → /wallet, /wallet/add-funds, /wallet/verify-topup
referralApi   → /registrations/validate-referral, /auth/my-referrals
chatbotApi    → /chatbot (POST with { message, session_id })
```

---

## 🔐 Authentication

- **JWT-based**: token stored in `localStorage` under `auth_token`. Role stored under `user_role`.
- **Axios request interceptor**: automatically attaches `Authorization: Bearer <token>` to every API request.
- **Axios response interceptor**: on HTTP 401, clears localStorage and fires an `auth-expired` browser event. `App.vue` listens for this event and logs the user out.
- **Pinia `authStore`**: holds `token`, `role`, `userId`, `userObj`. Computed properties: `isAuthenticated`, `isAdmin`, `isOrganizer`, `isUser`, `isFounder`.
- **Google OAuth**: uses Google Identity Services (`google.accounts.id`). On successful sign-in, the JWT credential is sent to `/api/auth/oauth/google`. New users are detected and shown the `GoogleOnboarding` modal.

---

## 💳 Payment Integration

Razorpay is used in two places:

**1. Ticket Booking (EventDetail)**
- User fills the registration form and clicks "Pay ₹X".
- Frontend calls `POST /payments/create-order` with `event_id`, `referral_code`, and `wallet_used` amount.
- Backend returns a Razorpay order object.
- `RazorpayCheckout.vue` opens the Razorpay modal with the order details.
- On success: `handlePaymentSuccess()` confirms the booking, updates wallet balance.
- On cancel (modal closed without payment): booking stays in `pending` state, no wallet deduction, no error.
- On failure: `POST /payments/fail` is called to reset registration to `payment_failed` and refund any wallet deduction.

**2. Wallet Top-up (WalletView)**
- User enters amount and clicks "Pay ₹X".
- Frontend calls `POST /wallet/add-funds`.
- Backend returns a Razorpay order.
- On payment success: `POST /wallet/verify-topup` is called with the Razorpay signature for server-side verification.
- Wallet balance is refreshed and navbar badge updates.

---

## 🎁 Referral System

Every user gets a unique referral code displayed on their Profile page and User Dashboard.

**How it works:**
- User A shares their referral code with User B.
- User B enters the code in the referral field while booking an event.
- The code is validated in real time via `POST /registrations/validate-referral`.
- If valid: User B gets **5% discount** on the ticket price, shown in the price breakdown.
- User A earns **5% of the ticket price** credited to their wallet as a reward.
- Referral discounts are **non-refundable** if the ticket is later cancelled.
- Referral earnings are tracked in the User Dashboard under "Referral Earnings".

---

## 🪙 Wallet System

- Every user has a wallet with a rupee balance.
- **Funding**: add money via Razorpay payment verified server-side.
- **Spending**: during ticket booking, users can toggle "Use Wallet Balance". The wallet covers as much of the total as possible; the remainder is paid via Razorpay.
- **Refunds**: cancelled tickets refund the wallet portion to the user's wallet instantly.
- **Live balance**: the navbar profile dropdown shows the wallet balance. It updates without a page reload using a custom browser event (`wallet-updated`) dispatched after any wallet-modifying operation.
- **Transaction History**: the Wallet page shows every credit and debit with a count summary.

---

## 🤖 Recommendation Engine

Two types of recommendations appear in the app:

**1. "Curated For You" (Home Page)**
- Shown only to authenticated users with the `user` role.
- Based on `preferred_sports` saved at registration or Google onboarding.
- Powered by `RecommendationRow` component hitting the recommendations API endpoint.

**2. "Similar Events You'll Love" (Event Detail Page)**
- Shown at the bottom of any event detail page.
- Passes the current `eventId` to `RecommendationRow` which fetches related events by sport category.

For unauthenticated visitors, the slider shows a generic "🔥 Trending Now" row instead.

---

## 💬 Chatbot

- Available on **every page** as a fixed floating button at the bottom-right corner.
- **Session tracking**: generates a unique `session_id` per browser tab to maintain conversation history within a session.
- **Quick suggestions**: 4 preset question chips shown at the start: "How do I register for an event?", "What payment methods are accepted?", "Show me upcoming events", "How do I cancel my registration?"
- **Send on Enter**: pressing Enter in the input sends the message.
- **Typing indicator**: three bouncing dots shown while awaiting the API response.
- **Escalation**: complex queries trigger an escalation flag in the response, and the chat shows "⚠ Transferred to a human agent".
- **Clear Chat**: resets conversation to the initial greeting message.
- **Auth-aware**: sends `Authorization: Bearer <token>` if user is logged in so the chatbot can give personalized responses.

---

## 📊 Charts & Analytics

All charts are built with **Chart.js 4** and wrapped in Vue components.

| Component | Chart Type | Used In |
|---|---|---|
| `MonthlyTrendChart` | Line | Admin Dashboard |
| `SportDonutChart` | Doughnut | Admin Dashboard |
| `CityDistributionChart` | Bar | Admin Dashboard |
| `FillRateChart` | Bar | Admin Dashboard |
| `OrganizerComparisonChart` | Bar | Admin Dashboard |
| `RegistrationTrend` | Line | Organizer Dashboard |
| `CategoryBarChart` | Bar | Organizer Dashboard |
| `CapacityChart` | Bar | Organizer Dashboard |
| `RevenuePerEventChart` | Bar | Organizer Dashboard |
| `FillRateTable` | Table | Organizer Dashboard |

---

## 🎨 Theme System

The app supports full dark and light mode via CSS custom properties defined in `src/assets/index.css`.

- A `data-theme` attribute (`"dark"` or `"light"`) is set on the `<html>` element.
- All components use CSS variables like `var(--bg-site)`, `var(--text-primary)`, `var(--brand-accent)`, `var(--border-subtle)` etc.
- The toggle button is in the navbar and persists the preference.
- Brand colors: **lime green** (`#ccff00`) as primary accent, **cyan** (`#00f3ff`) as secondary accent, **hot pink** (`#ff007f`) for alerts and highlights.

---

## 🗃️ State Management

Two Pinia stores:

**`authStore` (`src/stores/auth.ts`)**
- `token` — JWT access token
- `role` — user role string (`'user'`, `'organizer'`, `'admin'`, `'founder'`)
- `userId` — logged-in user's ID
- `userObj` — full user profile object (name, email, referral_code, etc.)
- `isAuthenticated`, `isAdmin`, `isOrganizer`, `isUser`, `isFounder` — computed booleans
- `register()`, `login()`, `logout()`, `fetchUser()` — async actions

**`eventsStore` (`src/stores/events.ts`)**
- Caches event list data to avoid redundant API calls.

---

## 🔒 Routing & Guards

Defined in `src/router/index.ts` with `beforeEach` navigation guards:

- `meta: { requiresAuth: true }` — redirects unauthenticated users to `/login`.
- `meta: { guestOnly: true }` — redirects already-authenticated users to their dashboard.
- `meta: { role: 'organizer' }` — redirects non-organizer roles away.
- `meta: { role: 'admin' }` — redirects non-admin roles away.
- After login, users are redirected based on role: Admin → `/admin`, Organizer → `/organizer`, User → `/home`.

---

## 🚀 Getting Started

### Prerequisites
- Node.js 18.x
- npm

### Installation

```bash
# Install root dependencies
npm install

# Install frontend dependencies
cd frontend
npm install
```

### Development

```bash
cd frontend
npm run dev
```

The app runs at `http://localhost:3000` 

### Build for Production

```bash
# From root
npm run build

# Or from frontend/
npm run build
```

### Lint

```bash
cd frontend
npm run lint
```

---

## 🔧 Environment Variables

Create a `.env` file in `frontend/` (see `.env.example`):

```env
# Backend API base URL (default: /api — works via Vite proxy in dev)
VITE_API_BASE_URL=/api

# Google OAuth Client ID (required for Google Sign-In)
VITE_GOOGLE_CLIENT_ID=your_google_client_id_here
```

> If `VITE_GOOGLE_CLIENT_ID` is missing, the "Continue with Google" button will show an error message and Google sign-in will be disabled.

---

## 📝 Notes

- The **Admin role** cannot be created via the public registration form. Admin accounts must be provisioned directly in the backend database or via a backend admin script.
- The **Founder role** is treated identically to Organizer in the frontend (`isOrganizer` computed returns `true` for both `'organizer'` and `'founder'`).
- Event data on the Event Detail page is **polled every 30 seconds** to keep seat counts live without requiring a manual refresh.
- The wallet balance in the navbar updates **instantly** (without a page reload) after any transaction, using a custom browser `wallet-updated` event dispatched from child components and listened to in `App.vue`.
- All payment flows are secured with Razorpay signature verification on the backend before confirming a booking or wallet top-up.
