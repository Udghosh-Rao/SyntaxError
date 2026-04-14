<template>
  <div class="wallet-page">
    <div class="wallet-center">

      <!-- Balance card -->
      <div class="balance-card">
        <div class="balance-header">
          <div class="coin-icon">🪙</div>
          <div>
            <p class="balance-label">Your Wallet</p>
            <p class="balance-amount">₹{{ wallet?.balance?.toFixed(2) ?? '0.00' }}</p>
          </div>
        </div>
        <button class="btn-add" @click="showTopup = !showTopup">
          {{ showTopup ? '✕ Cancel' : '+ Add Funds' }}
        </button>
      </div>

      <!-- Top-up panel -->
      <transition name="slide">
        <div v-if="showTopup" class="topup-card">
          <p class="section-title">Add Funds</p>
          <div class="amount-grid">
            <button v-for="amt in quickAmounts" :key="amt"
              class="quick-amt" :class="{ 'quick-amt--active': topupAmount === amt }"
              @click="topupAmount = amt">₹{{ amt }}</button>
          </div>
          <div class="field mt-3">
            <label class="field-label">Custom Amount (₹)</label>
            <input v-model.number="topupAmount" type="number" min="1" class="field-input" placeholder="Enter amount" />
          </div>
          <div v-if="topupError" class="error-row">{{ topupError }}</div>
          <button class="btn-primary" :disabled="!topupAmount || topupLoading" @click="handleAddFunds">
            <span v-if="topupLoading" class="btn-spinner"></span>
            {{ topupLoading ? 'Processing…' : `Pay ₹${topupAmount || 0}` }}
          </button>
        </div>
      </transition>

      <!-- Transactions -->
      <div class="txn-card">
        <p class="section-title">Transaction History</p>
        <div v-if="loading" class="state-center">
          <div class="spinner"></div>
        </div>
        <div v-else-if="transactions.length === 0" class="empty-state">
          No transactions yet.
        </div>
        <div v-else class="txn-list">
          <div v-for="txn in transactions" :key="txn.id" class="txn-row">
            <div class="txn-icon" :class="'txn-icon--' + txn.type">
              {{ txn.type === 'credit' ? '↑' : txn.type === 'referral_bonus' ? '🎁' : '↓' }}
            </div>
            <div class="txn-info">
              <p class="txn-desc">{{ txn.description }}</p>
              <p class="txn-date">{{ new Date(txn.created_at).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }) }}</p>
            </div>
            <span class="txn-amount" :class="txn.amount > 0 ? 'txn-amount--credit' : 'txn-amount--debit'">
              {{ txn.amount > 0 ? '+' : '' }}₹{{ Math.abs(txn.amount).toFixed(2) }}
            </span>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../services/api';

const loading      = ref(true);
const wallet       = ref<any>(null);
const transactions = ref<any[]>([]);
const showTopup    = ref(false);
const topupAmount  = ref<number | null>(null);
const topupLoading = ref(false);
const topupError   = ref('');
const quickAmounts = [100, 250, 500, 1000];

const fetchWallet = async () => {
  loading.value = true;
  try {
    const res = await api.get('/wallet');
    wallet.value       = res.data.wallet;
    transactions.value = res.data.transactions;
  } finally { loading.value = false; }
};

onMounted(fetchWallet);

const handleAddFunds = async () => {
  if (!topupAmount.value || topupAmount.value < 1) return;
  topupLoading.value = true;
  topupError.value   = '';
  try {
    const res = await api.post('/wallet/add-funds', { amount: topupAmount.value });
    const { order_id, amount, currency, key_id } = res.data;

    const rzp = new (window as any).Razorpay({
      key:      key_id,
      amount,
      currency,
      order_id,
      name:     'LiveSports Wallet',
      description: 'Wallet top-up',
      handler: async (payment: any) => {
        await api.post('/wallet/verify-topup', {
          razorpay_order_id:   order_id,
          razorpay_payment_id: payment.razorpay_payment_id,
          razorpay_signature:  payment.razorpay_signature,
          amount:              topupAmount.value,
        });
        showTopup.value  = false;
        topupAmount.value = null;
        await fetchWallet();
      },
      modal: { ondismiss: () => { topupLoading.value = false; } },
    });
    rzp.open();
  } catch (err: any) {
    topupError.value = err.response?.data?.message || 'Payment failed.';
    topupLoading.value = false;
  }
};
</script>

<style scoped>
.wallet-page { min-height: 100vh; background: var(--bg-site); padding: 7rem 1rem 3rem; display: flex; align-items: flex-start; justify-content: center; }
.wallet-center { width: 100%; max-width: 480px; display: flex; flex-direction: column; gap: 1.25rem; }

