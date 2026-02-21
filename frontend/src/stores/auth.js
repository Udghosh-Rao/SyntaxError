import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  // State
  const token = ref(localStorage.getItem('token') || '')
  const userId = ref(localStorage.getItem('userId') || null)
  const role = ref(localStorage.getItem('role') || '')
  const userName = ref(localStorage.getItem('userName') || '')
  const userProfile = ref(null)

  // Computed
  const isLoggedIn = computed(() => !!token.value)

  const dashboardRoute = computed(() => {
    if (role.value === 'organizer') return '/organizer'
    if (role.value === 'admin') return '/admin'
    return '/home'
  })

  // Actions
  function setAuth(data) {
    token.value = data.token
    userId.value = data.user_id
    role.value = data.role
    userName.value = data.name || ''
    localStorage.setItem('token', data.token)
    localStorage.setItem('userId', data.user_id)
    localStorage.setItem('role', data.role)
    localStorage.setItem('userName', data.name || '')
    api.defaults.headers.common['Authorization'] = `Bearer ${data.token}`
  }

  function logout() {
    token.value = ''
    userId.value = null
    role.value = ''
    userName.value = ''
    userProfile.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('userId')
    localStorage.removeItem('role')
    localStorage.removeItem('userName')
    delete api.defaults.headers.common['Authorization']
  }

  async function fetchProfile() {
    try {
      const res = await api.get('/me')
      userProfile.value = res.data
      return res.data
    } catch {
      return null
    }
  }

  // Restore token into axios header on page reload
  if (token.value) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
  }

  return {
    token, userId, role, userName, userProfile,
    isLoggedIn, dashboardRoute,
    setAuth, logout, fetchProfile,
  }
})
