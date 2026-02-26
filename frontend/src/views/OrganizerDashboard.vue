<template>
  <div class="organizer-dashboard">
    <div class="container py-12">
      <div class="dashboard-header-corp mb-12 animate-corp">
        <div class="header-text">
          <span class="badge-corp">Management Console</span>
          <h1 class="hero-title-small mt-4">Architect Dashboard</h1>
          <p class="text-dim mt-2">Precision monitoring of your event portfolio and revenue stream.</p>
        </div>
        <router-link to="/organizer/create" class="btn-corp btn-corp-primary">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
          Deploy New Event
        </router-link>
      </div>

      <div v-if="loading" class="loading-corp-full">
        <div class="pulse-loader"></div>
        <span>fetching Dashboard intelligence...</span>
      </div>
      
      <div v-else-if="error" class="error-panel-inline mb-12">{{ error }}</div>
      
      <div v-else class="dashboard-grid">
        <!-- FEATURE: FOUNDER ADMIN KPIs -->
        <section v-if="authStore.isFounder" class="kpi-grid-corp span-2 mb-8 animate-corp border border-brand-primary/20 rounded-2xl bg-gradient-to-br from-brand-primary/10 to-transparent p-6 shadow-[0_0_30px_rgba(0,240,255,0.05)]">
          <h2 class="label-muted mb-6 text-brand-primary w-full col-span-4 tracking-widest">Platform Overview (Founder Rights)</h2>
          <div class="card-premium kpi-card-corp bg-black/60 shadow-inner border-white/5">
            <span class="label-muted mb-4 opacity-70">Platform Users</span>
            <span class="kpi-val-corp text-white text-4xl">{{ adminOverview.total_users }}</span>
          </div>
          <div class="card-premium kpi-card-corp bg-black/60 shadow-inner border-white/5">
            <span class="label-muted mb-4 opacity-70">Platform Events</span>
            <span class="kpi-val-corp text-white text-4xl">{{ adminOverview.total_events }}</span>
          </div>
          <div class="card-premium kpi-card-corp bg-black/60 shadow-inner border-white/5">
            <span class="label-muted mb-4 opacity-70">Platform Regs</span>
            <span class="kpi-val-corp text-white text-4xl">{{ adminOverview.total_registrations }}</span>
          </div>
          <div class="card-premium kpi-card-corp bg-black/60 shadow-inner border-white/5">
            <span class="label-muted mb-4 opacity-70">Top Sport</span>
            <span class="kpi-val-corp text-brand-primary text-2xl font-800">{{ adminOverview.most_popular_sport || 'N/A' }}</span>
          </div>
        </section>

        <!-- Feature 11: Ticket Sales Summary KPI -->
        <section class="kpi-grid-corp span-2 mb-12 animate-corp delay-50">
          <div class="card-premium kpi-card-corp hover:border-brand-primary/50 transition-all">
            <span class="label-muted mb-4">Total Capacity Units</span>
            <span class="kpi-val-corp text-gradient text-5xl">{{ totalCapacity }}</span>
          </div>
          <div class="card-premium kpi-card-corp hover:border-brand-primary/50 transition-all">
            <span class="label-muted mb-4">Commitments Secured</span>
            <span class="kpi-val-corp text-gradient text-5xl">{{ totalRegistrations }}</span>
          </div>
          <div class="card-premium kpi-card-corp hover:border-brand-primary/50 transition-all">
            <span class="label-muted mb-4">Aggregate Fill Rate</span>
            <span class="kpi-val-corp text-gradient text-5xl">{{ aggregateFillRate }}%</span>
          </div>
          <div class="card-premium kpi-card-corp hover:border-brand-primary/50 transition-all">
            <span class="label-muted mb-4">Grand Yield</span>
            <span class="kpi-val-corp text-gradient text-4xl">₹{{ totalRevenue.toLocaleString() }}</span>
          </div>
        </section>

        <!-- Overview Table -->
        <section class="card-premium span-2 animate-corp delay-100">
          <div class="section-header-corp mb-8">
            <h2 class="label-muted">Active Event Parameters</h2>
          </div>
          <div class="table-wrapper-corp">
            <table class="table-corp">
              <thead>
                <tr>
                  <th>Event Designation</th>
                  <th>Timeline</th>
                  <th>Bio-Region</th>
                  <th>Units</th>
                  <th>Cap</th>
                  <th>Yield (₹)</th>
                  <th>Efficiency</th>
                  <th v-if="authStore.isFounder">Visibility</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="event in events" :key="event.event_id">
                  <td class="font-800">{{ event.title }}</td>
                  <td>{{ new Date(event.event_date).toLocaleDateString('en-GB') }}</td>
                  <td>{{ event.venue_city }}</td>
                  <td>{{ event.registrations }}</td>
                  <td>{{ event.capacity }}</td>
                  <td class="text-gradient font-800">{{ event.revenue }}</td>
                  <td>
                    <span class="badge-corp-small" :class="event.performance_label.toLowerCase()">
                      {{ event.performance_label }}
                    </span>
                  </td>
                  <td v-if="authStore.isFounder">
                    <button 
                      @click="toggleFeatureEvent(event)" 
                      class="badge-corp-small !cursor-pointer transition-all hover:brightness-125"
                      :class="event.is_featured ? 'high' : 'medium'"
                    >
                      {{ event.is_featured ? 'Featured' : 'Standard' }}
                    </button>
                  </td>
                </tr>
                <tr v-if="events.length === 0">
                  <td colspan="8" class="text-center py-10 text-muted">No active registrations found.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Charts Segment -->
        <div class="charts-column span-2 grid-inner" v-if="events.length > 0">
          <section class="card-premium animate-corp delay-200">
            <h2 class="label-muted mb-8">Registration Pulse</h2>
            <div class="selector-corp mb-8">
              <label class="label-muted mb-4">Target Designation</label>
              <select v-model="selectedEventId" @change="fetchTrendData" class="input-corp">
                <option v-for="event in events" :key="event.event_id" :value="event.event_id">
                  {{ event.title }}
                </option>
              </select>
            </div>
            <div v-if="loadingTrend" class="text-center py-8">
               <div class="pulse-loader small mx-auto"></div>
            </div>
            <RegistrationTrend v-else :data="trendData" />
          </section>

          <section class="card-premium animate-corp delay-300">
            <h2 class="label-muted mb-8">Market Segmentation</h2>
            <CategoryBarChart :data="categoryData" />
          </section>
        </div>

        <!-- Promotion Panel (US-09) -->
        <section v-if="authStore.isFounder && promotedEvents.length > 0" class="card-premium span-2 animate-corp mb-8 border border-[#ff007f]/30">
          <div class="section-header-corp mb-6">
            <h2 class="label-muted text-[#ff007f] tracking-widest font-900">Active Promotion Campaigns</h2>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="promo in promotedEvents" :key="promo.event_id" class="p-6 bg-black/40 rounded-2xl border border-white/10">
              <h3 class="font-900 text-lg mb-4 text-white">{{ promo.title }}</h3>
              <div class="flex justify-between items-center mb-2">
                <span class="text-sm text-dim">Pre-Promotion:</span>
                <span class="font-800 text-xl">{{ promo.snapshot_registrations }}</span>
              </div>
              <div class="flex justify-between items-center mb-4">
                <span class="text-sm text-dim">Current:</span>
                <span class="font-800 text-xl text-brand-primary">{{ getEventCurrentRegistrations(promo.event_id) }}</span>
              </div>
              <div class="text-xs text-dim italic">
                Promoted at: {{ new Date(promo.timestamp).toLocaleTimeString() }}
              </div>
            </div>
          </div>
        </section>

        <!-- Charts Row 2: Revenue & Capacity -->
        <div class="charts-column span-2 grid-inner" v-if="events.length > 0">
          <section class="card-premium animate-corp delay-400">
            <h2 class="label-muted mb-8">Revenue per Event</h2>
            <RevenuePerEventChart :data="events" />
          </section>

          <section class="card-premium animate-corp delay-400">
            <h2 class="label-muted mb-8">Capacity Utilization</h2>
            <CapacityChart :data="events" />
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import { organizerApi, adminApi } from '../services/api';
import RegistrationTrend from '../components/charts/RegistrationTrend.vue';
import CategoryBarChart from '../components/charts/CategoryBarChart.vue';
import RevenuePerEventChart from '../components/charts/RevenuePerEventChart.vue';
import CapacityChart from '../components/charts/CapacityChart.vue';