.balance-card, .topup-card, .txn-card {
  background: var(--bg-panel-solid);
  border: 1px solid var(--border-subtle);
  border-radius: 20px; padding: 1.75rem;
}
[data-theme="light"] .balance-card,
[data-theme="light"] .topup-card,
[data-theme="light"] .txn-card { background: #fff; border: 2px solid #94a3b8; box-shadow: 0 4px 16px rgba(0,0,0,0.07); }

.balance-header { display: flex; align-items: center; gap: 1rem; margin-bottom: 1.25rem; }
.coin-icon  { font-size: 2.5rem; line-height: 1; }
.balance-label  { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted); }
.balance-amount { font-size: 2.4rem; font-weight: 900; letter-spacing: -0.04em; color: var(--text-primary); line-height: 1; }

.btn-add {
  width: 100%; padding: 0.72rem;
  border: 1.5px solid var(--brand-accent);
  color: var(--brand-accent); background: transparent;
  border-radius: 10px; font-weight: 800; font-size: 0.9rem;
  cursor: pointer; font-family: inherit;
  transition: background 0.15s ease, color 0.15s ease;
}
.btn-add:hover { background: var(--brand-accent); color: #000; }

.section-title { font-size: 0.68rem; font-weight: 900; text-transform: uppercase; letter-spacing: 0.15em; color: var(--text-dim); margin-bottom: 1rem; }

.amount-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.5rem; }
.quick-amt { padding: 0.55rem; border-radius: 8px; border: 1px solid var(--border-subtle); background: var(--bg-panel-light); color: var(--text-primary); font-weight: 700; font-size: 0.85rem; cursor: pointer; font-family: inherit; transition: all 0.12s ease; }
.quick-amt:hover { border-color: var(--brand-accent); }
.quick-amt--active { background: var(--brand-accent) !important; color: #000 !important; border-color: var(--brand-accent) !important; }

.field { display: flex; flex-direction: column; gap: 0.4rem; }
.field-label { font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.09em; color: var(--text-dim); }
.field-input { width: 100%; padding: 0.72rem 0.95rem; background: var(--bg-panel-light); border: 1px solid var(--border-subtle); border-radius: 10px; color: var(--text-primary); font-size: 0.9rem; font-family: inherit; outline: none; }
.field-input:focus { border-color: var(--brand-accent); }

.error-row { font-size: 0.8rem; color: #f87171; background: rgba(248,113,113,0.07); border: 1px solid rgba(248,113,113,0.18); border-radius: 8px; padding: 0.6rem 0.85rem; }

.btn-primary { display: inline-flex; align-items: center; justify-content: center; gap: 0.5rem; width: 100%; padding: 0.8rem; background: var(--brand-accent); color: #000; font-weight: 800; font-size: 0.9rem; font-family: inherit; border: none; border-radius: 10px; cursor: pointer; margin-top: 0.75rem; transition: opacity 0.15s ease; }
.btn-primary:disabled { opacity: 0.45; cursor: not-allowed; }
.btn-spinner { width: 14px; height: 14px; border: 2px solid rgba(0,0,0,0.25); border-top-color: #000; border-radius: 50%; animation: spin 0.6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.mt-3 { margin-top: 0.75rem; }

/* Transactions */
.state-center { display: flex; justify-content: center; padding: 2rem; }
.spinner { width: 28px; height: 28px; border: 2px solid var(--border-subtle); border-top-color: var(--brand-accent); border-radius: 50%; animation: spin 0.8s linear infinite; }
.empty-state { text-align: center; color: var(--text-muted); font-size: 0.85rem; padding: 1.5rem 0; }

.txn-list { display: flex; flex-direction: column; }
.txn-row { display: flex; align-items: center; gap: 0.85rem; padding: 0.8rem 0; border-bottom: 1px solid var(--border-subtle); }
.txn-row:last-child { border-bottom: none; }

.txn-icon { width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: 900; flex-shrink: 0; }
.txn-icon--credit       { background: rgba(34,197,94,0.12); color: #22c55e; }
.txn-icon--debit        { background: rgba(248,113,113,0.12); color: #f87171; }
.txn-icon--referral_bonus { background: rgba(0,243,255,0.12); color: var(--brand-accent); }

.txn-info { flex: 1; min-width: 0; }
.txn-desc { font-size: 0.82rem; font-weight: 600; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.txn-date { font-size: 0.72rem; color: var(--text-muted); margin-top: 0.15rem; }

.txn-amount { font-size: 0.92rem; font-weight: 800; flex-shrink: 0; }
.txn-amount--credit { color: #22c55e; }
.txn-amount--debit  { color: #f87171; }

.slide-enter-active, .slide-leave-active { transition: all 0.2s ease; }
.slide-enter-from, .slide-leave-to { opacity: 0; transform: translateY(-8px); }
</style>