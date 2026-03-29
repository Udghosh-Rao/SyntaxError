<template>
  <div class="organizer-dashboard">
    <div class="container py-12">

      <!-- Header -->
      <div class="dashboard-header mb-12 animate-corp">
        <div>
          <span class="dash-badge">Management Console</span>
          <h1 class="dash-title mt-3">Architect Dashboard</h1>
          <p class="dash-sub mt-2">Precision monitoring of your event portfolio and revenue stream.</p>
        </div>
        <router-link to="/organizer/create" class="create-btn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2.5"
            stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          Create Event
        </router-link>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-state">
        <div class="dash-spinner"></div>
        <span class="state-label">Loading dashboard…</span>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="error-banner">{{ error }}</div>

      <!-- Dashboard -->
      <div v-else class="dashboard-grid">

        <!-- Founder KPIs -->
        <section v-if="authStore.isFounder" class="dash-card span-2 founder-section">
          <h2 class="section-title">Platform Overview (Founder Rights)</h2>
          <div class="kpi-grid">
            <div class="kpi-card">
              <span class="kpi-label">Platform Users</span>
              <span class="kpi-value">{{ adminOverview.total_users }}</span>
            </div>
            <div class="kpi-card">
              <span class="kpi-label">Platform Events</span>
              <span class="kpi-value">{{ adminOverview.total_events }}</span>
            </div>
            <div class="kpi-card">
              <span class="kpi-label">Platform Registrations</span>
              <span class="kpi-value">{{ adminOverview.total_registrations }}</span>
            </div>
            <div class="kpi-card">
              <span class="kpi-label">Top Sport</span>
              <span class="kpi-value kpi-value--accent">{{ adminOverview.most_popular_sport || 'N/A' }}</span>
            </div>
          </div>
        </section>

        <!-- KPI Stats -->
        <section class="span-2 animate-corp delay-50">
          <div class="kpi-grid">
            <div class="kpi-card">
              <span class="kpi-label">Total Capacity</span>
              <span class="kpi-value kpi-value--grad">{{ totalCapacity }}</span>
            </div>
            <div class="kpi-card">
              <span class="kpi-label">Registrations</span>
              <span class="kpi-value kpi-value--grad">{{ totalRegistrations }}</span>
            </div>
            <div class="kpi-card">
              <span class="kpi-label">Fill Rate</span>
              <span class="kpi-value kpi-value--grad">{{ aggregateFillRate }}%</span>
            </div>
            <div class="kpi-card">
              <span class="kpi-label">Total Revenue</span>
              <span class="kpi-value kpi-value--grad">₹{{ totalRevenue.toLocaleString() }}</span>
            </div>
          </div>
        </section>

        <!-- Events Table -->
        <section class="dash-card span-2 animate-corp delay-100">
          <h2 class="section-title mb-6">Active Events</h2>
          <div class="table-scroll">
            <table class="dash-table">
              <thead>
                <tr>
                  <th>Event</th>
                  <th>Date</th>
                  <th>City</th>
                  <th>Registrations</th>
                  <th>Capacity</th>
                  <th>Revenue (₹)</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="event in events" :key="event.event_id" class="table-row">
                  <td class="td-name">{{ event.title }}</td>
                  <td class="td-dim">{{ new Date(event.event_date).toLocaleDateString('en-GB') }}</td>
                  <td class="td-dim">{{ event.venue_city }}</td>
                  <td class="td-dim">{{ event.registrations }}</td>
                  <td class="td-dim">{{ event.capacity }}</td>
                  <td class="td-revenue">{{ event.revenue }}</td>
                  <td>
                    <span class="perf-badge" :class="'perf-badge--' + event.performance_label.toLowerCase()">
                      {{ event.performance_label }}
                    </span>
                  </td>
                  <td v-if="authStore.isFounder">
                    <button
                      @click="toggleFeatureEvent(event)"
                      class="perf-badge perf-badge--clickable"
                      :class="event.is_featured ? 'perf-badge--high' : 'perf-badge--medium'"
                    >
                      {{ event.is_featured ? 'Featured' : 'Standard' }}
                    </button>
                  </td>
                  <td class="td-actions">
                    <button @click="openEditModal(event)" class="action-btn action-btn--edit">Edit</button>
                    <button @click="deleteOrgEvent(event)" class="action-btn action-btn--delete">Delete</button>
                  </td>
                </tr>
                  <tr v-if="events.length === 0">
                    <td colspan="9" class="td-empty">No active events found.</td>
                  </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Charts row 1 -->
        <div class="charts-row span-2" v-if="events.length > 0">
          <section class="dash-card animate-corp delay-200">
            <h2 class="section-title mb-5">Registration Trend</h2>
            <div class="selector-row mb-5">
              <label class="select-label">Select Event</label>
              <div class="select-wrap">
                <select v-model="selectedEventId" @change="fetchTrendData" class="dash-select">
                  <option v-for="event in events" :key="event.event_id" :value="event.event_id">
                    {{ event.title }}
                  </option>
                </select>
                <svg class="select-chev" width="14" height="14" viewBox="0 0 24 24"
                  fill="none" stroke="currentColor" stroke-width="2.5"
                  stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="6 9 12 15 18 9"/>
                </svg>
              </div>
            </div>
            <div v-if="loadingTrend" class="chart-loading">
              <div class="dash-spinner dash-spinner--sm"></div>
            </div>
            <RegistrationTrend v-else :data="trendData" />
          </section>

          <section class="dash-card animate-corp delay-300">
            <h2 class="section-title mb-5">Category Breakdown</h2>
            <CategoryBarChart :data="categoryData" />
          </section>
        </div>

        <!-- Promotion Panel -->
        <section v-if="authStore.isFounder && promotedEvents.length > 0"
          class="dash-card span-2 promo-section animate-corp">
          <h2 class="section-title promo-title mb-6">Active Promotion Campaigns</h2>
          <div class="promo-grid">
            <div v-for="promo in promotedEvents" :key="promo.event_id" class="promo-card">
              <h3 class="promo-name">{{ promo.title }}</h3>
              <div class="promo-row">
                <span class="td-dim text-sm">Pre-Promotion</span>
                <span class="promo-num">{{ promo.snapshot_registrations }}</span>
              </div>
              <div class="promo-row">
                <span class="td-dim text-sm">Current</span>
                <span class="promo-num promo-num--accent">{{ getEventCurrentRegistrations(promo.event_id) }}</span>
              </div>
              <p class="promo-time">Promoted {{ new Date(promo.timestamp).toLocaleTimeString() }}</p>
            </div>
          </div>
        </section>

        <!-- Charts row 2 -->
        <div class="charts-row span-2" v-if="events.length > 0">
          <section class="dash-card animate-corp delay-400">
            <h2 class="section-title mb-5">Revenue per Event</h2>
            <RevenuePerEventChart :data="events" />
          </section>
          <section class="dash-card animate-corp delay-400">
            <h2 class="section-title mb-5">Capacity Utilisation</h2>
            <CapacityChart :data="events" />
          </section>
        </div>

      </div>
    </div>

    <!-- ── Edit Event Modal ── -->
    <div v-if="showEditModal" class="modal-overlay" @click.self="showEditModal = false">
      <div class="modal-box">
        <h2 class="modal-title">Edit Event</h2>
        <form @submit.prevent="saveOrgEvent">
          <div class="field">
            <label class="field-label">Title</label>
            <input v-model="editForm.title" type="text" class="field-input" required />
          </div>
          <div class="field">
            <label class="field-label">Description</label>
            <textarea v-model="editForm.description" class="field-input" rows="3"></textarea>
          </div>
          <div class="field-row">
            <div class="field">
              <label class="field-label">Date & Time</label>
              <input v-model="editForm.event_date" type="datetime-local" class="field-input" required />
            </div>
            <div class="field">
              <label class="field-label">Entry Fee (₹)</label>
              <input v-model="editForm.price" type="number" min="0" class="field-input" required />
            </div>
          </div>
          <div class="field-row">
            <div class="field">
              <label class="field-label">City</label>
              <input v-model="editForm.venue_city" type="text" class="field-input" />
            </div>
            <div class="field">
              <label class="field-label">Venue Address</label>
              <input v-model="editForm.venue_address" type="text" class="field-input" />
            </div>
          </div>
          <div class="field-row">
            <div class="field">
              <label class="field-label">Sport Category</label>
              <select v-model="editForm.sport_category" class="field-input">
                <option>Football</option><option>Basketball</option>
                <option>Tennis</option><option>Cricket</option>
                <option>Swimming</option><option>Other</option>
              </select>
            </div>
            <div class="field">
              <label class="field-label">Capacity</label>
              <input v-model="editForm.capacity" type="number" min="1" class="field-input" required />
            </div>
          </div>
          <div class="modal-actions">
            <button type="button" @click="showEditModal = false" class="btn-cancel">Cancel</button>
            <button type="submit" class="btn-save">Save Changes</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import { organizerApi, adminApi, eventApi } from '../services/api';
