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

          <div class="header-actions">
            <button @click="fetchData" :disabled="loading" class="refresh-btn">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2.5"
                :class="{ 'animate-spin': loading }">
                <path d="M23 4v6h-6"/>
                <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
              </svg>
              Re-Sync Platform
            </button>
          </div>
        </div>

        <!-- ── Tab Bar ── -->
        <div class="tab-bar">
          <button
            class="tab-btn"
            :class="{ 'tab-btn--active': activeTab === 'analytics' }"
            @click="activeTab = 'analytics'"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
            </svg>
            Analytics
          </button>
          <button
            class="tab-btn"
            :class="{ 'tab-btn--active': activeTab === 'events' }"
            @click="activeTab = 'events'; fetchAllEvents()"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
              <line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/>
              <line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
            Event Management
          </button>
        </div>

        <!-- ── Loading ── -->
        <div v-if="loading && activeTab === 'analytics'" class="state-center">
          <div class="spinner"></div>
          <span class="state-label">Fetching Intelligence…</span>
        </div>

        <!-- ── Error ── -->
        <div v-else-if="error && activeTab === 'analytics'" class="error-banner">
          <span class="text-2xl">⚠️</span>
          <span>{{ error }}</span>
        </div>

        <!-- ── Analytics Tab ── -->
        <div v-else-if="activeTab === 'analytics'" class="dashboard-body">

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

        <!-- ── Event Management Tab ── -->
        <div v-else-if="activeTab === 'events'" class="dashboard-body">

          <!-- Toolbar -->
          <div class="em-toolbar">
            <div class="em-search-wrap">
              <svg class="em-search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
              </svg>
              <input
                v-model="eventSearch"
                type="text"
                class="em-search"
                placeholder="Search events by title, city, or sport…"
                id="admin-event-search"
              />
            </div>
            <button class="create-event-btn" @click="openCreateModal">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2.5"
                stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
              Create Event
            </button>
          </div>

          <!-- Loading state -->
          <div v-if="loadingEvents" class="state-center">
            <div class="spinner"></div>
            <span class="state-label">Loading Events…</span>
          </div>

          <!-- Events table -->
          <div v-else class="dash-card overflow-hidden">
            <div class="overflow-x-auto">
              <table class="leaderboard-table">
                <thead>
                  <tr class="table-header-row">
                    <th class="th">#</th>
                    <th class="th">Title</th>
                    <th class="th">Organizer ID</th>
                    <th class="th">Sport</th>
                    <th class="th">City</th>
                    <th class="th">Date</th>
                    <th class="th">Capacity</th>
                    <th class="th">Price (₹)</th>
                    <th class="th">Status</th>
                    <th class="th">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="ev in filteredEvents" :key="ev.id" class="table-body-row">
                    <td class="td td--muted">{{ ev.id }}</td>
                    <td class="td td--name">{{ ev.title }}</td>
                    <td class="td td--dim">{{ ev.organizer_id }}</td>
                    <td class="td td--dim">{{ ev.sport_category }}</td>
                    <td class="td td--dim">{{ ev.venue_city || '—' }}</td>
                    <td class="td td--dim">{{ new Date(ev.event_date).toLocaleDateString('en-GB') }}</td>
                    <td class="td td--dim">{{ ev.capacity }}</td>
                    <td class="td td--revenue">{{ ev.price }}</td>
                    <td class="td">
                      <span class="status-badge" :class="ev.is_active ? 'status-badge--active' : 'status-badge--inactive'">
                        {{ ev.is_active ? 'Active' : 'Inactive' }}
                      </span>
                    </td>
                    <td class="td">
                      <button @click="openEditModal(ev)" class="action-btn action-btn--edit">Edit</button>
                    </td>
                  </tr>
                  <tr v-if="filteredEvents.length === 0">
                    <td colspan="10" class="td td--muted" style="text-align:center;padding:3rem;">No events found.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- ── Create / Edit Event Modal ── -->
    <div v-if="showEventModal" class="modal-overlay" @click.self="showEventModal = false">
      <div class="modal-box">
        <h2 class="modal-title">{{ editingEvent ? 'Edit Event' : 'Create Event' }}</h2>
        <form @submit.prevent="saveEvent">

          <div class="field">
            <label class="field-label">Title *</label>
            <input v-model="eventForm.title" type="text" class="field-input" required />
          </div>

          <div class="field">
            <label class="field-label">Description</label>
            <textarea v-model="eventForm.description" class="field-input" rows="3"></textarea>
          </div>

          <div class="field-row">
            <div class="field">
              <label class="field-label">Sport Category</label>
              <select v-model="eventForm.sport_category" class="field-input">
                <option>Football</option><option>Basketball</option>
                <option>Tennis</option><option>Cricket</option>
                <option>Swimming</option><option>Other</option>
              </select>
            </div>
            <div class="field">
              <label class="field-label">Event Date & Time *</label>
              <input v-model="eventForm.event_date" type="datetime-local" class="field-input" required />
            </div>
          </div>

          <div class="field-row">
            <div class="field">
              <label class="field-label">City</label>
              <input v-model="eventForm.venue_city" type="text" class="field-input" />
            </div>
            <div class="field">
              <label class="field-label">Venue Address</label>
              <input v-model="eventForm.venue_address" type="text" class="field-input" />
            </div>
          </div>

          <div class="field-row">
            <div class="field">
              <label class="field-label">Capacity *</label>
              <input v-model="eventForm.capacity" type="number" min="1" class="field-input" required />
            </div>
            <div class="field">
              <label class="field-label">Price / Entry Fee (₹) *</label>
              <input v-model="eventForm.price" type="number" min="0" class="field-input" required />
            </div>
          </div>

          <div class="field-row">
            <div class="field">
              <label class="field-label">Banner URL</label>
              <input v-model="eventForm.banner_url" type="text" class="field-input" placeholder="https://…" />
            </div>
            <div class="field">
              <label class="field-label">Organizer User ID</label>
              <input v-model="eventForm.organizer_id" type="number" class="field-input" placeholder="Leave blank to assign to self" />
            </div>
          </div>

          <div class="modal-actions">
            <button
              v-if="editingEvent"
              type="button"
              @click="deleteEventFromModal(editingEvent)"
              class="btn-delete"
            >Delete Event</button>
            <div class="modal-actions-right">
              <button type="button" @click="showEventModal = false" class="btn-cancel">Cancel</button>
              <button type="submit" class="btn-save">{{ editingEvent ? 'Save Changes' : 'Create Event' }}</button>
            </div>
          </div>

        </form>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { adminApi, eventApi } from '../services/api';
