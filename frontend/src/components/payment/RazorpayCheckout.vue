<template>
  <div class="checkout-modal" v-if="isOpen">
    <div class="modal-backdrop" @click.self="handleBackdropClick" />

    <div class="checkout-card">
      <!-- Header -->
      <div class="checkout-header">
        <div class="header-left">
          <span class="secure-badge">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            Secure Payment
          </span>
          <h3 class="modal-title">Complete Registration</h3>
        </div>
        <button class="close-btn" @click="$emit('close')" aria-label="Close">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>

      <!-- Order summary -->
      <div class="order-summary">
        <div class="order-id-row">
          <span class="field-label">Order Reference</span>
          <span class="order-id-val">{{ orderData.order_id }}</span>
        </div>

        <!-- Price breakdown (only shown when discounts/wallet apply) -->
        <div v-if="(orderData.discount_amount ?? 0) > 0 || (orderData.wallet_used ?? 0) > 0" class="breakdown-block">
          <div class="breakdown-row">
            <span>Base Price</span>
            <span>₹{{ basePriceDisplay }}</span>
          </div>
          <div v-if="(orderData.discount_amount ?? 0) > 0" class="breakdown-row breakdown-row--discount">
            <span>
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              Referral Discount (5%)
            </span>
            <span>−₹{{ (orderData.discount_amount ?? 0).toFixed(2) }}</span>
          </div>
          <div v-if="(orderData.wallet_used ?? 0) > 0" class="breakdown-row breakdown-row--wallet">
            <span>🪙 Wallet Credit</span>
            <span>−₹{{ (orderData.wallet_used ?? 0).toFixed(2) }}</span>
          </div>
          <div class="breakdown-divider" />
        </div>

        <!-- Final amount -->
        <div class="amount-block">
          <span class="field-label">{{ (orderData.wallet_used ?? 0) > 0 ? 'Amount via Razorpay' : 'Total Amount' }}</span>
          <span class="amount-value">₹{{ (orderData.final_price ?? (orderData.amount / 100)).toFixed(2) }}</span>
        </div>
      </div>

      <!-- Pay action -->
      <div class="pay-section">
        <div class="rzp-branding">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          Powered by Razorpay · UPI, Cards, Net Banking & more
        </div>

        <button
          class="pay-btn"
          @click="openRazorpay"
          :disabled="processing || !razorpayLoaded"
        >
          <span v-if="processing" class="btn-spinner" />
          {{ processing ? 'Verifying…' : !razorpayLoaded ? 'Loading…' : `Pay ₹${(orderData.final_price ?? (orderData.amount / 100)).toFixed(2)}` }}
        </button>

        <p v-if="errorMsg" class="error-inline">{{ errorMsg }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../../stores/auth';

const props = defineProps<{
  isOpen: boolean;
  orderData: {
    order_id: string;
    amount: number;
    key_id: string;
    final_price?: number;
    discount_amount?: number;
    wallet_used?: number;
  };
  eventId: string;
}>();

const emit = defineEmits(['close', 'success', 'error']);
const authStore = useAuthStore();
const processing = ref(false);
const razorpayLoaded = ref(false);
const errorMsg = ref('');

const basePriceDisplay = computed(() => {
  const base = (props.orderData.final_price ?? 0)
    + (props.orderData.discount_amount ?? 0)
    + (props.orderData.wallet_used ?? 0);
  return base.toFixed(2);
});

const handleBackdropClick = () => {
  // Backdrop click counts as dismissal — emit error so wallet refund fires
  emit('error', 'Payment was not completed. Please try again.');
};

const loadRazorpayScript = (): Promise<void> => {
  return new Promise((resolve, reject) => {
    if ((window as any).Razorpay) { resolve(); return; }
    const script = document.createElement('script');
    script.src = 'https://checkout.razorpay.com/v1/checkout.js';
    script.onload = () => resolve();
    script.onerror = () => reject(new Error('Failed to load Razorpay SDK'));
    document.body.appendChild(script);
  });
};

onMounted(async () => {
  try {
    await loadRazorpayScript();
    razorpayLoaded.value = true;
  } catch {
    errorMsg.value = 'Could not load payment SDK. Check your connection.';
  }
});

const openRazorpay = () => {
  errorMsg.value = '';
  const options = {
    key: props.orderData.key_id,
    amount: props.orderData.amount,
    currency: 'INR',
    name: 'SyntaxError Events',
    description: 'Event Registration',
    order_id: props.orderData.order_id,
    handler: async function (response: any) {
      processing.value = true;
      try {
        const res = await axios.post(
          '/api/payments/verify',
          {
            razorpay_order_id: response.razorpay_order_id,
            razorpay_payment_id: response.razorpay_payment_id,
            razorpay_signature: response.razorpay_signature,
          },
          { headers: { Authorization: `Bearer ${authStore.token}` } }
        );
        emit('success', res.data);
      } catch (err: any) {
        emit('error', err.response?.data?.message || 'Payment verification failed.');
      } finally {
        processing.value = false;
      }
    },
    prefill: {
      name: (authStore.user as any)?.name || '',
      email: (authStore.user as any)?.email || '',
    },
    theme: { color: '#0070f3' },
    modal: {
      ondismiss: () => {
        emit('error', 'Payment was not completed. Please try again.');
      },
    },
  };
  const rzp = new (window as any).Razorpay(options);
  rzp.on('payment.failed', (response: any) => {
    emit('error', response.error?.description || 'Payment failed.');
  });
  rzp.open();
};
</script>

<style scoped>
/* ── Overlay ── */
.checkout-modal {
  position: fixed;
  inset: 0;
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  animation: fade-in 0.18s ease;
}

@keyframes fade-in {
  from { opacity: 0; }
  to   { opacity: 1; }
}

.modal-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(10px);
}

