<template>
  <div class="admin-dashboard">
    <div class="luxury-bg-mesh">
      <div class="aura-blob aura-1"></div>
      <div class="aura-blob aura-2"></div>
      <div class="aura-blob aura-3"></div>
    </div>

    <div class="container py-12">
      <div class="dashboard-header-corp mb-12 animate-corp">
        <div class="header-text">
          <span class="badge-corp">Platform Intelligence</span>
          <h1 class="hero-title-small mt-4">Command Overview</h1>
          <p class="text-dim mt-2">High-level telemetry of platform operatives and architectural efficiency.</p>
        </div>
        <button @click="fetchData" class="btn-corp btn-corp-outline" :disabled="loading">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M23 4v6h-6"></path><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path></svg>
          Re-Sync Platform
        </button>
      </div>

      <div v-if="loading" class="loading-corp-full">
        <div class="pulse-loader"></div>
        <span>fetching System Analytics...</span>
      </div>
      
      <div v-else-if="error" class="error-panel-inline mb-12">{{ error }}</div>
      
      <div v-else class="dashboard-content">
        <!-- Feature 13: Top-level Platform Stats -->
        <section class="kpi-grid mb-12 animate-corp delay-100">
          <div class="card-premium kpi-card-corp hover:border-brand-accent/50 transition-all shadow-luxury relative overflow-hidden group">
             <div class="absolute inset-0 bg-gradient-to-br from-brand-accent/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <span class="label-muted mb-4 relative z-10 w-full col-span-4 tracking-widest text-[#7000ff]">Total Operatives</span>
            <span class="kpi-val-corp text-white relative z-10 text-5xl">{{ overview.total_users }}</span>
          </div>
          <div class="card-premium kpi-card-corp hover:border-brand-primary/50 transition-all shadow-luxury relative overflow-hidden group">
             <div class="absolute inset-0 bg-gradient-to-br from-brand-primary/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <span class="label-muted mb-4 relative z-10 w-full col-span-4 tracking-widest text-[#00f0ff]">Active Deployments</span>
            <span class="kpi-val-corp text-white relative z-10 text-5xl">{{ overview.total_events }}</span>
          </div>
          <div class="card-premium kpi-card-corp hover:border-brand-secondary/50 transition-all shadow-luxury relative overflow-hidden group">
             <div class="absolute inset-0 bg-gradient-to-br from-brand-secondary/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <span class="label-muted mb-4 relative z-10 w-full col-span-4 tracking-widest text-[#ff0055]">Total Commitments</span>
            <span class="kpi-val-corp text-white relative z-10 text-5xl">{{ overview.total_registrations }}</span>
          </div>
          <div class="card-premium kpi-card-corp hover:border-white/50 transition-all shadow-luxury relative overflow-hidden group">
             <div class="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <span class="label-muted mb-4 relative z-10 w-full col-span-4 tracking-widest">Aggregate Yield</span>
            <span class="kpi-val-corp text-white relative z-10 text-4xl mt-2 tracking-tight">₹{{ overview.total_revenue?.toLocaleString() }}</span>
          </div>
        </section>

        <!-- Charts Row 1 -->
        <div class="charts-row mb-12">
          <!-- Feature 17: Monthly Trend -->
          <section class="card-premium animate-corp delay-200">
            <h2 class="label-muted mb-10">Temporal Growth Trend</h2>
            <MonthlyTrendChart :data="monthlyTrend" />
          </section>
          
          <!-- Feature 15: City Distribution -->
          <section class="card-premium animate-corp delay-300">
            <h2 class="label-muted mb-10">Bio-Region Distribution</h2>
            <CityDistributionChart :data="cityData" />
          </section>

          <!-- Feature 14: Most Popular Sport Category -->
          <section class="card-premium animate-corp delay-300">
            <h2 class="label-muted mb-8">Sport Category Distribution</h2>
            <SportDonutChart :data="popularSports" />
          </section>
        </div>

        <!-- Feature 16: Fill Rates Chart -->
        <section class="card-premium mb-12 animate-corp delay-400">
           <h2 class="label-muted mb-8">Event Fill Rates</h2>
           <FillRateChart :data="fillRates" />
        </section>

        <!-- Feature 18: Organizer Comparison Chart -->
        <section class="card-premium mb-12 animate-corp delay-400">
          <h2 class="label-muted mb-8">Organizer Performance</h2>
          <OrganizerComparisonChart :data="topOrganizers" />
        </section>

        <!-- Organizer Leaderboard Table -->
        <section class="card-premium animate-corp delay-400">
          <h2 class="label-muted mb-10">Elite Architect Performance</h2>
          <div class="table-wrapper-corp">
            <table class="table-corp">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Architect Name</th>
                  <th>Deployments</th>
                  <th>Commitments</th>
                  <th>Total Yield (₹)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(org, i) in topOrganizers" :key="org.organizer_id">
                  <td class="text-dim font-800">#{{ i + 1 }}</td>
                  <td class="font-800">{{ org.organizer_name }}</td>
                  <td>{{ org.total_events }}</td>
                  <td>{{ org.total_registrations }}</td>
                  <td class="text-gradient font-900">₹{{ org.total_revenue.toLocaleString() }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';
import MonthlyTrendChart from '../components/charts/MonthlyTrendChart.vue';
import CityDistributionChart from '../components/charts/CityDistributionChart.vue';
import FillRateChart from '../components/charts/FillRateChart.vue';
import OrganizerComparisonChart from '../components/charts/OrganizerComparisonChart.vue';
import SportDonutChart from '../components/charts/SportDonutChart.vue';

const authStore = useAuthStore();
const loading = ref(true);
const error = ref('');

// Data Refs
const overview = ref<any>({});
const monthlyTrend = ref<any[]>([]);
const cityData = ref<any[]>([]);
const fillRates = ref<any[]>([]);
const topOrganizers = ref<any[]>([]);
const popularSports = ref<any[]>([]);

const fetchData = async () => {
  loading.value = true;
  error.value = '';
  try {
    const config = { headers: { Authorization: `Bearer ${authStore.token}` } };
    
    const [statsRes, trendRes, cityRes, fillRes, orgRes] = await Promise.all([
      axios.get('http://localhost:8000/api/admin/dashboard', config),
      axios.get('http://localhost:8000/api/admin/monthly-trend', config),
      axios.get('http://localhost:8000/api/admin/city-distribution', config),
      axios.get('http://localhost:8000/api/admin/fill-rate', config),
      axios.get('http://localhost:8000/api/admin/organizer-performance', config)
    ]);

    overview.value = statsRes.data;
    monthlyTrend.value = trendRes.data;
    cityData.value = cityRes.data;
    fillRates.value = fillRes.data;
    topOrganizers.value = orgRes.data;
    popularSports.value = (await axios.get('http://localhost:8000/api/admin/popular-sport', config)).data;

  } catch (err: any) {
    error.value = 'Failed to load admin analytics. ' + (err.response?.data?.message || '');
  } finally {
    loading.value = false;
  }
};

onMounted(() => fetchData());
</script>

<style scoped>
.admin-dashboard {
  background-color: var(--bg-site);
  min-height: 100vh;
  position: relative;
}

.dashboard-header-corp {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.kpi-grid {
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
  font-size: 2rem;
  font-weight: 900;
  line-height: 1;
  letter-spacing: -0.04em;
}

.charts-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 1.5rem;
}

.sport-stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.sport-stat-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: var(--radius-sm);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

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

.table-corp td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
  font-size: 0.9rem;
}

.loading-corp-full {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 60px 0;
  color: var(--text-dim);
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

.hero-title-small {
  font-size: 1.75rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.15;
}

@media (max-width: 1200px) {
  .kpi-grid { grid-template-columns: repeat(2, 1fr); }
  .charts-row { grid-template-columns: 1fr; }
  .dashboard-header-corp { flex-direction: column; align-items: flex-start; gap: 2rem; }
}

@media (max-width: 640px) {
  .kpi-grid { grid-template-columns: 1fr; }
}
</style>
