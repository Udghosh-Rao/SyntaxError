<template>
  <div id="app" class="bg-black min-h-screen text-white rounded-none">
    <nav class="fixed top-4 left-1/2 -translate-x-1/2 w-[95%] max-w-7xl z-[100] bg-black/60 backdrop-blur-2xl border border-white/10 rounded-full flex items-center justify-between px-6 py-3 transition-all duration-300 pointer-events-auto" :class="{ 'border-[#00f3ff]/50 shadow-[0_0_30px_rgba(0,243,255,0.15)] bg-black/80 scale-[0.98]': isScrolled }">
      <router-link to="/" class="flex items-center gap-2 decoration-transparent">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" class="text-[#00f3ff] drop-shadow-[0_0_8px_rgba(0,243,255,0.5)]" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"></path></svg>
        <span class="tracking-tighter font-black text-2xl text-white">LIVE<span class="text-[#00f3ff] drop-shadow-[0_0_8px_rgba(0,243,255,0.3)]">SPORTS</span></span>
      </router-link>
    
      <div class="hidden md:flex items-center gap-8">
        <!-- Unauthenticated Links -->
        <template v-if="!authStore.isAuthenticated">
          <router-link to="/" class="text-white/70 hover:text-[#ccff00] font-800 tracking-widest uppercase text-xs transition-colors decoration-transparent">Home</router-link>
          <router-link to="/login" class="text-white/70 hover:text-[#ccff00] font-800 tracking-widest uppercase text-xs transition-colors decoration-transparent">Login</router-link>
          <router-link to="/register" class="bg-[#ccff00] text-black font-900 tracking-wider uppercase text-sm px-8 py-3 rounded-full hover:bg-white hover:shadow-[0_0_20px_rgba(204,255,0,0.6)] transition-all duration-300 decoration-transparent">
            Sign Up
          </router-link>
        </template>

        <!-- Authenticated Links -->
        <template v-else>
          <router-link 
            v-if="authStore.isUser" 
            to="/home" 
            class="text-white/70 hover:text-[#00f3ff] font-800 tracking-widest uppercase text-xs transition-colors decoration-transparent"
          >
            Browse
          </router-link>

          <router-link 
            v-if="authStore.isOrganizer" 
            to="/organizer" 
            class="text-white/70 hover:text-[#ff007f] font-800 tracking-widest uppercase text-xs transition-colors decoration-transparent"
          >
            Dashboard
          </router-link>

          <router-link 
            v-if="authStore.isAdmin" 
            to="/admin" 
            class="text-white/70 hover:text-white font-800 tracking-widest uppercase text-xs transition-colors decoration-transparent"
          >
            Admin
          </router-link>

          <button @click="handleLogout" class="border border-[#ff007f] text-[#ff007f] bg-transparent px-8 py-3 rounded-full font-900 tracking-wider hover:bg-[#ff007f] hover:text-black hover:shadow-[0_0_20px_rgba(255,0,127,0.5)] transition-all duration-300 uppercase text-sm">
            Logout
          </button>
        </template>
      </div>
    </nav>
    
    <main class="flex-1 w-full text-white min-h-screen">
      <router-view />
    </main>

    <ChatbotWidget v-if="authStore.isAuthenticated" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from './stores/auth';
import ChatbotWidget from './components/ChatbotWidget.vue';

const router = useRouter();
const authStore = useAuthStore();
const isScrolled = ref(false);

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20;
};

onMounted(() => {
  authStore.initializeAuth();
  window.addEventListener('scroll', handleScroll);
});

const handleLogout = () => {
  authStore.logout();
  router.push('/');
};
</script>

<style scoped>
/* Scoped styles removed in favor of Tailwind CSS in the template */
</style>