const authStore = useAuthStore();
const loading = ref(true);
const loadingTrend = ref(false);
const error = ref('');

const events = ref<any[]>([]);
const categoryData = ref<any[]>([]);
const trendData = ref<any[]>([]);
const selectedEventId = ref<number | null>(null);

const adminOverview = ref<any>({});
const promotedEvents = ref<any[]>([]);
let pollInterval: any;

const totalCapacity = computed(() => events.value.reduce((acc, e) => acc + e.capacity, 0));
const totalRegistrations = computed(() => events.value.reduce((acc, e) => acc + e.registrations, 0));
const totalRevenue = computed(() => events.value.reduce((acc, e) => acc + e.revenue, 0));
const aggregateFillRate = computed(() => {
    if (totalCapacity.value === 0) return 0;
    return round((totalRegistrations.value / totalCapacity.value) * 100, 1);
});

function round(val: number, precision: number) {
    const multiplier = Math.pow(10, precision || 0);
    return Math.round(val * multiplier) / multiplier;
}

const fetchDashboardData = async (isPolling = false) => {
    if (!isPolling) loading.value = true;
    error.value = '';
    try {
        const promises = [
            organizerApi.getDashboard(),
            organizerApi.getCategoryInsight()
        ];

        if (authStore.isFounder || authStore.isAdmin) {
             promises.push(adminApi.getDashboard());
        }

        const resArray = await Promise.all(promises);

        events.value = resArray[0].data;
        categoryData.value = resArray[1].data;
        
        if (authStore.isFounder || authStore.isAdmin) {
            adminOverview.value = resArray[2].data;
        }

        if (events.value.length > 0 && !isPolling) {
            selectedEventId.value = events.value[0].event_id;
            await fetchTrendData();
        }

    } catch (err: any) {
        if (!isPolling) error.value = 'Failed to synchronize dashboard telemetry.';
    } finally {
        if (!isPolling) loading.value = false;
    }
};

