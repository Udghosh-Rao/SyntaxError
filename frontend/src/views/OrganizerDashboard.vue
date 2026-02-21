<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Topbar -->
    <header class="sticky top-0 z-40 border-b border-gray-100 bg-white/90 backdrop-blur-sm">
      <div class="mx-auto max-w-6xl px-6 h-14 flex items-center justify-between">
        <span class="font-bold text-sm text-gray-900">SportsSync <span class="text-gray-400 font-normal">· Organizer</span></span>
        <div class="flex items-center gap-3">
          <span class="text-xs text-gray-500 hidden sm:block">{{ authStore.userName }}</span>
          <button @click="handleLogout" class="px-3 py-1.5 text-xs font-medium border border-gray-200 rounded-lg text-gray-600 hover:bg-gray-50 transition">Logout</button>
        </div>
      </div>
    </header>

    <main class="mx-auto max-w-6xl px-6 py-8">
      <h1 class="text-xl font-bold text-gray-900 mb-1">Organizer Dashboard</h1>
      <p class="text-sm text-gray-500 mb-6">Manage events and track performance.</p>

      <!-- Tabs -->
      <div class="flex gap-1 bg-gray-100 rounded-xl p-1 mb-8 overflow-x-auto">
        <button
          v-for="tab in tabs" :key="tab.id"
          @click="activeTab = tab.id"
          class="flex-1 min-w-max px-4 py-2 rounded-lg text-xs font-medium transition whitespace-nowrap"
          :class="activeTab === tab.id ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500 hover:text-gray-700'"
        >{{ tab.icon }} {{ tab.label }}</button>
      </div>

      <!-- Dashboard -->
      <div v-if="activeTab === 'dashboard'">
        <!-- Stats row -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div class="stat-card" v-for="s in summaryCards" :key="s.label">
            <div class="text-2xl font-bold text-gray-900">{{ s.value }}</div>
            <div class="text-xs text-gray-400 mt-0.5">{{ s.label }}</div>
          </div>
        </div>
        <!-- Table -->
        <div class="bg-white rounded-xl border border-gray-100 shadow-card overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full text-xs">
              <thead class="bg-gray-50 border-b border-gray-100">
                <tr>
                  <th class="text-left px-4 py-3 text-gray-500 font-medium" v-for="h in ['Event', 'Date', 'City', 'Registrations', 'Fill Rate', 'Revenue', 'Status']" :key="h">{{ h }}</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-50">
                <tr v-for="e in events" :key="e.event_id" class="hover:bg-gray-50 transition">
                  <td class="px-4 py-3 font-medium text-gray-900">{{ e.title }}</td>
                  <td class="px-4 py-3 text-gray-500">{{ fmt(e.event_date) }}</td>
                  <td class="px-4 py-3 text-gray-500">{{ e.venue_city }}</td>
                  <td class="px-4 py-3 text-gray-700">{{ e.registrations }}/{{ e.capacity }}</td>
                  <td class="px-4 py-3">
                    <div class="flex items-center gap-2">
                      <div class="w-16 h-1 bg-gray-100 rounded-full overflow-hidden"><div class="h-full bg-gray-900 rounded-full" :style="`width:${e.fill_rate}%`"></div></div>
                      <span class="text-gray-600">{{ e.fill_rate }}%</span>
                    </div>
                  </td>
                  <td class="px-4 py-3 text-gray-700">₹{{ (e.revenue||0).toLocaleString('en-IN') }}</td>
                  <td class="px-4 py-3">
                    <span class="badge" :class="e.performance_label?.toLowerCase()==='hot' ? 'badge-green':'badge-yellow'">{{ e.performance_label }}</span>
                  </td>
                </tr>
                <tr v-if="!events.length"><td colspan="7" class="px-4 py-8 text-center text-gray-400">No events yet. Create one below.</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Create Event -->
      <div v-if="activeTab === 'create'">
        <div class="bg-white rounded-xl border border-gray-100 shadow-card p-6 max-w-lg">
          <h2 class="text-sm font-semibold text-gray-900 mb-5">Create New Event</h2>
          <form @submit.prevent="handleCreateEvent" class="space-y-4">
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1.5">Event Title</label>
              <input v-model="newEvent.title" class="input" placeholder="Mumbai Football Championship" required />
            </div>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1.5">Sport</label>
                <select v-model="newEvent.sport_category" class="input">
                  <option v-for="s in sportsList" :key="s" :value="s">{{ s }}</option>
                </select>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1.5">City</label>
                <input v-model="newEvent.venue_city" class="input" placeholder="Mumbai" required />
              </div>
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1.5">Venue Address</label>
              <input v-model="newEvent.venue_address" class="input" placeholder="Wankhede Stadium" />
            </div>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1.5">Date & Time</label>
                <input v-model="newEvent.event_date" type="datetime-local" class="input" required />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1.5">Price (₹)</label>
                <input v-model.number="newEvent.price" type="number" min="0" class="input" placeholder="500" required />
              </div>
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1.5">Capacity</label>
              <input v-model.number="newEvent.capacity" type="number" min="1" class="input" placeholder="100" required />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1.5">Description</label>
              <textarea v-model="newEvent.description" class="input resize-none" rows="3" placeholder="Tell participants about your event…"></textarea>
            </div>
            <div v-if="createError" class="text-xs text-red-600 bg-red-50 border border-red-100 rounded-lg px-3 py-2">{{ createError }}</div>
            <div v-if="createSuccess" class="text-xs text-green-700 bg-green-50 border border-green-100 rounded-lg px-3 py-2">{{ createSuccess }}</div>
            <button type="submit" :disabled="createLoading"
              class="px-5 py-2.5 bg-gray-900 text-white text-sm font-semibold rounded-lg hover:bg-gray-800 disabled:opacity-50 transition shadow-btn">
              {{ createLoading ? 'Creating…' : '+ Create Event' }}
            </button>
          </form>
        </div>
      </div>

      <!-- Trend (Feature 10) -->
      <div v-if="activeTab === 'trend'">
        <div class="bg-white rounded-xl border border-gray-100 shadow-card p-6">
          <h2 class="text-sm font-semibold text-gray-900 mb-4">Daily Registration Trend</h2>
          <select v-model="selectedEventId" class="input max-w-xs mb-6" @change="loadTrend">
            <option value="">Select an event…</option>
            <option v-for="e in events" :key="e.event_id" :value="e.event_id">{{ e.title }}</option>
          </select>
          <div v-if="trendData.length" style="height:260px;"><BarChart :data="trendChartData" /></div>
          <p v-else class="text-sm text-gray-400">Select an event to see its trend.</p>
        </div>
      </div>

      <!-- Ticket Summary (Feature 11) -->
      <div v-if="activeTab === 'tickets'">
        <div class="bg-white rounded-xl border border-gray-100 shadow-card overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full text-xs">
              <thead class="bg-gray-50 border-b border-gray-100">
                <tr>
                  <th class="text-left px-4 py-3 text-gray-500 font-medium" v-for="h in ['Event', 'Capacity', 'Sold', '% Filled', 'Revenue']" :key="h">{{ h }}</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-50">
                <tr v-for="e in ticketSummary" :key="e.event_id" class="hover:bg-gray-50">
                  <td class="px-4 py-3 font-medium text-gray-900">{{ e.title }}</td>
                  <td class="px-4 py-3 text-gray-500">{{ e.capacity }}</td>
                  <td class="px-4 py-3 text-gray-700">{{ e.seats_sold }}</td>
                  <td class="px-4 py-3">
                    <div class="flex items-center gap-2">
                      <div class="w-16 h-1 bg-gray-100 rounded-full overflow-hidden"><div class="h-full bg-gray-900 rounded-full" :style="`width:${e.percentage_filled}%`"></div></div>
                      {{ e.percentage_filled }}%
                    </div>
                  </td>
                  <td class="px-4 py-3 text-gray-700">₹{{ (e.revenue||0).toLocaleString('en-IN') }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Category Insight (Feature 12) -->
      <div v-if="activeTab === 'category'">
        <div class="bg-white rounded-xl border border-gray-100 shadow-card p-6">
          <h2 class="text-sm font-semibold text-gray-900 mb-5">Popular Sport Categories</h2>
          <div v-if="categoryData.length" style="height:280px;"><DoughnutChart :data="catChartData" /></div>
          <p v-else class="text-sm text-gray-400">No registration data yet.</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import BarChart from '@/components/BarChart.vue'
import DoughnutChart from '@/components/DoughnutChart.vue'

const router = useRouter(); const authStore = useAuthStore()
const tabs = [
  { id:'dashboard', icon:'📊', label:'Events' }, { id:'create', icon:'➕', label:'Create Event' },
  { id:'trend', icon:'📈', label:'Trend' }, { id:'tickets', icon:'🎟', label:'Tickets' }, { id:'category', icon:'🏅', label:'Categories' },
]
const activeTab = ref('dashboard')
const events = ref([]); const ticketSummary = ref([]); const categoryData = ref([]); const trendData = ref([]); const selectedEventId = ref('')
const createLoading = ref(false); const createError = ref(''); const createSuccess = ref('')
const sportsList = ['Football','Cricket','Tennis','Basketball','Running','Badminton','Swimming','Cycling']
const newEvent = ref({ title:'', sport_category:'Football', venue_city:'', venue_address:'', event_date:'', price:'', capacity:'', description:'' })

const summaryCards = computed(() => {
  const e = events.value
  return [
    { label:'Total Events', value: e.length },
    { label:'Registrations', value: e.reduce((a,ev)=>a+ev.registrations,0) },
    { label:'Revenue', value: '₹'+e.reduce((a,ev)=>a+(ev.revenue||0),0).toLocaleString('en-IN') },
    { label:'Avg Fill Rate', value: e.length ? Math.round(e.reduce((a,ev)=>a+ev.fill_rate,0)/e.length)+'%':'0%' },
  ]
})
const trendChartData = computed(() => ({ labels:trendData.value.map(d=>d.day), datasets:[{ label:'Registrations', data:trendData.value.map(d=>d.count), backgroundColor:'#111827', borderRadius:4 }] }))
const catChartData = computed(() => ({ labels:categoryData.value.map(d=>d.sport_category), datasets:[{ data:categoryData.value.map(d=>d.registration_count), backgroundColor:['#22c55e','#f59e0b','#3b82f6','#ef4444','#8b5cf6','#6366f1','#06b6d4','#f97316'] }] }))

function fmt(d) { return new Date(d).toLocaleDateString('en-IN',{day:'numeric',month:'short',year:'numeric'}) }

async function loadTrend() { if (!selectedEventId.value) return; const r = await api.get(`/organizer/trend/${selectedEventId.value}`); trendData.value = r.data }

async function handleCreateEvent() {
  createLoading.value = true; createError.value = ''; createSuccess.value = ''
  try {
    await api.post('/events', { ...newEvent.value })
    createSuccess.value = 'Event created successfully!'
    Object.assign(newEvent.value, { title:'', venue_city:'', venue_address:'', event_date:'', price:'', capacity:'', description:'' })
    const r = await api.get('/organizer/dashboard'); events.value = r.data
  } catch (e) { createError.value = e.response?.data?.error || 'Failed to create event' }
  finally { createLoading.value = false }
}

function handleLogout() { authStore.logout(); router.push('/') }

onMounted(async () => {
  const [dash, tickets, cats] = await Promise.all([api.get('/organizer/dashboard'), api.get('/organizer/ticket-summary'), api.get('/organizer/category-insight')])
  events.value = dash.data; ticketSummary.value = tickets.data; categoryData.value = cats.data
})
</script>
