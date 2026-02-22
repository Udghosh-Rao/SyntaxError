<template>
  <div class="home-page animate-corp">
    <header class="hero-v3 relative overflow-hidden">
      <!-- Added a localized glowing stage light effect -->
      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full max-w-4xl bg-[radial-gradient(ellipse_at_top,_var(--brand-glow),_transparent_70%)] opacity-30 mix-blend-screen pointer-events-none"></div>

      <div class="container text-center animate-corp relative z-10">
        <span class="badge-corp backdrop-blur-md bg-black/40 border-[var(--brand-primary)]/30 text-[var(--brand-primary)]">Live Gig Platform</span>
        <h1 class="hero-main-title delay-100 text-5xl md:text-7xl font-900 tracking-tighter mt-6">
          Find Your Next <span class="text-gradient">Live Show.</span>
        </h1>
        <p class="hero-description delay-200 text-lg text-white/70 max-w-2xl mx-auto mt-6">
          Browse upcoming gigs, secure tickets instantly, and hype your favorite artists — all in one place.
        </p>

        <div v-if="authStore.isAuthenticated && authStore.isUser" class="hero-personalized-track mt-8 animate-corp delay-300">
           <RecommendationRow title="Curated For You" :limit="4" />
        </div>
      </div>
    </header>

    <section class="section-spacer relative">
      <div class="container relative z-10">
        <div class="section-header-flex mb-12 animate-corp p-6 lg:p-8 rounded-3xl bg-black/40 border border-white/5 backdrop-blur-xl shadow-luxury relative overflow-hidden group">
          <div class="absolute inset-0 bg-gradient-to-r from-brand-secondary/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700 pointer-events-none"></div>
          <div class="header-text relative z-10">
            <h2 class="section-title-large text-white font-900 tracking-tight">The Lineup</h2>
            <p class="section-subtitle text-white/50 mt-2 font-500">Find and join the latest massive shows near you.</p>
          </div>
          <div class="header-controls flex flex-col sm:flex-row gap-4 w-full lg:w-auto mt-6 lg:mt-0 relative z-10">
            <div class="search-luxury-wrapper flex-grow lg:flex-grow-0 lg:w-72">
               <label class="label-muted text-[10px] tracking-widest text-[#00f3ff] mb-2 block w-full">Vibe Search</label>
              <input 
                type="text" 
                v-model="searchQuery" 
                placeholder="Search gigs, artists..."
                 class="input-corp w-full bg-black/60 border-white/10 focus:border-[#00f3ff] focus:shadow-[0_0_15px_rgba(0,243,255,0.2)] transition-all"
              />
            </div>

            <div class="filter-luxury-wrapper flex-grow lg:flex-grow-0 lg:w-56">
               <label class="label-muted text-[10px] tracking-widest text-[#00f3ff] mb-2 block w-full">Ticket Bracket</label>
               <select v-model="budgetFilter" class="input-corp w-full bg-black/60 border-white/10 focus:border-[#00f3ff] transition-all">
                <option value="all">All Tiers</option>
                <option value="cheap">General Admission (< ₹500)</option>
                <option value="mid">VIP Access (₹500 - ₹2000)</option>
                <option value="premium">Backstage Pass (> ₹2000)</option>
              </select>
            </div>
          </div>
        </div>

        <div v-if="loading" class="loading-corp py-12">
          <div class="pulse-loader mx-auto mb-6"></div>
          <span class="text-dim">Fetching events...</span>
        </div>

        <div v-else-if="error" class="error-corp card-premium text-center py-12">
          <h3 class="mb-4">Failed to load</h3>
          <p class="text-dim mb-6">{{ error }}</p>
          <button @click="fetchEvents" class="btn-corp btn-corp-primary justify-center">Try Again</button>
        </div>

        <div v-else class="events-grid-premium animate-corp delay-100">
          <EventCard 
            v-for="event in filteredEvents" 
            :key="event.id" 
            :event="event" 
          />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
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
    const config = authStore.token ? {
        headers: { Authorization: `Bearer ${authStore.token}` }
    } : {};
    
    const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
    const response = await axios.get(`${baseUrl}/events`, config);
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
  let result = events.value;
  
  if (budgetFilter.value !== 'all') {
    result = result.filter(e => e.price_tier === budgetFilter.value);
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(event => 
      event.title.toLowerCase().includes(query) ||
      event.sport_category.toLowerCase().includes(query) ||
      (event.venue_city && event.venue_city.toLowerCase().includes(query))
    );
  }
  
  return result;
});
</script>

<style scoped>
.home-page {
  padding-top: var(--nav-height);
}

.hero-main-title {
  margin-bottom: 1.5rem;
}

.hero-description {
  margin-bottom: 2rem;
}

.section-header-flex {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.search-luxury-wrapper {
  flex: 1;
  min-width: 200px;
}

.filter-luxury-wrapper {
  width: 200px;
}

.loading-corp {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

@media (max-width: 1024px) {
  .section-header-flex {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-luxury-wrapper,
  .filter-luxury-wrapper {
    width: 100%;
  }
}
</style>


