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
      path: '/admin',
      name: 'admin',
      component: () => import('../views/AdminDashboard.vue'),
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
  } else if (to.meta.role && to.meta.role !== userRole) {
    // Role mismatch (e.g. user trying to access admin dashboard)
    next('/')
  } else {
    next()
  }
})

export default router
