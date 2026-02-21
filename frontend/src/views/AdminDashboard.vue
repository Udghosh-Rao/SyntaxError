<template>
  <div class="min-h-screen bg-gray-50">
    <header class="sticky top-0 z-40 border-b border-gray-100 bg-white/90 backdrop-blur-sm">
      <div class="mx-auto max-w-6xl px-6 h-14 flex items-center justify-between">
        <span class="font-bold text-sm text-gray-900">SportsSync <span class="text-gray-400 font-normal">· Admin</span></span>
        <button @click="handleLogout" class="px-3 py-1.5 text-xs font-medium border border-gray-200 rounded-lg text-gray-600 hover:bg-gray-50 transition">Logout</button>
      </div>
    </header>

    <main class="mx-auto max-w-6xl px-6 py-8">
      <h1 class="text-xl font-bold text-gray-900 mb-1">Admin Dashboard</h1>
      <p class="text-sm text-gray-500 mb-6">Platform-wide analytics and management.</p>

      <!-- Tabs -->
      <div class="flex gap-1 bg-gray-100 rounded-xl p-1 mb-8 overflow-x-auto">
        <button
          v-for="tab in tabs" :key="tab.id"
          @click="activeTab = tab.id"
          class="flex-1 min-w-max px-3 py-2 rounded-lg text-xs font-medium transition whitespace-nowrap"
          :class="activeTab === tab.id ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500 hover:text-gray-700'"
        >{{ tab.icon }} {{ tab.label }}</button>
      </div>

      <!-- Overview (Feature 13) -->
      <div v-if="activeTab === 'overview'">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="stat-card">
            <div class="text-2xl font-bold text-gray-900">{{ analytics.total_users }}</div>
            <div class="text-xs text-gray-400 mt-0.5">Total Users</div>
          </div>
          <div class="stat-card">
            <div class="text-2xl font-bold text-gray-900">{{ analytics.total_events }}</div>
            <div class="text-xs text-gray-400 mt-0.5">Active Events</div>
          </div>
          <div class="stat-card">
            <div class="text-2xl font-bold text-gray-900">{{ analytics.total_registrations }}</div>
            <div class="text-xs text-gray-400 mt-0.5">Registrations</div>
          </div>
          <div class="stat-card">
            <div class="text-2xl font-bold text-gray-900">₹{{ (analytics.total_revenue||0).toLocaleString('en-IN') }}</div>
            <div class="text-xs text-gray-400 mt-0.5">Platform Revenue</div>
          </div>
        </div>
      </div>

      <!-- Popular Sports (Feature 14) -->
      <div v-if="activeTab === 'sports'">
        <div class="bg-white rounded-xl border border-gray-100 shadow-card p-6">
          <h2 class="text-sm font-semibold text-gray-900 mb-5">Sports by Registrations</h2>
          <div v-if="popularSports.length" style="height:280px;"><BarChart :data="sportsChartData" /></div>
          <p v-else class="text-sm text-gray-400">No data yet.</p>
        </div>
      </div>

      <!-- City Distribution (Feature 15) -->
      <div v-if="activeTab === 'cities'">
        <div class="bg-white rounded-xl border border-gray-100 shadow-card p-6">
          <h2 class="text-sm font-semibold text-gray-900 mb-5">Users by City</h2>
          <div v-if="cityDist.length" style="height:280px;"><DoughnutChart :data="cityChartData" /></div>
          <table class="min-w-full text-xs mt-6">
            <thead class="border-b border-gray-100">
              <tr><th class="text-left py-2 text-gray-500 font-medium">City</th><th class="text-left py-2 text-gray-500 font-medium">Users</th></tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-for="c in cityDist" :key="c.city"><td class="py-2 text-gray-700">{{ c.city }}</td><td class="py-2 text-gray-900 font-medium">{{ c.user_count }}</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Fill Rate (Feature 16) -->
      <div v-if="activeTab === 'fillrate'">
        <div class="bg-white rounded-xl border border-gray-100 shadow-card overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full text-xs">
              <thead class="bg-gray-50 border-b border-gray-100">
                <tr>
                  <th class="text-left px-4 py-3 text-gray-500 font-medium" v-for="h in ['Event','Organizer','Capacity','Filled','Rate','Status']" :key="h">{{ h }}</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-50">
                <tr v-for="e in fillRate" :key="e.event_id" class="hover:bg-gray-50">
                  <td class="px-4 py-3 font-medium text-gray-900">{{ e.title }}</td>
                  <td class="px-4 py-3 text-gray-500">{{ e.organizer_name }}</td>
                  <td class="px-4 py-3 text-gray-500">{{ e.capacity }}</td>
                  <td class="px-4 py-3 text-gray-700">{{ e.seats_filled }}</td>
                  <td class="px-4 py-3">
                    <div class="flex items-center gap-2">
                      <div class="w-16 h-1 bg-gray-100 rounded-full overflow-hidden"><div class="h-full bg-gray-900 rounded-full" :style="`width:${e.fill_rate}%`"></div></div>
                      {{ e.fill_rate }}%
                    </div>
                  </td>
                  <td class="px-4 py-3">
                    <span class="badge" :class="e.performance_label?.toLowerCase()==='hot'?'badge-green':e.performance_label?.toLowerCase()==='warm'?'badge-yellow':'badge-gray'">{{ e.performance_label }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Monthly Trend (Feature 17) -->
      <div v-if="activeTab === 'trend'">
        <div class="bg-white rounded-xl border border-gray-100 shadow-card p-6">
          <h2 class="text-sm font-semibold text-gray-900 mb-5">Monthly Registrations (12 Months)</h2>
          <div v-if="monthlyTrend.length" style="height:280px;"><BarChart :data="trendChartData" /></div>
          <p v-else class="text-sm text-gray-400">No data yet.</p>
        </div>
      </div>

      <!-- Organizer Performance (Feature 18) -->
      <div v-if="activeTab === 'organizers'">
        <div class="bg-white rounded-xl border border-gray-100 shadow-card overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full text-xs">
              <thead class="bg-gray-50 border-b border-gray-100">
                <tr>
                  <th class="text-left px-4 py-3 text-gray-500 font-medium" v-for="h in ['Organizer','Events','Registrations','Revenue']" :key="h">{{ h }}</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-50">
                <tr v-for="o in orgPerf" :key="o.organizer_id" class="hover:bg-gray-50">
                  <td class="px-4 py-3 font-medium text-gray-900">{{ o.organizer_name }}</td>
                  <td class="px-4 py-3 text-gray-500">{{ o.total_events }}</td>
                  <td class="px-4 py-3 text-gray-700">{{ o.total_registrations }}</td>
                  <td class="px-4 py-3 font-semibold text-gray-900">₹{{ o.total_revenue.toLocaleString('en-IN') }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Escalations -->
      <div v-if="activeTab === 'escalations'">
        <div v-if="escalations.length" class="space-y-3">
          <div v-for="t in escalations" :key="t.id"
            class="bg-white rounded-xl border border-gray-100 shadow-card p-4 flex items-start justify-between gap-4">
            <div>
              <p class="text-xs font-semibold text-gray-900 mb-0.5">Ticket #{{ t.id }}</p>
              <p class="text-xs text-gray-500 leading-relaxed">{{ t.query }}</p>
              <p class="text-[10px] text-gray-400 mt-1.5">{{ t.created_at }}</p>
            </div>
            <button @click="resolveTicket(t.id)"
              class="px-3 py-1.5 text-xs font-medium border border-gray-200 rounded-lg text-gray-600 hover:bg-gray-50 transition whitespace-nowrap">
              Resolve
            </button>
          </div>
        </div>
        <div v-else class="py-16 text-center">
          <p class="text-2xl mb-2">🎉</p>
          <p class="text-sm font-medium text-gray-900">No open escalations</p>
          <p class="text-xs text-gray-400 mt-1">All chatbot tickets have been resolved.</p>
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
  {id:'overview',icon:'📊',label:'Overview'},{id:'sports',icon:'🏆',label:'Popular Sports'},
  {id:'cities',icon:'🗺',label:'Cities'},{id:'fillrate',icon:'📋',label:'Fill Rates'},
  {id:'trend',icon:'📅',label:'Monthly Trend'},{id:'organizers',icon:'🏢',label:'Organizers'},
  {id:'escalations',icon:'💬',label:'Escalations'},
]
const activeTab = ref('overview')
const analytics = ref({total_users:0,total_events:0,total_registrations:0,total_revenue:0})
const popularSports = ref([]);const cityDist = ref([]);const fillRate = ref([])
const monthlyTrend = ref([]);const orgPerf = ref([]);const escalations = ref([])

const COLORS = ['#22c55e','#f59e0b','#3b82f6','#ef4444','#8b5cf6','#6366f1','#06b6d4','#f97316']
const sportsChartData = computed(()=>({labels:popularSports.value.map(d=>d.sport_category),datasets:[{label:'Registrations',data:popularSports.value.map(d=>d.registration_count),backgroundColor:'#111827',borderRadius:4}]}))
const cityChartData = computed(()=>({labels:cityDist.value.map(d=>d.city),datasets:[{data:cityDist.value.map(d=>d.user_count),backgroundColor:COLORS}]}))
const trendChartData = computed(()=>({labels:monthlyTrend.value.map(d=>d.month),datasets:[{label:'Registrations',data:monthlyTrend.value.map(d=>d.count),backgroundColor:'#111827',borderRadius:4}]}))

async function resolveTicket(id){ await api.put(`/admin/escalations/${id}/resolve`); escalations.value=escalations.value.filter(t=>t.id!==id) }
function handleLogout(){ authStore.logout(); router.push('/') }

onMounted(async()=>{
  const [a,s,c,f,m,o,e]=await Promise.all([
    api.get('/admin/analytics'),api.get('/admin/popular-sport'),api.get('/admin/city-distribution'),
    api.get('/admin/fill-rate'),api.get('/admin/monthly-trend'),api.get('/admin/organizer-performance'),api.get('/admin/escalations')
  ])
  analytics.value=a.data;popularSports.value=s.data;cityDist.value=c.data;fillRate.value=f.data;monthlyTrend.value=m.data;orgPerf.value=o.data;escalations.value=e.data
})
</script>
