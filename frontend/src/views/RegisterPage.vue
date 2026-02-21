<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-12">
    <div class="w-full max-w-md">
      <router-link to="/" class="flex items-center justify-center gap-2 mb-8 text-gray-900 hover:text-gray-700 transition">
        <span class="font-bold text-lg">SportsSync</span>
      </router-link>

      <div class="bg-white rounded-2xl border border-gray-100 shadow-card p-8">
        <h1 class="text-xl font-bold text-gray-900 mb-1">Create account</h1>
        <p class="text-sm text-gray-500 mb-6">Join thousands of sports enthusiasts</p>

        <form @submit.prevent="handleRegister" class="space-y-4">
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1.5">Full Name</label>
              <input v-model="form.name" class="input" placeholder="John Doe" required />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1.5">Role</label>
              <select v-model="form.role" class="input">
                <option value="user">User</option>
                <option value="organizer">Organizer</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-xs font-medium text-gray-700 mb-1.5">Email</label>
            <input v-model="form.email" type="email" class="input" placeholder="you@example.com" required />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1.5">Password</label>
              <input v-model="form.password" type="password" class="input" placeholder="Min 6 chars" required />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1.5">Confirm</label>
              <input v-model="form.confirmPassword" type="password" class="input" placeholder="Repeat" required />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1.5">City</label>
              <input v-model="form.city" class="input" placeholder="Mumbai" />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1.5">Budget</label>
              <select v-model="form.budget_preference" class="input">
                <option value="cheap">Cheap (under ₹500)</option>
                <option value="mid">Mid (₹500–₹2000)</option>
                <option value="premium">Premium (₹2000+)</option>
              </select>
            </div>
          </div>

          <!-- Sports Preferences -->
          <div>
            <label class="block text-xs font-medium text-gray-700 mb-2">Preferred Sports</label>
            <div class="flex flex-wrap gap-2">
              <label
                v-for="sport in sportsList" :key="sport"
                class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full border text-xs cursor-pointer transition select-none"
                :class="form.preferred_sports.includes(sport)
                  ? 'bg-gray-900 text-white border-gray-900'
                  : 'bg-white text-gray-600 border-gray-200 hover:border-gray-300'"
              >
                <input type="checkbox" :value="sport" v-model="form.preferred_sports" class="hidden" />
                {{ sport }}
              </label>
            </div>
          </div>

          <div v-if="error" class="text-xs text-red-600 bg-red-50 border border-red-100 rounded-lg px-3 py-2">{{ error }}</div>

          <button type="submit" :disabled="loading"
            class="w-full py-2.5 bg-gray-900 text-white text-sm font-semibold rounded-lg hover:bg-gray-800 disabled:opacity-50 transition shadow-btn">
            {{ loading ? 'Creating account…' : 'Create Account' }}
          </button>
        </form>
      </div>

      <p class="text-center text-xs text-gray-500 mt-4">
        Already have an account?
        <router-link to="/login" class="font-medium text-gray-900 hover:underline">Sign in</router-link>
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
const sportsList = ['Football', 'Cricket', 'Tennis', 'Basketball', 'Running', 'Badminton', 'Swimming', 'Cycling']
const form = ref({ name:'', email:'', password:'', confirmPassword:'', role:'user', city:'', budget_preference:'mid', preferred_sports:[] })
const loading = ref(false)
const error = ref('')

async function handleRegister() {
  error.value = ''
  if (form.value.password !== form.value.confirmPassword) { error.value = 'Passwords do not match'; return }
  loading.value = true
  try {
    const payload = { ...form.value, preferred_sports: form.value.preferred_sports.map(s => s.toLowerCase()) }
    delete payload.confirmPassword
    payload.email = payload.email.toLowerCase()
    const res = await api.post('/register', payload)
    authStore.setAuth({ ...res.data, name: form.value.name })
    router.push(authStore.dashboardRoute)
  } catch (e) {
    error.value = e.response?.data?.error || 'Registration failed. Please try again.'
  } finally { loading.value = false }
}
</script>
