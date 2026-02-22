# EventHub - Frontend

A Vue 3 + TypeScript + Pinia based Sports Event Management System frontend application.

## Project Structure

```
src/
├── components/          # Reusable Vue components
│   ├── ChatInterface.vue
│   ├── EventDetail.vue
│   ├── EventList.vue
│   ├── Header.vue
│   ├── Footer.vue
│   ├── EventCard.vue
│   └── UserProfile.vue
├── composables/         # Vue composition API hooks
│   ├── useAuth.ts
│   ├── useEvent.ts
│   └── useUser.ts
├── stores/              # Pinia stores for state management
│   ├── auth.ts
│   ├── events.ts
│   └── index.ts
├── services/            # API services
│   └── api.ts
├── types/               # TypeScript type definitions
│   └── index.ts
├── router/              # Vue Router configuration
│   └── index.ts
├── views/               # Page components
│   ├── Home.vue
│   ├── EventDetail.vue
│   ├── OrganizerDashboard.vue
│   ├── AdminDashboard.vue
│   ├── Registration.vue
│   └── Payment.vue
├── App.vue              # Root component
└── main.ts              # Application entry point
```

## Features

- **Authentication**: User login, registration, and role-based access (user, organizer, admin)
- **Event Management**: Browse, create, and manage events
- **Event Registration**: Register for events and manage registrations
- **Payment Integration**: Razorpay payment gateway integration
- **Admin Dashboard**: Manage users and payments
- **Organizer Dashboard**: Create and manage events with analytics
- **Real-time Chat**: AI-powered event assistance chatbot

## Technology Stack

- **Vue 3**: Progressive JavaScript framework
- **TypeScript**: Type-safe JavaScript
- **Pinia**: State management
- **Vue Router**: Client-side routing
- **Axios**: HTTP client
- **Vite**: Fast build tool and dev server
- **Razorpay**: Payment processing

## Installation

```bash
# Install dependencies
npm install

# Create .env.local from .env.example
cp .env.example .env.local
```

## Environment Variables

Create a `.env.local` file with the following variables:

```
VITE_API_BASE_URL=http://localhost:3000/api
VITE_RAZORPAY_KEY=your_razorpay_key
VITE_ALGOLIA_APP_ID=your_algolia_app_id
VITE_ALGOLIA_SEARCH_KEY=your_algolia_search_key
```

## Development

```bash
# Run development server
npm run dev

# Run type checking
npm run type-check

# Build for production
npm run build

# Preview production build
npm run preview
```

## Usage

### User Workflows

1. **Browse Events**: Visit home page to view featured events
2. **Search Events**: Use search/filter to find specific events
3. **Register**: Click register on any event and complete registration form
4. **Payment**: Complete payment via Razorpay
5. **Manage Registrations**: View registered events in dashboard

### Organizer Workflows

1. **Create Event**: Navigate to organizer dashboard
2. **Manage Event**: Edit event details, view registrations
3. **Analytics**: View event statistics (attendees, revenue)

### Admin Workflows

1. **User Management**: View and manage all users
2. **Payment Monitoring**: Track all payments and transactions
3. **System Control**: Manage platform settings

## API Integration

The application integrates with a REST API backend at `VITE_API_BASE_URL`. Key endpoints:

- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /events` - List all events
- `GET /events/:id` - Get event details
- `POST /events/:id/register` - Register for event
- `POST /payments` - Process payment
- `GET /users` - List users (admin)
- `GET /payments` - List payments (admin)

## State Management (Pinia)

### Auth Store

```typescript
// Authentication and user state
- currentUser
- isAuthenticated
- login()
- logout()
- register()
```

### Events Store

```typescript
// Event management state
- events
- selectedEvent
- fetchEvents()
- getEventById()
- registerForEvent()
- unregisterFromEvent()
```

## Components

### Header Component
Navigation bar with logo, menu, and user actions (login/logout)

### Footer Component
Footer with links and company information

### EventCard Component
Displays event summary card with image, title, date, location

### EventList Component
Lists events with search and filtering capabilities

### EventDetail Component
Detailed event information with registration functionality

### ChatInterface Component
AI-powered chatbot for event assistance

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

MIT
