<template>
  <div class="org-dash-page">
    <div class="container mx-auto px-6 max-w-7xl">
      <div class="page-header">
        <h1 class="page-title">Analytics Dashboard</h1>
        <p class="page-sub">Performance overview of your events.</p>
      </div>

      <div v-if="loading" class="state-center"><div class="spinner"></div></div>
      <div v-else-if="error" class="error-banner">{{ error }}</div>

      <div v-else class="dash-body">

        <!-- KPI row -->
        <div class="kpi-grid">
          <div class="kpi-card">
            <span class="kpi-label">Total Capacity</span>
            <span class="kpi-value kpi-value--accent">{{ totalCapacity }}</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-label">Registrations</span>
            <span class="kpi-value kpi-value--accent">{{ totalRegistrations }}</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-label">Fill Rate</span>
            <span class="kpi-value kpi-value--accent">{{ aggregateFillRate }}%</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-label">Total Revenue</span>
            <span class="kpi-value kpi-value--accent">₹{{ totalRevenue.toLocaleString() }}</span>
          </div>
        </div>

        <!-- Charts row 1 -->
        <div class="charts-row">
          <div class="chart-card">
            <p class="chart-title">Registration Trend</p>
            <div class="selector-row">
              <div class="select-wrap">
                <select v-model="selectedEventId" @change="fetchTrend" class="dash-select">
                  <option v-for="e in events" :key="e.event_id" :value="e.event_id">{{ e.title }}</option>
                </select>
                <svg class="select-chev" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
              </div>
            </div>
            <div v-if="loadingTrend" class="state-center"><div class="spinner-sm"></div></div>
            <RegistrationTrend v-else :data="trendData" />
          </div>
          <div class="chart-card">
            <p class="chart-title">Category Breakdown</p>
            <CategoryBarChart :data="categoryData" />
          </div>
        </div>

        <!-- Charts row 2 -->
        <div class="charts-row">
          <div class="chart-card">
            <p class="chart-title">Revenue per Event</p>
            <RevenuePerEventChart :data="events" />
          </div>
          <div class="chart-card">
            <p class="chart-title">Capacity Utilisation</p>
            <CapacityChart :data="events" />
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { organizerApi } from '../services/api';
import RegistrationTrend  from '../components/charts/RegistrationTrend.vue';
import CategoryBarChart   from '../components/charts/CategoryBarChart.vue';
import RevenuePerEventChart from '../components/charts/RevenuePerEventChart.vue';
import CapacityChart      from '../components/charts/CapacityChart.vue';

const loading        = ref(true);
const loadingTrend   = ref(false);
const error          = ref('');
const events         = ref<any[]>([]);
const categoryData   = ref<any[]>([]);
const trendData      = ref<any[]>([]);
const selectedEventId = ref<number | null>(null);

const totalCapacity      = computed(() => events.value.reduce((a, e) => a + e.capacity, 0));
const totalRegistrations = computed(() => events.value.reduce((a, e) => a + e.registrations, 0));
const totalRevenue       = computed(() => events.value.reduce((a, e) => a + e.revenue, 0));
const aggregateFillRate  = computed(() => {
  if (!totalCapacity.value) return 0;
  return Math.round((totalRegistrations.value / totalCapacity.value) * 1000) / 10;
});

const fetchTrend = async () => {
  if (!selectedEventId.value) return;
  loadingTrend.value = true;
  try { trendData.value = (await organizerApi.getTrend(selectedEventId.value)).data; }
  finally { loadingTrend.value = false; }
};

onMounted(async () => {
  loading.value = true;
  try {
    const [evRes, catRes] = await Promise.all([
      organizerApi.getDashboard(),
      organizerApi.getCategoryInsight(),
    ]);
    events.value       = evRes.data;
    categoryData.value = catRes.data;
    if (events.value.length) { selectedEventId.value = events.value[0].event_id; await fetchTrend(); }
  } catch { error.value = 'Failed to load analytics.'; }
  finally { loading.value = false; }
});
</script>

<style scoped>
.org-dash-page { min-height: 100vh; background: var(--bg-site); padding: 7rem 0 4rem; }
.page-header { margin-bottom: 2rem; }
.page-title  { font-size: clamp(1.8rem, 4vw, 2.8rem); font-weight: 900; letter-spacing: -0.04em; color: var(--text-primary); }
.page-sub    { font-size: 0.88rem; color: var(--text-muted); margin-top: 0.25rem; }

.state-center { display: flex; justify-content: center; padding: 5rem; }
.spinner { width: 36px; height: 36px; border: 3px solid var(--border-subtle); border-top-color: var(--brand-accent); border-radius: 50%; animation: spin 0.8s linear infinite; }
.spinner-sm { width: 24px; height: 24px; border: 2px solid var(--border-subtle); border-top-color: var(--brand-accent); border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.error-banner { padding: 1rem 1.5rem; background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.2); border-radius: 12px; color: #f87171; margin-bottom: 1.5rem; }

.dash-body { display: flex; flex-direction: column; gap: 1.25rem; }

.kpi-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; }
@media (max-width: 900px) { .kpi-grid { grid-template-columns: repeat(2,1fr); } }

.kpi-card { background: var(--bg-panel); border: 1px solid var(--border-subtle); border-radius: 14px; padding: 1.4rem; display: flex; flex-direction: column; gap: 0.4rem; }
[data-theme="light"] .kpi-card { background: #fff; border: 2px solid #94a3b8; box-shadow: 0 3px 10px rgba(0,0,0,0.06); }
.kpi-label { font-size: 0.62rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.12em; color: var(--text-muted); }
.kpi-value { font-size: 2rem; font-weight: 900; letter-spacing: -0.04em; color: var(--text-primary); line-height: 1; }
.kpi-value--accent { color: var(--brand-accent); }
[data-theme="light"] .kpi-value--accent { color: #0369a1; }

.charts-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; }
@media (max-width: 1024px) { .charts-row { grid-template-columns: 1fr; } }

.chart-card { background: var(--bg-panel); border: 1px solid var(--border-subtle); border-radius: 18px; padding: 1.75rem; }
[data-theme="light"] .chart-card { background: #fff; border: 2px solid #94a3b8; box-shadow: 0 4px 16px rgba(0,0,0,0.07); }

.chart-title { font-size: 0.68rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.15em; color: var(--text-primary); margin-bottom: 1.1rem; }

.selector-row { margin-bottom: 1rem; }
.select-wrap { position: relative; display: inline-block; min-width: 220px; }
.dash-select { width: 100%; padding: 0.6rem 2.2rem 0.6rem 0.85rem; background: var(--bg-panel-light); border: 1px solid var(--border-subtle); border-radius: 9px; color: var(--text-primary); font-size: 0.85rem; font-family: inherit; outline: none; appearance: none; cursor: pointer; }
[data-theme="dark"] .dash-select, [data-theme="dark"] .dash-select option { background: #1c1c1f; color: #f8fafc; }
[data-theme="light"] .dash-select, [data-theme="light"] .dash-select option { background: #f8fafc; color: #0f172a; border-color: #cbd5e1; }
.select-chev { position: absolute; right: 0.7rem; top: 50%; transform: translateY(-50%); pointer-events: none; color: var(--text-muted); }
</style>