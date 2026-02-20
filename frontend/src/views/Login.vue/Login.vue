<template>
  <div class="login-page">
    <div class="login-container">
      <h1>SyntaxError Sports</h1>
      <h2>Login</h2>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <!-- Username Field -->
        <div class="form-group">
          <label for="username">Username</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            placeholder="Enter your username"
            required
          />
        </div>

        <!-- Password Field -->
        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            placeholder="Enter your password"
            required
          />
        </div>

        <!-- Error Message -->
        <div v-if="error" class="error-message">{{ error }}</div>

        <!-- Submit Button -->
        <button type="submit" :disabled="loading" class="submit-button">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>

      <!-- Sign Up Link -->
      <div class="signup-link">
        <p>Don't have an account? <router-link to="/register">Sign up here</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/useUserStore'
import api from '@/services/api'

const router = useRouter()
const userStore = useUserStore()

const form = ref({
  username: '',
  password: ''
})

const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await api.post('/auth/login', {
      username: form.value.username,
      password: form.value.password
    })

    const { user, access_token } = response.data

    // Store token and user info
    localStorage.setItem('access_token', access_token)
    userStore.setUser(user)
    userStore.setToken(access_token)

    // Redirect based on role
    if (user.role === 'admin') {
      router.push('/admin-dashboard')
    } else if (user.role === 'organizer') {
      router.push('/organizer-dashboard')
    } else {
      router.push('/events')
    }
  } catch (err: any) {
    error.value = err.response?.data?.message || 'Login failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  padding: 40px;
  max-width: 400px;
  width: 100%;
}

h1 {
  color: #667eea;
  text-align: center;
  margin-bottom: 10px;
  font-size: 28px;
}

h2 {
  color: #333;
  text-align: center;
  margin-bottom: 30px;
  font-size: 24px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

input {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s;
}

input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.error-message {
  background-color: #fee;
  color: #c33;
  padding: 12px;
  border-radius: 4px;
  font-size: 14px;
}

.submit-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 12px;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.3s;
  font-size: 16px;
}

.submit-button:hover:not(:disabled) {
  opacity: 0.9;
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.signup-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
  font-size: 14px;
}

.signup-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.signup-link a:hover {
  text-decoration: underline;
}
</style>
