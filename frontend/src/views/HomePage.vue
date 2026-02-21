<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Topbar -->
    <header class="sticky top-0 z-40 border-b border-gray-100 bg-white/90 backdrop-blur-sm">
      <div class="mx-auto max-w-6xl px-6 h-14 flex items-center justify-between">
        <span class="font-bold text-sm text-gray-900">SportsSync</span>
        <div class="flex items-center gap-3">
          <span class="text-xs text-gray-500 hidden sm:block">{{ authStore.userName }}</span>
          <button @click="handleLogout" class="px-3 py-1.5 text-xs font-medium border border-gray-200 rounded-lg text-gray-600 hover:bg-gray-50 transition">
            Logout
          </button>
        </div>
      </div>
    </header>

    <main class="mx-auto max-w-6xl px-6 py-8">
      <!-- Search -->
      <div class="relative mb-8">
        <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
          <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
        </div>
        <input
          v-model="searchQuery"
          type="text"
          class="w-full pl-10 pr-4 py-2.5 bg-white border border-gray-200 rounded-xl text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-900/10 focus:border-gray-300 transition"
          placeholder="Search events by sport, city, or keyword…"
          @input="handleSearch"
        />
        <!-- Algolia results dropdown -->
        <div v-if="searchQuery && searchResults.length" class="absolute top-full left-0 right-0 mt-1.5 bg-white border border-gray-100 rounded-xl shadow-card-hover overflow-hidden z-30">
          <router-link
            v-for="hit in searchResults" :key="hit.objectID"
            :to="`/event/${hit.objectID}`"
            class="flex items-center justify-between px-4 py-2.5 hover:bg-gray-50 transition"
          >
            <span class="text-sm font-medium text-gray-900">{{ hit.title }}</span>
            <span class="text-xs text-gray-400">{{ hit.sport_category }} · {{ hit.venue_city }}</span>
          </router-link>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-20">
        <div class="w-8 h-8 border-2 border-gray-200 border-t-gray-900 rounded-full animate-spin"></div>
      </div>

      <template v-else>
        <!-- This Week -->
        <section v-if="thisWeekEvents.length" class="mb-10">
          <div class="flex items-center gap-2 mb-4">
            <h2 class="text-sm font-semibold text-gray-900">Happening This Week</h2>
            <span class="badge badge-green">{{ thisWeekEvents.length }}</span>
          </div>
          <div class="snap-row">
            <EventCard v-for="e in thisWeekEvents" :key="e.id" :event="e" />
          </div>
        </section>

        <!-- Recommended -->
        <section class="mb-10">
          <h2 class="text-sm font-semibold text-gray-900 mb-4">Recommended For You</h2>
          <div v-if="topEvents.length" class="snap-row">
            <EventCard v-for="e in topEvents" :key="e.id" :event="e" />
          </div>
          <p v-else class="text-sm text-gray-400">No recommendations yet. Update your preferences!</p>
        </section>

        <!-- Nearby -->
        <section v-if="nearbyEvents.length" class="mb-10">
          <h2 class="text-sm font-semibold text-gray-900 mb-4">Near You</h2>
          <div class="snap-row">
            <EventCard v-for="e in nearbyEvents" :key="e.id" :event="e" />
          </div>
        </section>

        <!-- All Events -->
        <section>
          <h2 class="text-sm font-semibold text-gray-900 mb-4">All Events</h2>
          <div v-if="allEvents.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <EventCard v-for="e in allEvents" :key="e.id" :event="e" />
          </div>
          <div v-else class="py-16 text-center text-sm text-gray-400">No events available right now.</div>
        </section>
      </template>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useEventsStore } from '@/stores/events'
import EventCard from '@/components/EventCard.vue'
import { searchEvents } from '@/services/algolia'

const router = useRouter()
const authStore = useAuthStore()
const eventsStore = useEventsStore()
const loading = ref(true)
const searchQuery = ref('')
const searchResults = ref([])

const now = new Date()
const weekLater = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000)
const allEvents = computed(() => eventsStore.events)
const thisWeekEvents = computed(() => eventsStore.events.filter(e => { const d = new Date(e.event_date); return d >= now && d <= weekLater }))
const nearbyEvents = computed(() => {
  const city = authStore.userProfile?.city || ''
  if (!city) return []
  return eventsStore.events.filter(e => e.venue_city?.toLowerCase() === city.toLowerCase()).slice(0, 8)
})
const topEvents = computed(() => eventsStore.events.slice(0, 8))

let timer = null
async function handleSearch() {
  clearTimeout(timer)
  if (!searchQuery.value.trim()) { searchResults.value = []; return }
  timer = setTimeout(async () => { searchResults.value = await searchEvents(searchQuery.value) }, 300)
}
function handleLogout() { authStore.logout(); router.push('/') }
onMounted(async () => { await authStore.fetchProfile(); await eventsStore.fetchEvents(); loading.value = false })
</script>