import RegistrationTrend from '../components/charts/RegistrationTrend.vue';
import CategoryBarChart from '../components/charts/CategoryBarChart.vue';
import RevenuePerEventChart from '../components/charts/RevenuePerEventChart.vue';
import CapacityChart from '../components/charts/CapacityChart.vue';

const authStore    = useAuthStore();
const loading      = ref(true);
const loadingTrend = ref(false);
const error        = ref('');
const events       = ref<any[]>([]);
const categoryData = ref<any[]>([]);
const trendData    = ref<any[]>([]);
const selectedEventId = ref<number | null>(null);
const adminOverview   = ref<any>({});
const promotedEvents  = ref<any[]>([]);
let pollInterval: any;

const totalCapacity      = computed(() => events.value.reduce((a, e) => a + e.capacity, 0));
const totalRegistrations = computed(() => events.value.reduce((a, e) => a + e.registrations, 0));
const totalRevenue       = computed(() => events.value.reduce((a, e) => a + e.revenue, 0));
const aggregateFillRate  = computed(() => {
  if (!totalCapacity.value) return 0;
  return Math.round((totalRegistrations.value / totalCapacity.value) * 1000) / 10;
});

const fetchDashboardData = async (isPolling = false) => {
  if (!isPolling) loading.value = true;
  error.value = '';
  try {
    const promises: any[] = [organizerApi.getDashboard(), organizerApi.getCategoryInsight()];
    if (authStore.isFounder || authStore.isAdmin) promises.push(adminApi.getDashboard());
    const res = await Promise.all(promises);
    events.value       = res[0].data;
    categoryData.value = res[1].data;
    if (authStore.isFounder || authStore.isAdmin) adminOverview.value = res[2].data;
    if (events.value.length > 0 && !isPolling) {
      selectedEventId.value = events.value[0].event_id;
      await fetchTrendData();
    }
  } catch {
    if (!isPolling) error.value = 'Failed to load dashboard data.';
  } finally {
    if (!isPolling) loading.value = false;
  }
};

