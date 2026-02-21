import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Lazy-loaded route components
const LandingPage = () => import('@/views/LandingPage.vue')
const LoginPage = () => import('@/views/LoginPage.vue')
const RegisterPage = () => import('@/views/RegisterPage.vue')
const HomePage = () => import('@/views/HomePage.vue')
const EventDetail = () => import('@/views/EventDetail.vue')
const OrganizerDashboard = () => import('@/views/OrganizerDashboard.vue')
const AdminDashboard = () => import('@/views/AdminDashboard.vue')

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: LandingPage,
    meta: { public: true },
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
    meta: { public: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterPage,
    meta: { public: true },
  },
  {
    path: '/home',
    name: 'Home',
    component: HomePage,
    meta: { requiresAuth: true, roles: ['user'] },
  },
  {
    path: '/event/:id',
    name: 'EventDetail',
    component: EventDetail,
    meta: { requiresAuth: true, roles: ['user'] },
  },
  {
    path: '/organizer',
    name: 'OrganizerDashboard',
    component: OrganizerDashboard,
    meta: { requiresAuth: true, roles: ['organizer'] },
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, roles: ['admin'] },
  },
  // Catch-all redirect
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    return { top: 0 }
  },
})

// Navigation guard — role-based access control
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // Public routes — always allow
  if (to.meta.public) {
    // Redirect already-logged-in users from login/register to their dashboard
    if (authStore.isLoggedIn && (to.path === '/login' || to.path === '/register')) {
      return next(authStore.dashboardRoute)
    }
    return next()
  }

  // Protected routes — must be authenticated
  if (!authStore.isLoggedIn) {
    return next('/login')
  }

  // Role check
  const allowedRoles = to.meta.roles || []
  if (allowedRoles.length && !allowedRoles.includes(authStore.role)) {
    return next(authStore.dashboardRoute)
  }

  next()
})

export default router
