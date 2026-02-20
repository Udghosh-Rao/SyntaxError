<template>
  <div class="register-page">
    <div class="register-container">
      <h1>SyntaxError Sports</h1>
      <h2>Create Account</h2>
      
      <form @submit.prevent="handleRegister" class="register-form">
        <!-- Username Field -->
        <div class="form-group">
          <label for="username">Username</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            placeholder="Choose a username"
            required
          />
        </div>

        <!-- Email Field -->
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="Enter your email"
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
            placeholder="Create a password"
            required
          />
        </div>

        <!-- Role Selection -->
        <div class="form-group">
          <label for="role">I want to register as:</label>
          <select id="role" v-model="form.role" required>
            <option value="user">Regular User</option>
            <option value="organizer">Event Organizer</option>
          </select>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="error-message">{{ error }}</div>

        <!-- Submit Button -->
        <button type="submit" :disabled="loading" class="submit-button">
          {{ loading ? 'Creating account...' : 'Register' }}
        </button>
      </form>

      <!-- Login Link -->
      <div class="login-link">
        <p>Already have an account? <router-link to="/login">Login here</router-link></p>
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
  email: '',
  password: '',
  role: 'user'
})

const loading = ref(false)
const error = ref('')

const handleRegister = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await api.post('/auth/register', {
      username: form.value.username,
      email: form.value.email,
      password: form.value.password,
      role: form.value.role
    })

    const { user, access_token } = response.data

    // Store token and user info
    localStorage.setItem('access_token', access_token)
    userStore.setUser(user)
    userStore.setToken(access_token)

    // Redirect based on role
    if (user.role === 'organizer') {
      router.push('/organizer-dashboard')
    } else {
      router.push('/events')
    }
  } catch (err: any) {
    error.value = err.response?.data?.message || 'Registration failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.register-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  padding: 40px;
  max-width: 450px;
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

.register-form {
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

input,
select {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s;
}

input:focus,
select:focus {
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

.login-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
  font-size: 14px;
}

.login-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
