<template>
  <div class="admin-page">

    <!-- Ambient background blobs — visible in dark, subtle in light -->
    <div class="ambient-bg" aria-hidden="true">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
    </div>

    <div class="admin-content">
      <div class="container mx-auto px-6 max-w-7xl">

        <!-- ── Header ── -->
        <div class="admin-header">
          <div>
            <div class="header-badge">
              <span>Platform Intelligence</span>
            </div>
            <h1 class="admin-title">
              Command <br/>
              <span class="title-dim">Overview.</span>
            </h1>
            <p class="admin-sub">
              High-level telemetry of platform operatives and architectural efficiency.
            </p>
          </div>

          <button
            @click="fetchData"
            :disabled="loading"
            class="refresh-btn"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2.5"
              :class="{ 'animate-spin': loading }">
              <path d="M23 4v6h-6"/>
              <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
            </svg>
            Re-Sync Platform
          </button>
        </div>

        <!-- ── Loading ── -->
        <div v-if="loading" class="state-center">
          <div class="spinner"></div>
          <span class="state-label">Fetching Intelligence…</span>
        </div>

        <!-- ── Error ── -->
        <div v-else-if="error" class="error-banner">
          <span class="text-2xl">⚠️</span>
          <span>{{ error }}</span>
        </div>

        <!-- ── Dashboard ── -->
        <div v-else class="dashboard-body">

          <!-- Stat cards -->
          <div class="stats-grid">

            <div class="stat-card stat-card--purple">
              <div class="stat-card-glow glow-purple"></div>
              <span class="stat-label">Total Operatives</span>
              <span class="stat-value">{{ overview.total_users }}</span>
            </div>

            <div class="stat-card stat-card--cyan">
              <div class="stat-card-glow glow-cyan"></div>
              <span class="stat-label">Active Deployments</span>
              <span class="stat-value">{{ overview.total_events }}</span>
            </div>

            <div class="stat-card stat-card--pink">
              <div class="stat-card-glow glow-pink"></div>
              <span class="stat-label">Total Commitments</span>
              <span class="stat-value">{{ overview.total_registrations }}</span>
            </div>

            <div class="stat-card stat-card--neutral">
              <div class="stat-card-glow glow-neutral"></div>
              <span class="stat-label stat-label--muted">Aggregate Yield</span>
              <span class="stat-value stat-value--lg">₹{{ overview.total_revenue?.toLocaleString() }}</span>
            </div>

          </div>

          <!-- Charts row 1 -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div class="dash-card lg:col-span-2">
              <h2 class="dash-card-title">Temporal Growth Trend</h2>
              <div class="chart-area"><MonthlyTrendChart :data="monthlyTrend" /></div>
            </div>
            <div class="dash-card">
              <h2 class="dash-card-title">Sport Category</h2>
              <div class="chart-area"><SportDonutChart :data="popularSports" /></div>
            </div>
          </div>

          <!-- Charts row 2 -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="dash-card">
              <h2 class="dash-card-title">Bio-Region Distribution</h2>
              <div class="chart-area"><CityDistributionChart :data="cityData" /></div>
            </div>
            <div class="dash-card">
              <h2 class="dash-card-title">Event Fill Rates</h2>
              <div class="chart-area"><FillRateChart :data="fillRates" /></div>
            </div>
          </div>

          <!-- Organizer comparison -->
          <div class="dash-card">
            <h2 class="dash-card-title">Organizer Performance</h2>
            <div class="chart-area chart-area--tall"><OrganizerComparisonChart :data="topOrganizers" /></div>
          </div>

          <!-- Leaderboard table -->
          <div class="dash-card overflow-hidden">
            <h2 class="dash-card-title">Elite Architect Performance</h2>
            <div class="overflow-x-auto">
              <table class="leaderboard-table">
                <thead>
                  <tr class="table-header-row">
                    <th class="th">Rank</th>
                    <th class="th">Architect Name</th>
                    <th class="th">Deployments</th>
                    <th class="th">Commitments</th>
                    <th class="th">Total Yield (₹)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(org, i) in topOrganizers"
                    :key="org.organizer_id"
                    class="table-body-row"
                  >
                    <td class="td td--muted">#{{ i + 1 }}</td>
                    <td class="td td--name">{{ org.organizer_name }}</td>
                    <td class="td td--dim">{{ org.total_events }}</td>
                    <td class="td td--dim">{{ org.total_registrations }}</td>
                    <td class="td td--revenue">₹{{ org.total_revenue.toLocaleString() }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { adminApi } from '../services/api';
import MonthlyTrendChart from '../components/charts/MonthlyTrendChart.vue';
import CityDistributionChart from '../components/charts/CityDistributionChart.vue';
import FillRateChart from '../components/charts/FillRateChart.vue';
import OrganizerComparisonChart from '../components/charts/OrganizerComparisonChart.vue';
import SportDonutChart from '../components/charts/SportDonutChart.vue';

const loading = ref(true);
const error   = ref('');

const overview      = ref<any>({});
const monthlyTrend  = ref<any[]>([]);
const cityData      = ref<any[]>([]);
const fillRates     = ref<any[]>([]);
const topOrganizers = ref<any[]>([]);
const popularSports = ref<any[]>([]);

const fetchData = async () => {
  loading.value = true;
  error.value   = '';
  try {
    const [statsRes, trendRes, cityRes, fillRes, orgRes, popularRes] = await Promise.all([
      adminApi.getDashboard(),
      adminApi.getMonthlyTrend(),
      adminApi.getCityDistribution(),
      adminApi.getFillRate(),
      adminApi.getOrganizerPerformance(),
      adminApi.getPopularSport(),
    ]);
    overview.value      = statsRes.data;
    monthlyTrend.value  = trendRes.data;
    cityData.value      = cityRes.data;
    fillRates.value     = fillRes.data;
    topOrganizers.value = orgRes.data;
    popularSports.value = popularRes.data;
  } catch (err: any) {
    error.value = 'Failed to load admin analytics. ' + (err.response?.data?.message || '');
  } finally {
    loading.value = false;
  }
};

onMounted(() => fetchData());
</script>

<style scoped>
/* ══════════════════════════════════════════
   PAGE SHELL
══════════════════════════════════════════ */
.admin-page {
  min-height: 100vh;
  background: var(--bg-site);
  color: var(--text-main);
  position: relative;
  display: flex;
  flex-direction: column;
  transition: background 0.3s ease, color 0.3s ease;
}

.admin-content {
  position: relative;
  z-index: 10;
  padding-top: 7rem;
  padding-bottom: 6rem;
  flex: 1;
}

/* ══════════════════════════════════════════
   AMBIENT BLOBS
══════════════════════════════════════════ */
.ambient-bg {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
}

.blob-1 {
  top: -10%;
  right: -5%;
  width: 55%;
  height: 55%;
  background: radial-gradient(circle, rgba(112,0,255,0.12) 0%, transparent 70%);
}

.blob-2 {
  bottom: -10%;
  left: -5%;
  width: 50%;
  height: 50%;
  background: radial-gradient(circle, rgba(0,243,255,0.08) 0%, transparent 70%);
}

/* Tone down blobs in light mode */
[data-theme="light"] .blob-1 {
  background: radial-gradient(circle, rgba(112,0,255,0.05) 0%, transparent 70%);
}
[data-theme="light"] .blob-2 {
  background: radial-gradient(circle, rgba(0,243,255,0.04) 0%, transparent 70%);
}

/* ══════════════════════════════════════════
   HEADER
══════════════════════════════════════════ */
.admin-header {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 4rem;
}

@media (min-width: 768px) {
  .admin-header {
    flex-direction: row;
    align-items: flex-end;
  }
}

.header-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 1rem;
  border-radius: 9999px;
  border: 1px solid var(--border-subtle);
  background: var(--bg-panel);
  margin-bottom: 1.25rem;
}

