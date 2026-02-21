<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-12">
    <div class="w-full max-w-sm">
      <!-- Logo -->
      <router-link to="/" class="flex items-center justify-center gap-2 mb-8 text-gray-900 hover:text-gray-700 transition">
        <span class="font-bold text-lg">SportsSync</span>
      </router-link>

      <div class="bg-white rounded-2xl border border-gray-100 shadow-card p-8">
        <h1 class="text-xl font-bold text-gray-900 mb-1">Welcome back</h1>
        <p class="text-sm text-gray-500 mb-6">Sign in to your account</p>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-xs font-medium text-gray-700 mb-1.5">Email address</label>
            <input v-model="form.email" type="email" class="input" placeholder="you@example.com" required />
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-700 mb-1.5">Password</label>
            <input v-model="form.password" type="password" class="input" placeholder="••••••••" required />
          </div>

          <div v-if="error" class="text-xs text-red-600 bg-red-50 border border-red-100 rounded-lg px-3 py-2">{{ error }}</div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full py-2.5 bg-gray-900 text-white text-sm font-semibold rounded-lg hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition shadow-btn"
          >
            {{ loading ? 'Signing in…' : 'Sign In' }}
          </button>
        </form>
      </div>

      <p class="text-center text-xs text-gray-500 mt-4">
        No account?
        <router-link to="/register" class="font-medium text-gray-900 hover:underline">Register free</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()
const form = ref({ email: '', password: '' })
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true; error.value = ''
  try {
    const res = await api.post('/login', { email: form.value.email.toLowerCase(), password: form.value.password })
    authStore.setAuth(res.data)
    router.push(authStore.dashboardRoute)
  } catch (e) {
    error.value = e.response?.data?.error || 'Login failed. Please check your credentials.'
  } finally { loading.value = false }
}
</script>