const toggleFeatureEvent = async (event: any) => {
  try {
    const res = await organizerApi.toggleFeature(event.event_id);
    event.is_featured = res.data.is_featured;
    if (event.is_featured) {
      promotedEvents.value.push({ event_id: event.event_id, title: event.title, snapshot_registrations: res.data.snapshot_registrations, timestamp: Date.now() });
    } else {
      promotedEvents.value = promotedEvents.value.filter(p => p.event_id !== event.event_id);
    }
  } catch { alert('Failed to toggle feature status'); }
};

const getEventCurrentRegistrations = (id: number) => events.value.find(e => e.event_id === id)?.registrations ?? 0;

const fetchTrendData = async () => {
  if (!selectedEventId.value) return;
  loadingTrend.value = true;
  try {
    const res = await organizerApi.getTrend(selectedEventId.value);
    trendData.value = res.data;
  } catch { /* silent */ } finally { loadingTrend.value = false; }
};

onMounted(() => { fetchDashboardData(); pollInterval = setInterval(() => fetchDashboardData(true), 5000); });
onUnmounted(() => { if (pollInterval) clearInterval(pollInterval); });

// ── Organizer Edit / Delete ──
const showEditModal    = ref(false);
const editingEventId   = ref<number | null>(null);
const editForm = ref({
  title: '', description: '', sport_category: 'Football',
  event_date: '', venue_city: '', venue_address: '',
  capacity: 100, price: 0
});

