<template>
  <div class="login-page">
    <div class="container auth-wrapper">
      <div class="card-premium auth-card animate-corp relative overflow-hidden group">
        <div class="absolute inset-0 bg-gradient-to-br from-[#ff007f]/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
        <div class="auth-header mb-10 text-center relative z-10">
          <span class="badge-corp bg-[#ff007f]/10 text-[#ff007f] border-[#ff007f]/20">Verified Access</span>
          <h1 class="hero-title-small mt-4 text-white font-900 tracking-tight">Athlete Login</h1>
          <p class="text-dim mt-2 font-500">Sign in to unlock massive events and manage your tournaments.</p>
        </div>
        
        <form @submit.prevent="handleLogin" class="auth-form relative z-10 w-full">
          <div class="input-stack mb-6">
            <label class="block text-xs font-bold tracking-widest text-[#00f3ff] mb-2 uppercase">Email</label>
            <input v-model="email" type="email" class="input-corp w-full px-4 py-3 rounded-xl text-white placeholder-white/40 bg-black/60 border border-white/20 focus:outline-none focus:border-[#00f3ff] focus:shadow-[0_0_15px_rgba(0,243,255,0.2)] transition-all" placeholder="name@sport.live" required />
          </div>
          
          <div class="input-stack mb-6">
            <label class="block text-xs font-bold tracking-widest text-[#00f3ff] mb-2 uppercase">Password</label>
            <input v-model="password" type="password" class="input-corp w-full px-4 py-3 rounded-xl text-white placeholder-white/40 bg-black/60 border border-white/20 focus:outline-none focus:border-[#00f3ff] focus:shadow-[0_0_15px_rgba(0,243,255,0.2)] transition-all" placeholder="••••••••" required />
          </div>
          
          <div v-if="error" class="error-panel-inline mt-4 animate-corp bg-[#ff007f]/10 border-[#ff007f]/20 text-[#ff007f]">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
            <span>{{ error }}</span>
          </div>
          
          <button type="submit" :disabled="authStore.isLoading" class="btn-corp bg-[#ff007f] text-black w-full mt-8 py-4 text-sm font-900 tracking-wider hover:bg-white hover:text-black hover:shadow-[0_0_20px_rgba(255,0,127,0.4)] transition-all duration-300">
            {{ authStore.isLoading ? 'Verifying Ticket...' : 'Get In' }}
          </button>
        </form>
        
        <div class="auth-footer mt-12 text-center pt-8 border-t relative z-10 border-white/10">
          <p class="text-white/60 text-sm">Not on the list? <router-link to="/register" class="link-corp text-[#00f3ff] ml-2 font-900 hover:text-white transition-colors">Join the Platform</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();
const email = ref('');
const password = ref('');
const error = ref('');

const handleLogin = async () => {
  error.value = '';
  try {
    await authStore.login(email.value, password.value);
    
    if (authStore.isAdmin) {
      router.push('/admin');
    } else if (authStore.isOrganizer) {
      router.push('/organizer');
    } else {
      router.push('/home');
    }
  } catch (err: any) {
    error.value = err.response?.data?.message || 'Authentication sequence failed. Verify credentials.';
  }
};
</script>

<style scoped>
.login-page {
  padding: 80px 0 40px;
  min-height: 100vh;
  display: flex;
  align-items: center;
}

.auth-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}

.auth-card {
  width: 100%;
  max-width: 440px;
  padding: 2.5rem;
}

.hero-title-small {
  font-size: 1.75rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.15;
}

.error-panel-inline {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #ff5555;
  font-size: 0.85rem;
  padding: 1rem;
  background: rgba(255, 85, 85, 0.05);
  border: 1px solid rgba(255, 85, 85, 0.1);
  border-radius: var(--radius-sm);
}

.link-corp {
  color: var(--brand-primary);
  text-decoration: none;
  font-weight: 700;
  transition: var(--transition-fast);
}

.link-corp:hover {
  filter: brightness(1.2);
  text-decoration: underline;
}

.border-top {
  border-top: 1px solid var(--border-subtle);
}

@media (max-width: 640px) {
  .auth-card {
    padding: 2.5rem;
  }
}
</style>