.header-badge span {
  font-size: 0.65rem;
  font-weight: 900;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: #7000ff;
}

[data-theme="light"] .header-badge span { color: #6d28d9; }

.admin-title {
  font-size: clamp(2.5rem, 6vw, 4.5rem);
  font-weight: 900;
  letter-spacing: -0.04em;
  line-height: 0.95;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.title-dim {
  color: var(--text-dim);
}

.admin-sub {
  font-size: 1rem;
  color: var(--text-dim);
  font-weight: 500;
  max-width: 36rem;
  line-height: 1.65;
}

/* Refresh button */
.refresh-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.85rem 1.75rem;
  border-radius: 9999px;
  border: 1px solid var(--border-subtle);
  background: var(--bg-panel);
  color: var(--text-primary);
  font-weight: 700;
  font-size: 0.88rem;
  cursor: pointer;
  transition: background 0.2s ease, border-color 0.2s ease, transform 0.15s ease;
  white-space: nowrap;
  flex-shrink: 0;
}

.refresh-btn:hover:not(:disabled) {
  background: var(--bg-panel-light);
  border-color: var(--border-premium);
  transform: translateY(-1px);
}

.refresh-btn:disabled { opacity: 0.5; cursor: not-allowed; }

/* ══════════════════════════════════════════
   STATE: LOADING / ERROR
══════════════════════════════════════════ */
.state-center {
  padding: 6rem 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
}

.spinner {
  width: 44px;
  height: 44px;
  border: 3px solid var(--border-subtle);
  border-top-color: #7000ff;
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

.error-banner {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: rgba(239,68,68,0.08);
  border: 1px solid rgba(239,68,68,0.2);
  border-radius: 1.5rem;
  padding: 1.5rem 2rem;
  margin-bottom: 2rem;
  color: #ef4444;
  font-weight: 500;
}

/* ══════════════════════════════════════════
   DASHBOARD BODY
══════════════════════════════════════════ */
.dashboard-body {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* ══════════════════════════════════════════
   STAT CARDS
══════════════════════════════════════════ */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 1.5rem;
}

@media (min-width: 768px)  { .stats-grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 1024px) { .stats-grid { grid-template-columns: repeat(4, 1fr); } }

.stat-card {
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-radius: 1.5rem;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  position: relative;
  overflow: hidden;
  transition: background 0.25s ease, border-color 0.25s ease, transform 0.2s ease;
}

.stat-card:hover { transform: translateY(-3px); }

.stat-card--purple:hover { border-color: rgba(112,0,255,0.4); }
.stat-card--cyan:hover   { border-color: rgba(0,243,255,0.4); }
.stat-card--pink:hover   { border-color: rgba(255,0,85,0.4); }
.stat-card--neutral:hover { border-color: var(--border-premium); }

/* Light mode stat cards: white background, solid border, shadow */
[data-theme="light"] .stat-card {
  background: #ffffff;
  border-color: #64748b;
  box-shadow: 0 0 0 2px #64748b, 0 6px 24px rgba(0,0,0,0.1);
}

/* Glow overlays — visible only on hover */
.stat-card-glow {
  position: absolute;
  inset: 0;
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
}

.stat-card:hover .stat-card-glow { opacity: 1; }

.glow-purple  { background: linear-gradient(135deg, rgba(112,0,255,0.08) 0%, transparent 70%); }
.glow-cyan    { background: linear-gradient(135deg, rgba(0,243,255,0.08) 0%, transparent 70%); }
.glow-pink    { background: linear-gradient(135deg, rgba(255,0,85,0.08) 0%, transparent 70%); }
.glow-neutral { background: linear-gradient(135deg, rgba(148,163,184,0.06) 0%, transparent 70%); }

.stat-label {
  font-size: 0.62rem;
  font-weight: 900;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: #7000ff;
  position: relative;
  z-index: 1;
}

.stat-label--muted { color: var(--text-dim); }

[data-theme="light"] .stat-label { color: #6d28d9; }

.stat-card--cyan  .stat-label { color: #00b8cc; }
.stat-card--pink  .stat-label { color: #e00048; }

[data-theme="light"] .stat-card--cyan .stat-label  { color: #0369a1; }
[data-theme="light"] .stat-card--pink .stat-label  { color: #be185d; }

.stat-value {
  font-size: 2.75rem;
  font-weight: 900;
  letter-spacing: -0.04em;
  color: var(--text-primary);
  position: relative;
  z-index: 1;
  line-height: 1;
}

.stat-value--lg { font-size: 2.2rem; }

/* ══════════════════════════════════════════
   DASHBOARD CARDS (charts + table wrapper)
══════════════════════════════════════════ */
.dash-card {
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-radius: 1.5rem;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  transition: background 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
}

/* Light mode: solid white card with a clearly visible border + shadow */
[data-theme="light"] .dash-card {
  background: #ffffff;
  border-color: #64748b;
  box-shadow: 0 0 0 2px #64748b, 0 6px 24px rgba(0,0,0,0.1);
}

.dash-card-title {
  font-size: 0.68rem;
  font-weight: 900;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--text-primary);
  margin-bottom: 1.5rem;
}

.chart-area {
  flex: 1;
  width: 100%;
  min-height: 300px;
}

.chart-area--tall { min-height: 400px; }

/* ══════════════════════════════════════════
   LEADERBOARD TABLE
══════════════════════════════════════════ */
.leaderboard-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.table-header-row {
  border-bottom: 1px solid var(--border-subtle);
}

.th {
  padding: 1rem 1.5rem;
  font-size: 0.62rem;
  font-weight: 900;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-muted);
  white-space: nowrap;
}

.table-body-row {
  border-bottom: 1px solid var(--border-subtle);
  transition: background 0.15s ease;
}

.table-body-row:last-child { border-bottom: none; }

.table-body-row:hover { background: var(--bg-panel-light); }

.td {
  padding: 1.25rem 1.5rem;
  font-size: 0.9rem;
}

.td--muted   { font-weight: 700; color: var(--text-muted); }
.td--name    { font-weight: 700; color: var(--text-primary); }
.td--dim     { font-weight: 500; color: var(--text-dim); }
.td--revenue {
  font-weight: 900;
  letter-spacing: -0.02em;
  color: #00b8cc;
}

[data-theme="light"] .td--revenue { color: #0369a1; }
</style>
