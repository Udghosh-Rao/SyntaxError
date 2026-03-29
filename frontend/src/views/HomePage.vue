<template>
  <div class="home-page">

    <!-- Background — toned down in light mode via CSS -->
    <div class="home-bg" aria-hidden="true">
      <img src="/stadium-hero.png" alt="" class="home-bg-img" />
      <div class="home-bg-overlay"></div>
    </div>

    <div class="home-content">
      <div class="container mx-auto px-6 max-w-7xl">

        <!-- Header -->
        <div class="mb-16">
          <div class="header-badge">
            <span>Live Sports Platform</span>
          </div>
          <h1 class="home-title">
            Find Your Next <br/>
            <span class="title-gradient animate-gradient-x">Tournament.</span>
          </h1>
          <p class="home-sub">
            Browse upcoming massive sports events, secure your premium tickets instantly, and experience the pure hype.
          </p>
        </div>

        <!-- Curated Section -->
        <div v-if="authStore.isAuthenticated && authStore.isUser" class="mb-20">
          <RecommendationRow title="Curated For You 🎯" :limit="6" />
        </div>

        <!-- Search & Filter -->
        <div class="search-panel mb-16">
          <div class="flex flex-col md:flex-row gap-6 relative z-10">

            <!-- Search -->
            <div class="flex-1">
              <label class="filter-label" style="color: var(--brand-primary)">Event Search</label>
              <div class="relative">
                <input
                  type="text"
                  v-model="searchQuery"
                  placeholder="Search sports, cities, events..."
                  class="search-input"
                />
                <span class="absolute right-6 top-1/2 -translate-y-1/2 text-xl pointer-events-none"
                  :style="{ color: 'var(--text-muted)' }">🔍</span>
              </div>
            </div>

            <!-- Budget filter -->
            <div class="w-full md:w-80">
              <label class="filter-label" style="color: var(--brand-accent)">Ticket Bracket</label>
              <div class="relative">
                <select v-model="budgetFilter" class="search-input appearance-none cursor-pointer">
                  <option value="all">All Tiers</option>
                  <option value="cheap">General Admission (&lt; ₹500)</option>
                  <option value="mid">VIP Access (₹500 - ₹2000)</option>
                  <option value="premium">Backstage Pass (&gt; ₹2000)</option>
                </select>
                <span class="absolute right-6 top-1/2 -translate-y-1/2 pointer-events-none"
                  :style="{ color: 'var(--text-muted)' }">▼</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Grid header -->
        <div class="flex items-end justify-between mb-10">
          <h2 class="lineup-title">The Lineup</h2>
          <span class="lineup-count">{{ filteredEvents.length }} Events</span>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="py-24 flex flex-col items-center justify-center gap-6">
          <div class="home-spinner"></div>
          <span class="state-label">Fetching Lineup…</span>
        </div>

        <!-- Error -->
        <div v-else-if="error" class="error-panel text-center max-w-2xl mx-auto">
          <h3 class="text-3xl font-black mb-4" :style="{ color: 'var(--text-primary)' }">Connection Lost</h3>
          <p class="mb-8" style="color: #f87171">{{ error }}</p>
          <button @click="fetchEvents" class="retry-btn">Retry Connection</button>
        </div>

        <!-- Events Grid -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <EventCard
            v-for="event in filteredEvents"
            :key="event.id"
            :event="event"
            :class="{ 'opacity-40 grayscale hover:opacity-100 hover:grayscale-0 transition-all duration-700': event._dePrioritize }"
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

const events      = ref<any[]>([]);
const loading     = ref(true);
const error       = ref<string | null>(null);
const searchQuery = ref('');
const budgetFilter = ref('all');
const authStore   = useAuthStore();

const fetchEvents = async () => {
  loading.value = true;
  error.value   = null;
  try {
    const response = await eventApi.getAll();
    events.value = response.data;
  } catch (err: any) {
    error.value = 'Service unavailable. Please verify connectivity.';
  } finally {
    loading.value = false;
  }
};

onMounted(() => fetchEvents());

const filteredEvents = computed(() => {
  let result = [...events.value];
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase();
    result = result.filter(e =>
      e.title.toLowerCase().includes(q) ||
      e.sport_category.toLowerCase().includes(q) ||
      (e.venue_city && e.venue_city.toLowerCase().includes(q))
    );
  }
  if (budgetFilter.value !== 'all') {
    result = result.map(e => ({ ...e, _dePrioritize: e.price_tier !== budgetFilter.value }))
      .sort((a, b) => Number(a._dePrioritize) - Number(b._dePrioritize));
  } else {
    result = result.map(e => ({ ...e, _dePrioritize: false }));
  }
  return result;
});
</script>

