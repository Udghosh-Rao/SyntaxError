<template>
  <div class="register-page">
    <div class="container auth-wrapper">
      <div class="card-premium auth-card animate-corp relative overflow-hidden group">
        <div class="absolute inset-0 bg-gradient-to-br from-[#00f3ff]/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
        <div class="auth-header mb-10 text-center relative z-10">
          <span class="badge-corp bg-[#00f3ff]/10 text-[#00f3ff] border-[#00f3ff]/20">New Arrival</span>
          <h1 class="hero-title-small mt-4 text-white font-900 tracking-tight">Join the Party</h1>
          <p class="text-dim mt-2 font-500">Create your account to start booking massive gigs.</p>
        </div>
        
        <form @submit.prevent="handleRegister" class="auth-form-grid relative z-10 w-full">
          <div class="input-stack mb-6">
            <label class="label-muted text-[10px] tracking-widest text-[#00f3ff] mb-2">Display Name</label>
            <input v-model="form.name" type="text" class="input-corp bg-black/60 border-white/10 focus:border-[#00f3ff] focus:shadow-[0_0_15px_rgba(0,243,255,0.2)] transition-all" placeholder="Party Goer Name" required />
          </div>
          
          <div class="input-stack mb-6">
            <label class="label-muted text-[10px] tracking-widest text-[#00f3ff] mb-2">Email</label>
            <input v-model="form.email" type="email" class="input-corp bg-black/60 border-white/10 focus:border-[#00f3ff] focus:shadow-[0_0_15px_rgba(0,243,255,0.2)] transition-all" placeholder="name@party.live" required />
          </div>
          
          <div class="input-stack mb-6">
            <label class="label-muted text-[10px] tracking-widest text-[#00f3ff] mb-2">Password</label>
            <input v-model="form.password" type="password" class="input-corp bg-black/60 border-white/10 focus:border-[#00f3ff] focus:shadow-[0_0_15px_rgba(0,243,255,0.2)] transition-all" placeholder="••••••••" required />
          </div>
          
          <div class="input-stack mb-6">
            <label class="label-muted text-[10px] tracking-widest text-[#ff007f] mb-2">Your Vibe</label>
            <select v-model="form.role" class="input-corp bg-black/60 border-white/10 focus:border-[#ff007f] focus:shadow-[0_0_15px_rgba(255,0,127,0.2)] transition-all">
              <option value="user">Attending Shows</option>
              <option value="organizer">Hosting Gigs (Vendor)</option>
            </select>
          </div>

          <!-- Profile Preferences -->
          <div v-if="form.role === 'user'" class="preferences-panel mt-6 animate-corp p-6 rounded-2xl bg-black/40 border border-[#00f3ff]/20 shadow-[inset_0_0_20px_rgba(0,243,255,0.05)] backdrop-blur-xl">
              <p class="label-muted mb-6 text-[#00f3ff]">Local Scene</p>
              
              <div class="input-stack">
                <label class="label-muted text-[10px] tracking-widest text-white/50 mb-2">Home City</label>
                <input v-model="form.city" type="text" class="input-corp bg-black/40 border-white/10 focus:border-[#00f3ff]" placeholder="e.g. Mumbai" />
              </div>
              <div class="input-stack mt-6">
                <label class="label-muted text-[10px] tracking-widest text-white/50 mb-2">Ticket Preference</label>
                <select v-model="form.budget_preference" class="input-corp bg-black/40 border-white/10 focus:border-[#00f3ff]">
                  <option value="cheap">General Admission (< ₹500)</option>
                  <option value="mid">VIP Access (₹500 - ₹2000)</option>
                  <option value="premium">Backstage Pass (> ₹2000)</option>
                </select>
              </div>
          </div>

          <div v-if="error" class="error-panel-inline mt-6 animate-corp bg-[#ff007f]/10 border-[#ff007f]/20 text-[#ff007f]">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
            <span>{{ error }}</span>
          </div>
          
          <button type="submit" :disabled="loading" class="btn-corp bg-[#00f3ff] text-black w-full mt-8 py-4 text-sm font-900 tracking-wider hover:bg-white hover:text-black hover:shadow-[0_0_20px_rgba(0,243,255,0.4)] transition-all duration-300">
            {{ loading ? 'Processing...' : 'Secure Profile' }}
          </button>
        </form>
        
        <div class="auth-footer mt-12 text-center pt-8 border-t relative z-10 border-white/10">
          <p class="text-white/60 text-sm">Already on the list? <router-link to="/login" class="link-corp text-[#ff007f] ml-2 font-900 hover:text-white transition-colors">Log In</router-link></p>
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
const loading = ref(false);
const error = ref('');

const form = ref({
  name: '',
  email: '',
  password: '',
  role: 'user',
  city: '',
  budget_preference: 'mid',
  preferred_sports: [] as string[]
});

const handleRegister = async () => {
  loading.value = true;
  error.value = '';

  try {
    await authStore.register(form.value);
    
    if (authStore.isAdmin) {
      router.push('/admin');
    } else if (authStore.isOrganizer) {
      router.push('/organizer');
    } else {
      router.push('/home');
    }
  } catch (err: any) {
    error.value = err.response?.data?.message || authStore.error || 'Identity initialization failed.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.register-page {
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
  max-width: 480px;
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

.panel-divider {
  height: 1px;
  background: var(--border-subtle);
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
