<template>
  <div id="app">
    <nav class="navbar">
      <div class="navbar-container">
        <router-link to="/" class="nav-logo">SyntaxError Sports</router-link>
        <ul class="nav-menu">
          <li class="nav-item">
            <router-link to="/" class="nav-link">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/events" class="nav-link">Events</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/profile" class="nav-link">Profile</router-link>
          </li>
        </ul>
      </div>
    </nav>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

onMounted(() => {
  // Initialize app
  console.log('App mounted');
});
</script>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background-color: #1e1e1e;
  padding: 1rem 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-logo {
  color: #00bcd4;
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
}

.nav-menu {
  display: flex;
  list-style: none;
  gap: 2rem;
}

.nav-item {
  margin: 0;
}

.nav-link {
  color: #fff;
  text-decoration: none;
  transition: color 0.3s;
}

.nav-link:hover {
  color: #00bcd4;
}

.main-content {
  flex: 1;
  max-width: 1200px;
  margin: 2rem auto;
  width: 100%;
  padding: 0 2rem;
}
</style>
