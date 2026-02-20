<template>
  <div class="home-view">
    <section class="hero">
      <h1>Welcome to SyntaxError Sports</h1>
      <p>Discover and manage exciting sports events around you</p>
      <div class="button-group">
        <router-link to="/events" class="btn btn-primary">Explore Events</router-link>
        <router-link to="/login" class="btn btn-outline">Login</router-link>
        <router-link to="/register" class="btn btn-outline">Register</router-link>
      </div>
    </section>

    <section class="features">
      <div class="feature-card">
        <h2>📄 Browse Events</h2>
        <p>Find sports events happening near you with detailed information</p>
      </div>
      <div class="feature-card">
        <h2>📝 Registration</h2>
        <p>Quick and easy registration for events you're interested in</p>
      </div>
      <div class="feature-card">
        <h2>💬 Chat Support</h2>
        <p>Get instant help with our AI-powered event assistant</p>
      </div>
    </section>

    <section class="dashboards">
      <h2>Manage Your Platform</h2>
      <div class="dashboard-links">
        <router-link to="/admin" class="dashboard-card admin-card">
          <h3>👨‍💼 Admin Dashboard</h3>
          <p>Manage all events, users, and platform settings</p>
        </router-link>
        <router-link to="/organizer" class="dashboard-card organizer-card">
          <h3>🎯 Organizer Dashboard</h3>
          <p>Create and manage your events, view analytics</p>
        </router-link>
      </div>
    </section>

    <section class="chat-section">
      <h2>Need Help?</h2>
      <ChatInterface />
    </section>
  </div>
</template>

<script setup lang="ts">
import ChatInterface from '../components/ChatInterface.vue';
</script>

<style scoped>
.home-view {
  padding: 2rem 0;
}

.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 2rem;
  text-align: center;
}

.hero h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.hero p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
}

.button-group {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  display: inline-block;
  padding: 0.75rem 2rem;
  background-color: #00bcd4;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 500;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #008ba3;
}

.btn-outline {
  background-color: transparent;
  border: 2px solid white;
}

.btn-outline:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  padding: 4rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background: #f5f5f5;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.dashboards {
  background-color: #f9f9f9;
  padding: 4rem 2rem;
  text-align: center;
}

.dashboards h2 {
  margin-bottom: 3rem;
  font-size: 2rem;
}

.dashboard-links {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-card {
  padding: 2rem;
  border-radius: 8px;
  text-decoration: none;
  color: white;
  font-weight: 500;
  transition: transform 0.3s, box-shadow 0.3s;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.dashboard-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 12px rgba(0,0,0,0.2);
}

.dashboard-card h3 {
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
}

.admin-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.organizer-card {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.chat-section {
  padding: 4rem 2rem;
  max-width: 600px;
  margin: 0 auto;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.chat-section h2 {
  text-align: center;
  margin-bottom: 2rem;
}
</style>
