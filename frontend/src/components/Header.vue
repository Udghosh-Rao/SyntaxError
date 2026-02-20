<template>
  <header class="app-header">
    <div class="header-container">
      <div class="logo-section">
        <h1 class="logo">EventHub</h1>
      </div>
      <nav class="nav-menu">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/events" class="nav-link">Events</router-link>
        <router-link v-if="isOrgani zer" to="/organizer-dashboard" class="nav-link">Dashboard</router-link>
        <router-link v-if="isAdmin" to="/admin-dashboard" class="nav-link">Admin</router-link>
      </nav>
      <div class="header-actions">
        <div v-if="isAuthenticated" class="user-menu">
          <span class="user-name">{{ currentUser?.name }}</span>
          <button @click="logout" class="btn-logout">Logout</button>
        </div>
        <div v-else class="auth-buttons">
          <router-link to="/login" class="btn-login">Login</router-link>
          <router-link to="/register" class="btn-register">Register</router-link>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const isAuthenticated = computed(() => authStore.isAuthenticated);
const currentUser = computed(() => authStore.currentUser);
const isOrganizer = computed(() => authStore.currentUser?.role === 'organizer');
const isAdmin = computed(() => authStore.currentUser?.role === 'admin');

const logout = () => {
  authStore.logout();
  router.push({ name: 'Home' });
};
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-section {
  flex: 0 0 auto;
}

.logo {
  margin: 0;
  font-size: 1.8rem;
  font-weight: bold;
}

.nav-menu {
  flex: 1;
  display: flex;
  gap: 2rem;
  margin: 0 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  padding: 0.5rem 0;
  border-bottom: 2px solid transparent;
}

.nav-link:hover {
  border-bottom-color: white;
}

.nav-link.router-link-active {
  border-bottom-color: white;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-name {
  font-weight: 500;
}

.btn-logout {
  padding: 0.5rem 1rem;
  background: rgba(255,255,255,0.2);
  color: white;
  border: 1px solid white;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-logout:hover {
  background: rgba(255,255,255,0.3);
}

.auth-buttons {
  display: flex;
  gap: 0.5rem;
}

.btn-login,
.btn-register {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  display: inline-block;
}

.btn-login {
  color: white;
  border: 1px solid white;
  background: transparent;
}

.btn-login:hover {
  background: rgba(255,255,255,0.1);
}

.btn-register {
  background: white;
  color: #667eea;
}

.btn-register:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}
</style>
