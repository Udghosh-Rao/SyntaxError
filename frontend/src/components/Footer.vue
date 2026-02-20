<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-section">
        <h4>About EventHub</h4>
        <p>Your ultimate platform for discovering and managing sports events with ease.</p>
      </div>
      
      <div class="footer-section">
        <h4>Quick Links</h4>
        <ul>
          <li><router-link to="/">Home</router-link></li>
          <li><router-link to="/events">Events</router-link></li>
          <li><a href="#">About Us</a></li>
          <li><a href="#">Contact</a></li>
        </ul>
      </div>
      
      <div class="footer-section">
        <h4>Follow Us</h4>
        <div class="social-links">
          <a href="#" class="social-icon">Facebook</a>
          <a href="#" class="social-icon">Twitter</a>
          <a href="#" class="social-icon">Instagram</a>
        </div>
      </div>
      
      <div class="footer-section">
        <h4>Legal</h4>
        <ul>
          <li><a href="#">Privacy Policy</a></li>
          <li><a href="#">Terms of Service</a></li>
          <li><a href="#">Cookie Policy</a></li>
        </ul>
      </div>
    </div>
    
    <div class="footer-bottom">
      <p>&copy; 2024 EventHub. All rights reserved.</p>
    </div>
  </footer>
</template>

<script setup lang="ts">
// Footer component with navigation links and social media
</script>

<style scoped>
.footer {
  background-color: #1f2937;
  color: #f3f4f6;
  padding: 3rem 0 0;
  margin-top: 4rem;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.footer-section h4 {
  font-size: 1.1rem;
  margin-bottom: 1rem;
  color: #fff;
}

.footer-section ul {
  list-style: none;
  padding: 0;
}

.footer-section ul li {
  margin-bottom: 0.5rem;
}

.footer-section a {
  color: #d1d5db;
  text-decoration: none;
  transition: color 0.3s;
}

.footer-section a:hover {
  color: #3b82f6;
}

.social-links {
  display: flex;
  gap: 1rem;
}

.social-icon {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: rgba(59, 130, 246, 0.2);
  border-radius: 0.25rem;
  transition: background-color 0.3s;
}

.social-icon:hover {
  background-color: rgba(59, 130, 246, 0.4);
}

.footer-bottom {
  border-top: 1px solid #374151;
  padding: 1.5rem;
  text-align: center;
  background-color: #111827;
  color: #9ca3af;
}
</style>
