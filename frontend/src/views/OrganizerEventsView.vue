<template>
  <div class="org-events-page">
    <div class="container mx-auto px-6 max-w-6xl">
      <div class="page-header">
        <div>
          <h1 class="page-title">My Events</h1>
          <p class="page-sub">All events you've created.</p>
        </div>
        <router-link to="/organizer/create" class="btn-create">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          Create Event
        </router-link>
      </div>

      <div v-if="loading" class="state-center"><div class="spinner"></div></div>

      <div v-else-if="events.length === 0" class="empty-state">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" :style="{ color: 'var(--text-muted)' }">
          <rect x="3" y="4" width="18" height="18" rx="2"/>
          <line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/>
          <line x1="3" y1="10" x2="21" y2="10"/>
        </svg>
        <p>No events yet. <router-link to="/organizer/create" class="link">Create your first event →</router-link></p>
      </div>

      <div v-else>
        <!-- Table -->
        <div class="table-card">
          <div class="table-scroll">
            <table class="events-table">
              <thead>
                <tr>
                  <th>Event</th><th>Date</th><th>City</th>
                  <th>Registrations</th><th>Capacity</th>
                  <th>Revenue (₹)</th><th>Status</th><th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="event in events" :key="event.event_id" class="table-row" :class="{ 'table-row--inactive': !event.is_active }">
                  <td class="td-name">
                    {{ event.title }}
                    <span v-if="!event.is_active" class="cancelled-badge">Cancelled</span>
                  </td>
                  <td class="td-dim">{{ new Date(event.event_date).toLocaleDateString('en-GB') }}</td>
                  <td class="td-dim">{{ event.venue_city }}</td>
                  <td class="td-dim">{{ event.registrations }}</td>
                  <td class="td-dim">{{ event.capacity }}</td>
                  <td class="td-revenue">{{ event.revenue.toLocaleString() }}</td>
                  <td>
                    <span class="perf-badge" :class="'perf--' + event.performance_label.toLowerCase()">
                      {{ event.performance_label }}
                    </span>
                  </td>
                  <td>
                    <div class="action-btns">
                      <router-link :to="'/events/' + event.event_id" class="action-btn">View</router-link>
                      <span
                        v-if="!event.is_active"
                        class="action-btn action-btn--edit action-btn--disabled"
                        title="Event has been cancelled"
                      >Edit</span>
                      <router-link
                        v-else
                        :to="'/organizer/edit/' + event.event_id"
                        class="action-btn action-btn--edit"
                      >Edit</router-link>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { organizerApi } from '../services/api';

const loading = ref(true);
const events  = ref<any[]>([]);

onMounted(async () => {
  loading.value = true;
  try { events.value = (await organizerApi.getDashboard()).data; }
  finally { loading.value = false; }
});
</script>

<style scoped>
.org-events-page { min-height: 100vh; background: var(--bg-site); padding: 7rem 0 4rem; }

.page-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2rem; flex-wrap: wrap; gap: 1rem; }
.page-title  { font-size: clamp(1.8rem, 4vw, 2.8rem); font-weight: 900; letter-spacing: -0.04em; color: var(--text-primary); }
.page-sub    { font-size: 0.88rem; color: var(--text-muted); margin-top: 0.25rem; }

.btn-create { display: inline-flex; align-items: center; gap: 0.45rem; padding: 0.72rem 1.4rem; background: var(--brand-accent); color: #000; font-weight: 800; font-size: 0.88rem; border-radius: 9999px; text-decoration: none; transition: opacity 0.15s ease; }
.btn-create:hover { opacity: 0.85; }

.state-center { display: flex; justify-content: center; padding: 5rem; }
.spinner { width: 36px; height: 36px; border: 3px solid var(--border-subtle); border-top-color: var(--brand-accent); border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.empty-state { display: flex; flex-direction: column; align-items: center; gap: 1rem; padding: 5rem; text-align: center; color: var(--text-muted); font-size: 0.9rem; }
.link { color: var(--brand-accent); text-decoration: none; font-weight: 700; }

.table-card { background: var(--bg-panel); border: 1px solid var(--border-subtle); border-radius: 18px; overflow: hidden; }
[data-theme="light"] .table-card { background: #fff; border: 2px solid #94a3b8; box-shadow: 0 4px 16px rgba(0,0,0,0.07); }

.table-scroll { overflow-x: auto; }

.events-table { width: 100%; border-collapse: collapse; text-align: left; }
.events-table th { padding: 0.85rem 1.1rem; font-size: 0.62rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted); border-bottom: 1px solid var(--border-subtle); white-space: nowrap; }
[data-theme="light"] .events-table th { border-bottom: 2px solid #94a3b8; }

.table-row { border-bottom: 1px solid var(--border-subtle); transition: background 0.12s ease; }
.table-row:last-child { border-bottom: none; }
.table-row:hover { background: var(--bg-panel-light); }
[data-theme="light"] .table-row:hover { background: #fdf5e6; }

.events-table td { padding: 0.9rem 1.1rem; font-size: 0.88rem; }
.td-name    { font-weight: 700; color: var(--text-primary); max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.td-dim     { color: var(--text-dim); }
.td-revenue { font-weight: 800; color: var(--brand-accent); }
[data-theme="light"] .td-revenue { color: #0369a1; }

.perf-badge { display: inline-flex; padding: 0.25rem 0.65rem; border-radius: 9999px; font-size: 0.62rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; }
.perf--high   { background: rgba(0,223,216,0.12); color: #00dfd8; }
.perf--medium { background: rgba(255,171,0,0.12); color: #ffab00; }
.perf--low    { background: rgba(255,85,85,0.12); color: #ff5555; }
[data-theme="light"] .perf--high   { background: rgba(5,150,105,0.1);  color: #059669; }
[data-theme="light"] .perf--medium { background: rgba(217,119,6,0.1);  color: #d97706; }
[data-theme="light"] .perf--low    { background: rgba(220,38,38,0.1);  color: #dc2626; }

.action-btns { display: flex; gap: 0.4rem; }
.action-btn { padding: 0.35rem 0.75rem; border-radius: 7px; font-size: 0.78rem; font-weight: 700; text-decoration: none; background: var(--bg-panel-light); color: var(--text-dim); transition: background 0.12s ease; }
.action-btn:hover { background: var(--border-subtle); }
.action-btn--edit { color: var(--brand-accent); }

.action-btn--disabled {
  opacity: 0.35;
  cursor: not-allowed;
  pointer-events: none;
  color: var(--text-muted) !important;
}

.table-row--inactive td { opacity: 0.55; }

.cancelled-badge {
  display: inline-block;
  margin-left: 0.4rem;
  font-size: 0.6rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #f87171;
  background: rgba(248, 113, 113, 0.12);
  border: 1px solid rgba(248, 113, 113, 0.3);
  border-radius: 4px;
  padding: 0.1rem 0.35rem;
  vertical-align: middle;
}
</style>