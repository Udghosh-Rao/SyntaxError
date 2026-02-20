<template>
  <div class="home-view">
    <section class="hero">
      <h1>Welcome to SyntaxError Sports</h1>
      <p>Discover and manage exciting sports events around you</p>
      <router-link to="/events" class="btn btn-primary">Explore Events</router-link>
    </section>
    <section class="features">
      <div class="feature-card">
        <h2>📄 Browse Events</h2>
        <p>Find sports events happening near you with detailed information</p>
      </div>
      <div class="feature-card">
        <h2>📞 Register</h2>
        <p>Quick and easy registration for events you're interested in</p>
      </div>
      <div class="feature-card">
        <h2>💬 Chat Support</h2>
        <p>Get instant help with our AI-powered event assistant</p>
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
}

.feature-card h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
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