import MonthlyTrendChart from '../components/charts/MonthlyTrendChart.vue';
import CityDistributionChart from '../components/charts/CityDistributionChart.vue';
import FillRateChart from '../components/charts/FillRateChart.vue';
import OrganizerComparisonChart from '../components/charts/OrganizerComparisonChart.vue';
import SportDonutChart from '../components/charts/SportDonutChart.vue';

// ── Tab state ──
const activeTab = ref<'analytics' | 'events'>('analytics');

// ── Analytics state ──
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

// ── Event Management state ──
const allEvents     = ref<any[]>([]);
const loadingEvents = ref(false);
const eventSearch   = ref('');
const showEventModal  = ref(false);
const editingEvent    = ref<any>(null);

const eventForm = ref({
  title: '', description: '', sport_category: 'Football',
  event_date: '', venue_city: '', venue_address: '',
  capacity: 100, price: 0, banner_url: '', organizer_id: '' as string | number
});

const filteredEvents = computed(() => {
  const q = eventSearch.value.toLowerCase().trim();
  if (!q) return allEvents.value;
  return allEvents.value.filter(e =>
    e.title?.toLowerCase().includes(q) ||
    e.venue_city?.toLowerCase().includes(q) ||
    e.sport_category?.toLowerCase().includes(q)
  );
});

const fetchAllEvents = async () => {
  loadingEvents.value = true;
  try {
    const res = await adminApi.getAllEvents();
    allEvents.value = res.data;
  } catch { /* silent */ } finally {
    loadingEvents.value = false;
  }
};

const openCreateModal = () => {
  editingEvent.value = null;
  eventForm.value = {
    title: '', description: '', sport_category: 'Football',
    event_date: '', venue_city: '', venue_address: '',
    capacity: 100, price: 0, banner_url: '', organizer_id: ''
  };
  showEventModal.value = true;
};

const openEditModal = (ev: any) => {
  editingEvent.value = ev;
  eventForm.value = {
    title: ev.title,
    description: ev.description || '',
    sport_category: ev.sport_category,
    event_date: ev.event_date?.slice(0, 16) || '',
    venue_city: ev.venue_city || '',
    venue_address: ev.venue_address || '',
    capacity: ev.capacity,
    price: ev.price,
    banner_url: ev.banner_url || '',
    organizer_id: ev.organizer_id
  };
  showEventModal.value = true;
};

const saveEvent = async () => {
  try {
    const payload: any = {
      ...eventForm.value,
      event_date: new Date(eventForm.value.event_date).toISOString()
    };
    // Strip empty organizer_id so backend defaults to admin's own user_id
    if (payload.organizer_id === '' || payload.organizer_id === null || payload.organizer_id === undefined) {
      delete payload.organizer_id;
    } else {
      payload.organizer_id = Number(payload.organizer_id);
    }
    if (editingEvent.value) {
      await eventApi.update(String(editingEvent.value.id), payload);
    } else {
      await eventApi.create(payload);
    }
    showEventModal.value = false;
    await fetchAllEvents();
  } catch (err: any) {
    alert('Error: ' + (err.response?.data?.message || 'Unknown error'));
  }
};

