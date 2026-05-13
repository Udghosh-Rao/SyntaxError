<template>
  <div class="events-page">
    <div class="container mx-auto px-6 max-w-5xl">
      <div class="page-header">
        <h1 class="page-title">My Events</h1>
        <p class="page-sub">All events you've registered for.</p>
      </div>

      <div v-if="loading" class="state-center"><div class="spinner"></div></div>

      <div v-else-if="registrations.length === 0" class="empty-state">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor"
          stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"
          :style="{ color: 'var(--text-muted)' }">
          <rect x="3" y="4" width="18" height="18" rx="2"/>
          <line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/>
          <line x1="3" y1="10" x2="21" y2="10"/>
        </svg>
        <p>No registrations yet. <router-link to="/home" class="link">Browse events →</router-link></p>
      </div>

      <div v-else class="reg-grid">
        <div v-for="reg in registrations" :key="reg.id" class="reg-card">

          <div class="reg-card-top">
            <span class="sport-badge">{{ reg.event?.sport_category }}</span>
            <span class="status-badge" :class="'status--' + reg.status">
              {{ reg.status }}
            </span>
          </div>

          <h3 class="reg-title">{{ reg.event?.title }}</h3>

          <div class="reg-meta">
            <span>📍 {{ reg.event?.venue_city }}</span>
            <span>📅 {{ reg.event ? new Date(reg.event.event_date).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }) : '' }}</span>
            <span>₹{{ reg.event?.price }}</span>
          </div>

          <div class="reg-footer">
            <router-link :to="'/events/' + reg.event_id" class="btn-view">View Event</router-link>
            <button v-if="reg.status === 'confirmed'" class="btn-cancel"
              @click="cancelReg(reg.id)">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { registrationApi } from '../services/api';

const loading       = ref(true);
const registrations = ref<any[]>([]);

const fetchRegs = async () => {
  loading.value = true;
  try { registrations.value = (await registrationApi.getMy()).data; }
  finally { loading.value = false; }
};

onMounted(fetchRegs);

const cancelReg = async (id: number) => {
  if (!confirm('Cancel this registration?')) return;
  await registrationApi.cancel(id);
  await fetchRegs();
};
</script>

<style scoped>
.events-page { min-height: 100vh; background: var(--bg-site); padding: 7rem 0 4rem; }
.page-header { margin-bottom: 2.5rem; }
.page-title  { font-size: clamp(1.8rem, 4vw, 2.8rem); font-weight: 900; letter-spacing: -0.04em; color: var(--text-primary); }
.page-sub    { font-size: 0.88rem; color: var(--text-muted); margin-top: 0.25rem; }

.state-center { display: flex; justify-content: center; padding: 5rem; }
.spinner { width: 36px; height: 36px; border: 3px solid var(--border-subtle); border-top-color: var(--brand-accent); border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.empty-state { display: flex; flex-direction: column; align-items: center; gap: 1rem; padding: 5rem; text-align: center; color: var(--text-muted); font-size: 0.9rem; }
.link { color: var(--brand-accent); text-decoration: none; font-weight: 700; }

.reg-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.25rem; }

.reg-card { background: var(--bg-panel); border: 1px solid var(--border-subtle); border-radius: 16px; padding: 1.5rem; display: flex; flex-direction: column; gap: 0.75rem; transition: border-color 0.2s ease; }
.reg-card:hover { border-color: var(--border-premium); }
[data-theme="light"] .reg-card { background: #fff; border: 2px solid #94a3b8; box-shadow: 0 3px 12px rgba(0,0,0,0.06); }

.reg-card-top { display: flex; align-items: center; justify-content: space-between; }

.sport-badge { font-size: 0.65rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.1em; padding: 0.25rem 0.7rem; border-radius: 9999px; background: color-mix(in srgb, var(--brand-accent) 12%, transparent); color: var(--brand-accent); }
[data-theme="light"] .sport-badge { color: #15803d; background: rgba(22,163,74,0.1); }

.status-badge { font-size: 0.65rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; padding: 0.25rem 0.7rem; border-radius: 9999px; }
.status--confirmed { background: rgba(34,197,94,0.12); color: #22c55e; }
.status--pending   { background: rgba(255,171,0,0.12); color: #ffab00; }
.status--cancelled { background: rgba(248,113,113,0.12); color: #f87171; }

.reg-title { font-size: 1.05rem; font-weight: 800; color: var(--text-primary); letter-spacing: -0.02em; }

.reg-meta { display: flex; flex-direction: column; gap: 0.3rem; font-size: 0.8rem; color: var(--text-dim); }

.reg-footer { display: flex; gap: 0.6rem; margin-top: 0.25rem; }

.btn-view { flex: 1; padding: 0.6rem; text-align: center; background: var(--brand-accent); color: #000; border-radius: 8px; font-weight: 800; font-size: 0.82rem; text-decoration: none; transition: opacity 0.15s ease; }
.btn-view:hover { opacity: 0.85; }

.btn-cancel { padding: 0.6rem 1rem; border: 1px solid rgba(248,113,113,0.4); color: #f87171; background: transparent; border-radius: 8px; font-weight: 700; font-size: 0.82rem; cursor: pointer; font-family: inherit; transition: background 0.15s ease; }
.btn-cancel:hover { background: rgba(248,113,113,0.1); }
</style>