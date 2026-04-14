<template>
  <div class="udash-page">
    <div class="container mx-auto px-6 max-w-4xl">
      <div class="page-header">
        <h1 class="page-title">My Dashboard</h1>
        <p class="page-sub">Your referral activity and stats.</p>
      </div>

      <div v-if="loading" class="state-center"><div class="spinner"></div></div>

      <div v-else class="dash-body">

        <!-- Referral code card -->
        <div class="ref-card">
          <p class="ref-label">Your Referral Code</p>
          <div class="ref-code-row">
            <span class="ref-code">{{ data.referral_code || '—' }}</span>
            <button class="copy-btn" @click="copyCode" :class="{ 'copy-btn--done': copied }">
              {{ copied ? '✓ Copied' : 'Copy' }}
            </button>
          </div>
          <p class="ref-hint">Share this code. When someone registers using it they get 5% off and you earn 5% of the ticket price in your wallet.</p>
        </div>

        <!-- Stats row -->
        <div class="stats-grid">
          <div class="stat-card">
            <span class="stat-label">Total Referrals</span>
            <span class="stat-value">{{ data.total_referrals ?? 0 }}</span>
          </div>
          <div class="stat-card">
            <span class="stat-label">Wallet Balance</span>
            <span class="stat-value stat-value--accent">🪙 ₹{{ walletBalance.toFixed(2) }}</span>
          </div>
        </div>

        <!-- Referred users list -->
        <div class="table-card" v-if="data.referrals?.length">
          <p class="section-title">People You've Referred</p>
          <div class="ref-list">
            <div v-for="r in data.referrals" :key="r.id" class="ref-row">
              <div class="ref-avatar">{{ r.name[0].toUpperCase() }}</div>
              <div class="ref-info">
                <p class="ref-name">{{ r.name }}</p>
                <p class="ref-date">Joined {{ new Date(r.joined_at).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }) }}</p>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          <p>No referrals yet. Share your code to start earning!</p>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../services/api';

const loading      = ref(true);
const data         = ref<any>({});
const walletBalance = ref(0);
const copied       = ref(false);

onMounted(async () => {
  loading.value = true;
  try {
    const [refRes, walletRes] = await Promise.all([
      api.get('/auth/my-referrals'),
      api.get('/wallet'),
    ]);
    data.value         = refRes.data;
    walletBalance.value = walletRes.data.wallet?.balance ?? 0;
  } finally { loading.value = false; }
});

const copyCode = async () => {
  if (!data.value.referral_code) return;
  await navigator.clipboard.writeText(data.value.referral_code);
  copied.value = true;
  setTimeout(() => copied.value = false, 2000);
};
</script>

<style scoped>
.udash-page { min-height: 100vh; background: var(--bg-site); padding: 7rem 0 4rem; }
.page-header { margin-bottom: 2rem; }
.page-title  { font-size: clamp(1.8rem, 4vw, 2.8rem); font-weight: 900; letter-spacing: -0.04em; color: var(--text-primary); }
.page-sub    { font-size: 0.88rem; color: var(--text-muted); margin-top: 0.25rem; }

.dash-body { display: flex; flex-direction: column; gap: 1.25rem; }

.state-center { display: flex; justify-content: center; padding: 5rem; }
.spinner { width: 36px; height: 36px; border: 3px solid var(--border-subtle); border-top-color: var(--brand-accent); border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Referral card */
.ref-card { background: var(--bg-panel); border: 1px solid var(--border-subtle); border-radius: 18px; padding: 1.75rem; }
[data-theme="light"] .ref-card { background: #fff; border: 2px solid #94a3b8; box-shadow: 0 4px 16px rgba(0,0,0,0.07); }

.ref-label { font-size: 0.68rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.15em; color: var(--text-muted); margin-bottom: 0.75rem; }

.ref-code-row { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem; }

.ref-code { font-size: 1.6rem; font-weight: 900; letter-spacing: 0.1em; color: var(--brand-accent); }
[data-theme="light"] .ref-code { color: #0369a1; }

.copy-btn { padding: 0.45rem 1rem; border-radius: 8px; border: 1px solid var(--brand-accent); color: var(--brand-accent); background: transparent; font-weight: 700; font-size: 0.82rem; cursor: pointer; font-family: inherit; transition: all 0.15s ease; }
.copy-btn:hover { background: var(--brand-accent); color: #000; }
.copy-btn--done { background: var(--brand-accent) !important; color: #000 !important; }
[data-theme="light"] .copy-btn { border-color: #0369a1; color: #0369a1; }

.ref-hint { font-size: 0.78rem; color: var(--text-muted); line-height: 1.55; }

/* Stats */
.stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.stat-card { background: var(--bg-panel); border: 1px solid var(--border-subtle); border-radius: 14px; padding: 1.4rem; display: flex; flex-direction: column; gap: 0.4rem; }
[data-theme="light"] .stat-card { background: #fff; border: 2px solid #94a3b8; box-shadow: 0 3px 10px rgba(0,0,0,0.06); }
.stat-label { font-size: 0.62rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.12em; color: var(--text-muted); }
.stat-value { font-size: 2rem; font-weight: 900; letter-spacing: -0.04em; color: var(--text-primary); line-height: 1; }
.stat-value--accent { color: var(--brand-accent); }
[data-theme="light"] .stat-value--accent { color: #0369a1; }

/* Referred list */
.table-card { background: var(--bg-panel); border: 1px solid var(--border-subtle); border-radius: 18px; padding: 1.75rem; }
[data-theme="light"] .table-card { background: #fff; border: 2px solid #94a3b8; box-shadow: 0 4px 16px rgba(0,0,0,0.07); }

.section-title { font-size: 0.68rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.15em; color: var(--text-dim); margin-bottom: 1rem; }

.ref-list { display: flex; flex-direction: column; }
.ref-row { display: flex; align-items: center; gap: 0.85rem; padding: 0.75rem 0; border-bottom: 1px solid var(--border-subtle); }
.ref-row:last-child { border-bottom: none; }

.ref-avatar { width: 36px; height: 36px; border-radius: 50%; background: color-mix(in srgb, var(--brand-accent) 15%, transparent); color: var(--brand-accent); font-size: 0.9rem; font-weight: 900; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.ref-name   { font-size: 0.88rem; font-weight: 700; color: var(--text-primary); }
.ref-date   { font-size: 0.72rem; color: var(--text-muted); margin-top: 0.1rem; }

.empty-state { text-align: center; color: var(--text-muted); font-size: 0.88rem; padding: 2rem; background: var(--bg-panel); border: 1px solid var(--border-subtle); border-radius: 14px; }
</style>