const deleteEventFromModal = async (ev: any) => {
  if (!confirm(`Delete "${ev.title}"? This cannot be undone.`)) return;
  try {
    await eventApi.delete(String(ev.id));
    showEventModal.value = false;
    await fetchAllEvents();
  } catch (err: any) {
    alert('Error deleting: ' + (err.response?.data?.message || ''));
  }
};


onMounted(() => {
  fetchData();
  fetchAllEvents();
});
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
  margin-bottom: 2.5rem;
}

@media (min-width: 768px) {
  .admin-header {
    flex-direction: row;
    align-items: flex-end;
  }
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-shrink: 0;
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
   TAB BAR
══════════════════════════════════════════ */
.tab-bar {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-radius: 9999px;
  padding: 0.35rem;
  width: fit-content;
}

[data-theme="light"] .tab-bar {
  background: #ffffff;
  border-color: #94a3b8;
}

.tab-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.25rem;
  border-radius: 9999px;
  border: none;
  background: transparent;
  color: var(--text-dim);
  font-size: 0.85rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s ease, color 0.2s ease;
}

.tab-btn--active {
  background: #7000ff;
  color: #fff;
}

.tab-btn:not(.tab-btn--active):hover {
  background: var(--bg-panel-light);
  color: var(--text-primary);
}

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

[data-theme="light"] .stat-card {
  background: #ffffff;
  border-color: #64748b;
  box-shadow: 0 0 0 2px #64748b, 0 6px 24px rgba(0,0,0,0.1);
}

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
   DASHBOARD CARDS
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
   EVENT MANAGEMENT TOOLBAR
══════════════════════════════════════════ */
.em-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.em-search-wrap {
  position: relative;
  flex: 1;
  min-width: 220px;
  max-width: 480px;
}

.em-search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  pointer-events: none;
}

.em-search {
  width: 100%;
  padding: 0.7rem 1rem 0.7rem 2.75rem;
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-radius: 9999px;
  color: var(--text-primary);
  font-size: 0.9rem;
  outline: none;
  transition: border-color 0.2s ease;
}

.em-search:focus { border-color: #7000ff; }

[data-theme="light"] .em-search {
  background: #ffffff;
  border-color: #94a3b8;
}

.create-event-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #7000ff;
  color: #fff;
  border: none;
  border-radius: 9999px;
  font-weight: 800;
  font-size: 0.88rem;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.15s ease;
  white-space: nowrap;
  flex-shrink: 0;
}

.create-event-btn:hover {
  background: #5a00d4;
  transform: translateY(-1px);
}

/* ══════════════════════════════════════════
   STATUS BADGES
══════════════════════════════════════════ */
.status-badge {
  display: inline-flex;
  padding: 0.25rem 0.65rem;
  border-radius: 9999px;
  font-size: 0.65rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.status-badge--active {
  background: rgba(0,223,216,0.12);
  color: #00dfd8;
}

.status-badge--inactive {
  background: rgba(239,68,68,0.1);
  color: #ef4444;
}

[data-theme="light"] .status-badge--active { background: rgba(5,150,105,0.1); color: #059669; }
[data-theme="light"] .status-badge--inactive { background: rgba(220,38,38,0.1); color: #dc2626; }

/* ══════════════════════════════════════════
   ACTION BUTTONS IN TABLE
══════════════════════════════════════════ */
.td-actions {
  display: flex;
  gap: 0.5rem;
}

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

/* ══════════════════════════════════════════
   LEADERBOARD TABLE (shared)
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

/* ══════════════════════════════════════════
   MODAL
══════════════════════════════════════════ */
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
  max-width: 680px;
  max-height: 90vh;
  overflow-y: auto;
}

[data-theme="light"] .modal-box {
  background: #ffffff;
  border-color: #94a3b8;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}

.modal-title {
  font-size: 1.3rem;
  font-weight: 900;
  margin-bottom: 1.75rem;
  color: var(--text-primary);
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin-bottom: 1rem;
}

.field-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

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
  padding: 0.65rem 0.9rem;
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
  align-items: center;
  justify-content: space-between;
  margin-top: 1.75rem;
  gap: 1rem;
}

.modal-actions-right {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.btn-delete {
  padding: 0.65rem 1.5rem;
  border-radius: 9999px;
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s ease;
}

.btn-delete:hover { background: rgba(239, 68, 68, 0.22); }

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