const openEditModal = (event: any) => {
  editingEventId.value = event.event_id;
  editForm.value = {
    title: event.title,
    description: event.description || '',
    sport_category: event.sport_category,
    event_date: event.event_date?.slice(0, 16) || '',
    venue_city: event.venue_city || '',
    venue_address: event.venue_address || '',
    capacity: event.capacity,
    price: event.price
  };
  showEditModal.value = true;
};

const saveOrgEvent = async () => {
  if (!editingEventId.value) return;
  try {
    const payload = {
      ...editForm.value,
      event_date: new Date(editForm.value.event_date).toISOString()
    };
    await eventApi.update(String(editingEventId.value), payload);
    showEditModal.value = false;
    await fetchDashboardData();
  } catch (err: any) {
    alert('Failed to save: ' + (err.response?.data?.message || ''));
  }
};

const deleteOrgEvent = async (event: any) => {
  if (!confirm(`Delete "${event.title}"? This cannot be undone.`)) return;
  try {
    await eventApi.delete(String(event.event_id));
    await fetchDashboardData();
  } catch (err: any) {
    alert('Failed to delete: ' + (err.response?.data?.message || ''));
  }
};
</script>

<style scoped>
/* ── Page ── */
.organizer-dashboard {
  min-height: 100vh;
  background: var(--bg-site);
  color: var(--text-main);
  padding-top: 6rem; /* clears fixed navbar */
}

/* ── Header ── */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.dash-badge {
  display: inline-block;
  font-size: 0.65rem;
  font-weight: 900;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 0.35rem 0.85rem;
  border-radius: 9999px;
  border: 1px solid var(--border-subtle);
  background: var(--bg-panel);
  color: var(--text-dim);
}

.dash-title {
  font-size: clamp(1.8rem, 4vw, 2.8rem);
  font-weight: 900;
  letter-spacing: -0.04em;
  color: var(--text-primary);
  line-height: 1.1;
}

.dash-sub {
  font-size: 0.9rem;
  color: var(--text-dim);
}

/* Create button — matches login/register style */
.create-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: var(--brand-accent);
  color: #000;
  font-weight: 800;
  font-size: 0.88rem;
  border-radius: 9999px;
  text-decoration: none;
  transition: opacity 0.15s ease, transform 0.15s ease, box-shadow 0.15s ease;
  flex-shrink: 0;
}

.create-btn:hover {
  opacity: 0.88;
  transform: translateY(-1px);
  box-shadow: 0 6px 20px color-mix(in srgb, var(--brand-accent) 25%, transparent);
}

/* ── Loading / error ── */
.loading-state {
  display: flex; flex-direction: column; align-items: center;
  gap: 1rem; padding: 5rem 0; color: var(--text-dim);
}

.dash-spinner {
  width: 36px; height: 36px;
  border: 3px solid var(--border-subtle);
  border-top-color: var(--brand-accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.dash-spinner--sm { width: 24px; height: 24px; }

@keyframes spin { to { transform: rotate(360deg); } }

.state-label {
  font-size: 0.75rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.15em;
  color: var(--text-muted);
}

.error-banner {
  padding: 1rem 1.5rem;
  background: rgba(239,68,68,0.08);
  border: 1px solid rgba(239,68,68,0.2);
  border-radius: 12px;
  color: #f87171;
  font-size: 0.9rem;
  margin-bottom: 2rem;
}

/* ── Grid ── */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.span-2 { grid-column: span 2; }

.charts-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

@media (max-width: 1200px) { .charts-row { grid-template-columns: 1fr; } }

/* ── Cards ── */
.dash-card {
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-radius: 1.25rem;
  padding: 1.75rem;
  transition: background 0.25s ease, border-color 0.25s ease;
}

[data-theme="light"] .dash-card {
  background: #ffffff;
  border: 2px solid #94a3b8;
  box-shadow: 0 0 0 0px transparent, 0 4px 16px rgba(0,0,0,0.07);
}

.section-title {
  font-size: 0.68rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--text-primary);
}

/* ── KPI grid ── */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

@media (max-width: 900px) { .kpi-grid { grid-template-columns: repeat(2, 1fr); } }

.kpi-card {
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-radius: 1rem;
  padding: 1.25rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  transition: background 0.2s ease, border-color 0.2s ease;
}

[data-theme="light"] .kpi-card {
  background: #ffffff;
  border: 2px solid #94a3b8;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.kpi-label {
  font-size: 0.65rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--text-muted);
}

