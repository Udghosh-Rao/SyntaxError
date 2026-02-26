<template>
  <div class="min-h-screen bg-black text-white relative flex flex-col selection:bg-[#ccff00] selection:text-black">
    <!-- Cinematic Fixed Background -->
    <div class="fixed inset-0 z-0 pointer-events-none">
      <img src="/stadium-hero.png" alt="Stadium" class="w-full h-full object-cover object-top opacity-[0.15]" />
      <div class="absolute inset-0 bg-gradient-to-b from-black/90 via-black/80 to-black"></div>
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_0%,black_100%)] opacity-90"></div>
    </div>

    <!-- Main Content Area -->
    <div class="relative z-10 pt-32 pb-24 flex-1">
      <div class="container mx-auto px-6 max-w-7xl">
        
        <!-- Dashboard Header -->
        <div class="mb-16">
          <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-white/10 bg-white/5 backdrop-blur-2xl shadow-xl mb-6">
             <span class="text-xs font-black tracking-[0.2em] text-[#00f3ff] uppercase">Live Sports Platform</span>
          </div>
          <h1 class="text-6xl md:text-8xl font-black text-white tracking-tighter leading-[0.95] mb-6 drop-shadow-2xl">
            Find Your Next <br/>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#00f3ff] via-[#ccff00] to-[#00f3ff] bg-[length:200%_auto] animate-gradient-x">Tournament.</span>
          </h1>
          <p class="text-xl text-white/60 font-medium max-w-2xl leading-relaxed drop-shadow-md">
            Browse upcoming massive sports events, secure your premium tickets instantly, and experience the pure hype.
          </p>
        </div>

        <!-- Curated Section -->
        <div v-if="authStore.isAuthenticated && authStore.isUser" class="mb-20">
           <RecommendationRow title="Curated For You 🎯" :limit="4" />
        </div>

        <!-- Search & Filter Glass Bar -->
        <div class="bg-white/5 border border-white/10 rounded-3xl p-6 md:p-8 backdrop-blur-3xl shadow-2xl mb-16 relative overflow-hidden group">
          <div class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/5 to-white/0 opacity-0 group-hover:opacity-100 transition-opacity duration-700 pointer-events-none"></div>
          
          <div class="flex flex-col md:flex-row gap-6 relative z-10">
            <!-- Search Input -->
            <div class="flex-1">
              <label class="block text-[0.65rem] font-black tracking-[0.2em] text-[#ccff00] mb-3 uppercase">Event Search</label>
              <div class="relative">
                <input 
                  type="text" 
                  v-model="searchQuery" 
                  placeholder="Search sports, cities, events..."
                  class="w-full bg-black/40 border border-white/10 rounded-2xl px-6 py-5 text-white placeholder-white/40 focus:outline-none focus:border-[#ccff00]/50 focus:bg-black/60 transition-all font-medium text-lg placeholder:font-normal hover:border-white/20"
                />
                <span class="absolute right-6 top-1/2 -translate-y-1/2 text-white/40 text-xl pointer-events-none">🔍</span>
              </div>
            </div>

            <!-- Ticket Bracket Filter -->
            <div class="w-full md:w-80">
              <label class="block text-[0.65rem] font-black tracking-[0.2em] text-[#00f3ff] mb-3 uppercase">Ticket Bracket</label>
              <div class="relative">
                <select v-model="budgetFilter" class="w-full bg-black/40 border border-white/10 rounded-2xl px-6 py-5 text-white focus:outline-none focus:border-[#00f3ff]/50 focus:bg-black/60 transition-all font-medium text-lg appearance-none cursor-pointer hover:border-white/20">
                  <option value="all" class="bg-gray-900">All Tiers</option>
                  <option value="cheap" class="bg-gray-900">General Admission (&lt; ₹500)</option>
                  <option value="mid" class="bg-gray-900">VIP Access (₹500 - ₹2000)</option>
                  <option value="premium" class="bg-gray-900">Backstage Pass (&gt; ₹2000)</option>
                </select>
                <span class="absolute right-6 top-1/2 -translate-y-1/2 text-white/40 pointer-events-none tracking-tighter">▼</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Events Grid Header -->
        <div class="flex items-end justify-between mb-10">
          <h2 class="text-4xl md:text-5xl font-black tracking-tighter text-white">The Lineup</h2>
          <span class="text-white/40 font-bold uppercase tracking-widest text-sm">{{ filteredEvents.length }} Events</span>
        </div>

        <!-- State Handling -->
        <div v-if="loading" class="py-24 flex flex-col items-center justify-center">
          <div class="w-12 h-12 border-4 border-white/10 border-t-[#ccff00] rounded-full animate-spin mb-6"></div>
          <span class="text-white/60 font-bold tracking-widest uppercase text-sm">Fetching Lineup...</span>
        </div>

        <div v-else-if="error" class="bg-red-500/10 border border-red-500/20 rounded-3xl p-12 text-center backdrop-blur-xl max-w-2xl mx-auto">
          <h3 class="text-3xl font-black text-white mb-4">Connection Lost</h3>
          <p class="text-red-400 font-medium mb-8 text-lg">{{ error }}</p>
          <button @click="fetchEvents" class="bg-white text-black font-black px-8 py-3 rounded-full hover:scale-105 active:scale-95 transition-transform shadow-xl">
            Retry Connection
          </button>
        </div>

        <!-- Events Grid -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <EventCard 
            v-for="event in filteredEvents" 
            :key="event.id" 
            :event="event" 
            :class="{ 'opacity-[0.35] grayscale-[0.8] hover:opacity-100 hover:grayscale-0 transition-all duration-700': event._dePrioritize }"
          />
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { eventApi } from '../services/api';
import EventCard from '../components/EventCard.vue';
import RecommendationRow from '../components/RecommendationRow.vue';
import { useAuthStore } from '../stores/auth';

const events = ref<any[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);
const searchQuery = ref('');
const budgetFilter = ref('all');
const authStore = useAuthStore();

const fetchEvents = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await eventApi.getAll();
    events.value = response.data;
  } catch (err: any) {
    console.error('Error fetching events:', err);
    error.value = 'Service unavailable. Please verify connectivity.';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchEvents();
});

const filteredEvents = computed(() => {
  let result = [...events.value];
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(event => 
      event.title.toLowerCase().includes(query) ||
      event.sport_category.toLowerCase().includes(query) ||
      (event.venue_city && event.venue_city.toLowerCase().includes(query))
    );
  }
  
  // US-01: Visually de-prioritise instead of strictly filtering
  if (budgetFilter.value !== 'all') {
    result = result.map(e => ({
      ...e,
      _dePrioritize: e.price_tier !== budgetFilter.value
    })).sort((a, b) => {
      if (a._dePrioritize && !b._dePrioritize) return 1;
      if (!a._dePrioritize && b._dePrioritize) return -1;
      return 0;
    });
  } else {
    result = result.map(e => ({ ...e, _dePrioritize: false }));
  }
  
  return result;
});
</script>

<style scoped>
@keyframes gradient-x {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}
.animate-gradient-x {
  animation: gradient-x 6s ease infinite;
}
</style>