const toggleFeatureEvent = async (event: any) => {
    try {
        const res = await organizerApi.toggleFeature(event.event_id);
        event.is_featured = res.data.is_featured;
        
        if (event.is_featured) {
            // Add to promotion tracking
            promotedEvents.value.push({
                event_id: event.event_id,
                title: event.title,
                snapshot_registrations: res.data.snapshot_registrations,
                timestamp: Date.now()
            });
        } else {
            // Remove from tracking
            promotedEvents.value = promotedEvents.value.filter(p => p.event_id !== event.event_id);
        }
    } catch (e) {
        alert('Failed to toggle feature status');
    }
};

const getEventCurrentRegistrations = (eventId: number) => {
    const ev = events.value.find(e => e.event_id === eventId);
    return ev ? ev.registrations : 0;
};

const fetchTrendData = async () => {
    if (!selectedEventId.value) return;
    loadingTrend.value = true;
    try {
        const res = await organizerApi.getTrend(selectedEventId.value);
        trendData.value = res.data;
    } catch (err) {
        console.error("Trend synchronization failed", err);
    } finally {
        loadingTrend.value = false;
    }
};

onMounted(() => {
    fetchDashboardData();
    // US-02: Organizer Real-Time Polling 
    pollInterval = setInterval(() => {
        fetchDashboardData(true);
    }, 5000); // 5 seconds
});

onUnmounted(() => {
    if (pollInterval) clearInterval(pollInterval);
});
</script>

<style scoped>
.organizer-dashboard {
  background-color: var(--bg-site);
  min-height: 100vh;
}

.dashboard-header-corp {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.grid-inner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.span-2 { grid-column: span 2; }

.kpi-grid-corp {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.kpi-card-corp {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
}

.kpi-val-corp {
  font-size: 1.75rem;
  font-weight: 900;
  line-height: 1;
  letter-spacing: -0.04em;
}

.font-800 { font-weight: 800; }

.table-wrapper-corp {
  overflow-x: auto;
}

.table-corp {
  width: 100%;
}

.table-corp th {
  text-align: left;
  padding: 0.75rem 1rem;
  font-size: 0.65rem;
  text-transform: uppercase;
  color: var(--text-muted);
  letter-spacing: 0.1em;
  border-bottom: 1px solid var(--border-subtle);
}

.badge-corp-small {
  padding: 0.4rem 0.8rem;
  font-size: 0.65rem;
  font-weight: 800;
  border-radius: var(--radius-pill);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.badge-corp-small.high { background: rgba(0, 223, 216, 0.1); color: var(--brand-secondary); }
.badge-corp-small.medium { background: rgba(255, 171, 0, 0.1); color: #ffab00; }
.badge-corp-small.low { background: rgba(255, 85, 85, 0.1); color: #ff5555; }

.loading-corp-full {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 60px 0;
  color: var(--text-dim);
}

.pulse-loader.small {
  width: 24px;
  height: 24px;
}

.card-premium {
  padding: 2rem;
}

@media (max-width: 1200px) {
  .dashboard-header-corp {
    flex-direction: column;
    align-items: flex-start;
    gap: 2rem;
  }
  .grid-inner {
    grid-template-columns: 1fr;
  }
}
</style>
