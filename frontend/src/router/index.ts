import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: () => import('../views/LandingPage.vue')
    },
    {
      path: '/home',
      name: 'home',
      component: () => import('../views/HomePage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/organizer',
      name: 'organizer',
      component: () => import('../views/OrganizerDashboard.vue'),
      meta: { requiresAuth: true, role: 'organizer' }
    },
    {
      path: '/organizer/create',
      name: 'create-event',
      component: () => import('../views/CreateEvent.vue'),
      meta: { requiresAuth: true, role: 'organizer' }
    },
    {
      path: '/organizer/edit/:id',
      name: 'edit-event',
      component: () => import('../views/EditEvent.vue'),
      meta: { requiresAuth: true, role: 'organizer' }
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/AdminDashboard.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/admin/events/create',
      name: 'admin-create-event',
      component: () => import('../views/AdminEventForm.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/admin/events/edit/:id',
      name: 'admin-edit-event',
      component: () => import('../views/AdminEventForm.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { guestOnly: true }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
      meta: { guestOnly: true }
    },
    {
      path: '/events/:id',
      name: 'event-detail',
      component: () => import('../views/EventDetail.vue')
    },
    {
      path: '/my-registrations',
      name: 'my-registrations',
      component: () => import('../views/MyRegistrations.vue'),
      meta: { requiresAuth: true, role: 'user' }
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/wallet',
      name: 'wallet',
      component: () => import('../views/WalletView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/events',
      name: 'user-events',
      component: () => import('../views/UserEventsView.vue'),
      meta: { requiresAuth: true, role: 'user' }
    },
    {
      path: '/organizer/events',
      name: 'organizer-events',
      component: () => import('../views/OrganizerEventsView.vue'),
      meta: { requiresAuth: true, role: 'organizer' }
    },
    {
      path: '/dashboard',
      name: 'user-dashboard',
      component: () => import('../views/UserDashboardView.vue'),
      meta: { requiresAuth: true, role: 'user' }
    },
    {
      path: '/organizer/analytics',
      name: 'organizer-analytics',
      component: () => import('../views/OrganizerDashboardView.vue'),
      meta: { requiresAuth: true, role: 'organizer' }
    }
  ]
})

router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = !!authStore.token
  const userRole = authStore.role

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.meta.guestOnly && isAuthenticated) {
    if (userRole === 'admin') next('/admin')
    else if (userRole === 'organizer') next('/organizer')
    else next('/home')
  } else if (to.meta.role && to.meta.role !== userRole && userRole !== 'admin') {
    // Role mismatch — admin can access anything
    next('/')
  } else {
    next()
  }
})

export default router