.kpi-value {
  font-size: 2rem;
  font-weight: 900;
  letter-spacing: -0.04em;
  color: var(--text-primary);
  line-height: 1;
}

.kpi-value--grad { color: var(--brand-accent); }
.kpi-value--accent { font-size: 1.4rem; color: var(--brand-primary); }

/* ── Founder & promo sections ── */
.founder-section {
  border-color: color-mix(in srgb, var(--brand-accent) 20%, transparent);
  background: color-mix(in srgb, var(--brand-accent) 4%, var(--bg-panel));
}

[data-theme="light"] .founder-section {
  border: 2px solid #94a3b8;
  background: #f8fafc;
}

.promo-section { border-color: rgba(255,0,127,0.25); }
[data-theme="light"] .promo-section { border: 2px solid #94a3b8; }

.promo-title { color: var(--brand-secondary); }

.promo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
}

.promo-card {
  background: var(--bg-panel-light);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  padding: 1.1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

[data-theme="light"] .promo-card {
  background: #f1f5f9;
  border: 1.5px solid #94a3b8;
}

.promo-name { font-size: 0.9rem; font-weight: 800; color: var(--text-primary); }
.promo-row  { display: flex; justify-content: space-between; align-items: center; }
.promo-num  { font-size: 1.1rem; font-weight: 900; color: var(--text-primary); }
.promo-num--accent { color: var(--brand-primary); }
.promo-time { font-size: 0.7rem; color: var(--text-muted); font-style: italic; }

/* ── Table ── */
.table-scroll { overflow-x: auto; }

.dash-table { width: 100%; border-collapse: collapse; text-align: left; }

.dash-table th {
  padding: 0.75rem 1rem;
  font-size: 0.62rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 900;
  color: var(--text-muted);
  border-bottom: 1px solid var(--border-subtle);
  white-space: nowrap;
}

[data-theme="light"] .dash-table th { border-bottom: 2px solid #94a3b8; }

.table-row { border-bottom: 1px solid var(--border-subtle); transition: background 0.15s ease; }
.table-row:hover { background: var(--bg-panel-light); }
.table-row:last-child { border-bottom: none; }

[data-theme="light"] .table-row { border-bottom: 1px solid #e2e8f0; }

.dash-table td { padding: 0.85rem 1rem; font-size: 0.88rem; }

.td-name    { font-weight: 700; color: var(--text-primary); }
.td-dim     { color: var(--text-dim); font-weight: 500; }
.td-revenue { font-weight: 900; color: var(--brand-accent); }
.td-empty   { text-align: center; padding: 2.5rem; color: var(--text-muted); }

[data-theme="light"] .td-revenue { color: #0369a1; }

/* Performance badges */
.perf-badge {
  display: inline-flex;
  padding: 0.3rem 0.7rem;
  border-radius: 9999px;
  font-size: 0.62rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.perf-badge--high,
.perf-badge.high    { background: rgba(0,223,216,0.12); color: #00dfd8; }
.perf-badge--medium,
.perf-badge.medium  { background: rgba(255,171,0,0.12); color: #ffab00; }
.perf-badge--low,
.perf-badge.low     { background: rgba(255,85,85,0.12); color: #ff5555; }

[data-theme="light"] .perf-badge--high,
[data-theme="light"] .perf-badge.high    { background: rgba(5,150,105,0.1); color: #059669; }
[data-theme="light"] .perf-badge--medium,
[data-theme="light"] .perf-badge.medium  { background: rgba(217,119,6,0.1); color: #d97706; }
[data-theme="light"] .perf-badge--low,
[data-theme="light"] .perf-badge.low     { background: rgba(220,38,38,0.1); color: #dc2626; }

.perf-badge--clickable { cursor: pointer; border: none; transition: filter 0.15s ease; }
.perf-badge--clickable:hover { filter: brightness(1.2); }

/* ── Select input ── */
.selector-row { display: flex; flex-direction: column; gap: 0.35rem; }

.select-label {
  font-size: 0.65rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.08em;
  color: var(--text-dim);
}

.select-wrap { position: relative; }

.dash-select {
  width: 100%;
  padding: 0.65rem 2.5rem 0.65rem 0.9rem;
  background: var(--bg-panel-light);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  color: var(--text-primary);
  font-size: 0.88rem;
  font-family: inherit;
  outline: none;
  appearance: none;
  cursor: pointer;
  transition: border-color 0.15s ease;
}

.dash-select:focus { border-color: var(--brand-accent); }

[data-theme="dark"] .dash-select,
[data-theme="dark"] .dash-select option { background: #1c1c1f; color: #f8fafc; }

[data-theme="light"] .dash-select,
[data-theme="light"] .dash-select option { background: #ffffff; color: #0f172a; border-color: #94a3b8; }

.select-chev {
  position: absolute; right: 0.75rem; top: 50%;
  transform: translateY(-50%);
  pointer-events: none; color: var(--text-muted);
}

.chart-loading { display: flex; justify-content: center; padding: 2rem; }

/* ── Action buttons in table ── */
.td-actions { display: flex; gap: 0.5rem; }

.action-btn {
  padding: 0.3rem 0.75rem;
  border-radius: 6px;
  font-size: 0.78rem;
  font-weight: 700;
  cursor: pointer;
  border: 1px solid transparent;
  transition: background 0.15s ease;
}

.action-btn--edit {
  background: rgba(0, 184, 204, 0.1);
  color: #00b8cc;
  border-color: rgba(0, 184, 204, 0.3);
}

.action-btn--edit:hover { background: rgba(0, 184, 204, 0.2); }

.action-btn--delete {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border-color: rgba(239, 68, 68, 0.3);
}

.action-btn--delete:hover { background: rgba(239, 68, 68, 0.2); }

/* ── Modal ── */
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 50;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.modal-box {
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-radius: 1.5rem;
  padding: 2rem;
  width: 100%;
  max-width: 640px;
  max-height: 90vh;
  overflow-y: auto;
}

[data-theme="light"] .modal-box {
  background: #ffffff;
  border-color: #94a3b8;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  color: var(--text-primary);
}

.field { display: flex; flex-direction: column; gap: 0.4rem; margin-bottom: 1rem; }
.field-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }

@media (max-width: 540px) { .field-row { grid-template-columns: 1fr; } }

.field-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--text-dim);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.field-input {
  background: var(--bg-site);
  border: 1px solid var(--border-subtle);
  border-radius: 0.6rem;
  padding: 0.6rem 0.85rem;
  color: var(--text-primary);
  font-size: 0.9rem;
  width: 100%;
  outline: none;
  transition: border-color 0.2s ease;
  font-family: inherit;
}

.field-input:focus { border-color: #7000ff; }

[data-theme="light"] .field-input {
  background: #f8fafc;
  border-color: #94a3b8;
  color: #0f172a;
}

textarea.field-input { resize: vertical; }

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

.btn-cancel {
  padding: 0.65rem 1.5rem;
  border-radius: 9999px;
  border: 1px solid var(--border-subtle);
  background: transparent;
  color: var(--text-dim);
  font-weight: 700;
  cursor: pointer;
  transition: background 0.15s ease;
}

.btn-cancel:hover { background: var(--bg-panel-light); }

.btn-save {
  padding: 0.65rem 1.75rem;
  border-radius: 9999px;
  background: #7000ff;
  color: #fff;
  border: none;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s ease;
}

.btn-save:hover { background: #5a00d4; }

</style>