/* ── Card ── */
.checkout-card {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 460px;
  background: var(--bg-panel-solid);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.45), 0 0 0 1px rgba(255,255,255,0.04);
  animation: slide-up 0.22s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes slide-up {
  from { opacity: 0; transform: translateY(20px) scale(0.97); }
  to   { opacity: 1; transform: translateY(0)   scale(1); }
}

[data-theme="light"] .checkout-card {
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(0,0,0,0.06);
}

/* ── Header ── */
.checkout-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 1.75rem 1.75rem 0;
}

.header-left { display: flex; flex-direction: column; gap: 0.5rem; }

.secure-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.65rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--brand-primary);
  background: color-mix(in srgb, var(--brand-primary) 10%, transparent);
  border: 1px solid color-mix(in srgb, var(--brand-primary) 25%, transparent);
  padding: 0.25rem 0.6rem;
  border-radius: 9999px;
  width: fit-content;
}

.modal-title {
  font-size: 1.55rem;
  font-weight: 900;
  letter-spacing: -0.04em;
  color: var(--text-primary);
  line-height: 1.1;
}

.close-btn {
  background: var(--bg-panel-light);
  border: 1px solid var(--border-subtle);
  border-radius: 9px;
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--text-muted);
  flex-shrink: 0;
  transition: background 0.15s ease, color 0.15s ease;
}
.close-btn:hover { background: var(--border-subtle); color: var(--text-primary); }

/* ── Order summary block ── */
.order-summary {
  margin: 1.25rem 1.75rem;
  background: var(--bg-panel-light);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  overflow: hidden;
}

.order-id-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.85rem 1.1rem;
  border-bottom: 1px solid var(--border-subtle);
}

.field-label {
  font-size: 0.62rem;
  font-weight: 900;
  letter-spacing: 0.13em;
  text-transform: uppercase;
  color: var(--text-muted);
}

.order-id-val {
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--text-dim);
  font-family: 'Courier New', monospace;
  letter-spacing: 0.04em;
}

/* ── Price breakdown ── */
.breakdown-block {
  padding: 0.85rem 1.1rem 0;
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.breakdown-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.82rem;
  color: var(--text-dim);
  gap: 0.5rem;
}

.breakdown-row span:first-child {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.breakdown-row--discount { color: #22c55e; }
.breakdown-row--wallet   { color: var(--brand-accent); }

.breakdown-divider {
  height: 1px;
  background: var(--border-subtle);
  margin-top: 0.5rem;
}

/* ── Amount block ── */
.amount-block {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.1rem;
}

.amount-value {
  font-size: 1.9rem;
  font-weight: 900;
  letter-spacing: -0.04em;
  color: var(--brand-primary);
  line-height: 1;
}

/* ── Pay section ── */
.pay-section {
  padding: 0 1.75rem 1.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.rzp-branding {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.72rem;
  color: var(--text-muted);
  justify-content: center;
}

.pay-btn {
  width: 100%;
  padding: 1rem;
  border-radius: 12px;
  border: none;
  background: var(--brand-primary);
  color: #000;
  font-size: 1rem;
  font-weight: 900;
  font-family: inherit;
  letter-spacing: -0.01em;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  transition: filter 0.15s ease, transform 0.15s ease, box-shadow 0.15s ease;
}

.pay-btn:hover:not(:disabled) {
  filter: brightness(1.08);
  transform: translateY(-1px);
  box-shadow: 0 8px 24px color-mix(in srgb, var(--brand-primary) 35%, transparent);
}

.pay-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(0,0,0,0.3);
  border-top-color: #000;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  flex-shrink: 0;
}

@keyframes spin { to { transform: rotate(360deg); } }

.error-inline {
  font-size: 0.8rem;
  color: #f87171;
  text-align: center;
  line-height: 1.4;
}
</style>