<style scoped>
/* ── Page shell ── */
.home-page {
  min-height: 100vh;
  background: var(--bg-site);
  color: var(--text-main);
  position: relative;
  display: flex;
  flex-direction: column;
  transition: background 0.3s ease;
}

.home-content {
  position: relative;
  z-index: 10;
  padding-top: 8rem;
  padding-bottom: 6rem;
  flex: 1;
}

/* ── Background ── */
.home-bg {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}

.home-bg-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: top;
  opacity: 0.12;
}

[data-theme="light"] .home-bg-img { opacity: 0.04; }

.home-bg-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, rgba(0,0,0,0.88) 0%, rgba(0,0,0,0.75) 50%, #000 100%);
}

[data-theme="light"] .home-bg-overlay {
  background: linear-gradient(to bottom,
    rgba(241,245,249,0.97) 0%,
    rgba(241,245,249,0.95) 50%,
    rgba(241,245,249,1) 100%);
}

/* ── Header ── */
.header-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.4rem 1rem;
  border-radius: 9999px;
  border: 1px solid var(--border-subtle);
  background: var(--bg-panel);
  margin-bottom: 1.5rem;
}

.header-badge span {
  font-size: 0.65rem;
  font-weight: 900;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--brand-accent);
}

.home-title {
  font-size: clamp(2.8rem, 7vw, 5.5rem);
  font-weight: 900;
  letter-spacing: -0.04em;
  line-height: 0.95;
  color: var(--text-primary);
  margin-bottom: 1.5rem;
}

.title-gradient {
  background: linear-gradient(90deg, #00f3ff, #ccff00, #00f3ff);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

[data-theme="light"] .title-gradient {
  background: linear-gradient(90deg, #0284c7, #7c3aed, #0284c7);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

@keyframes gradient-x {
  0%, 100% { background-position: 0% 50%; }
  50%       { background-position: 100% 50%; }
}
.animate-gradient-x { animation: gradient-x 6s ease infinite; }

.home-sub {
  font-size: clamp(1rem, 2vw, 1.2rem);
  color: var(--text-dim);
  font-weight: 500;
  max-width: 42rem;
  line-height: 1.65;
}

/* ── Search panel ── */
.search-panel {
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-radius: 1.5rem;
  padding: 1.5rem 2rem;
  backdrop-filter: blur(24px);
}

[data-theme="light"] .search-panel {
  background: #ffffff;
  border-color: #cbd5e1;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

.filter-label {
  display: block;
  font-size: 0.62rem;
  font-weight: 900;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  margin-bottom: 0.75rem;
}

.search-input {
  width: 100%;
  background: var(--bg-panel-light);
  border: 1px solid var(--border-subtle);
  border-radius: 1rem;
  padding: 1rem 1.5rem;
  color: var(--text-primary);
  font-size: 1rem;
  font-family: inherit;
  font-weight: 500;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

[data-theme="light"] .search-input {
  background: #ffffff;
  border: 2px solid #94a3b8;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

.search-input::placeholder { color: var(--text-muted); }

.search-input:focus {
  border-color: var(--brand-accent);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--brand-accent) 10%, transparent);
}

[data-theme="light"] .search-input:focus {
  border-color: var(--brand-accent);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--brand-accent) 12%, transparent);
}

[data-theme="dark"] .search-input option { background: #1c1c1f; color: #f8fafc; }
[data-theme="light"] .search-input option { background: #ffffff; color: #0f172a; }

/* ── Lineup header ── */
.lineup-title {
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 900;
  letter-spacing: -0.04em;
  color: var(--text-primary);
}

.lineup-count {
  font-weight: 700;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--text-muted);
}

/* ── Loading / error ── */
.home-spinner {
  width: 44px;
  height: 44px;
  border: 3px solid var(--border-subtle);
  border-top-color: var(--brand-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.state-label {
  font-size: 0.75rem;
  font-weight: 800;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--text-muted);
}

.error-panel {
  background: rgba(239,68,68,0.07);
  border: 1px solid rgba(239,68,68,0.2);
  border-radius: 1.5rem;
  padding: 3rem;
}

.retry-btn {
  background: var(--text-primary);
  color: var(--bg-site);
  font-weight: 900;
  padding: 0.75rem 2rem;
  border-radius: 9999px;
  border: none;
  cursor: pointer;
  transition: opacity 0.15s ease, transform 0.15s ease;
}

.retry-btn:hover { opacity: 0.85; transform: scale(1.03); }
</style>
