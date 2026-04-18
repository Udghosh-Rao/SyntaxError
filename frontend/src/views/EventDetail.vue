<template>
  <div class="event-detail-page">
    <div class="party-bg-mesh">
      <div class="aura-blob aura-1"></div>
      <div class="aura-blob aura-2"></div>
      <div class="aura-blob aura-3"></div>
    </div>

    <div class="container py-12 relative z-10">
      <button @click="$router.push('/home')" class="back-btn-corp mb-12">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
        Back to Lineup
      </button>

      <div v-if="loading" class="loading-corp-full">
        <div class="pulse-loader"></div>
        <span class="tracking-widest font-900 uppercase text-sm mt-4">Syncing Event Data...</span>
      </div>

      <div v-else-if="error" class="error-panel">{{ error }}</div>

      <div v-else-if="event" class="detail-card animate-corp relative overflow-hidden">
        <div class="card-glow"></div>

        <div class="header-corp mb-12">
          <div class="header-main">
            <span class="sport-badge">{{ event.sport_category }}</span>
            <h1 class="hero-title-large mt-6">{{ event.title }}</h1>
          </div>
          <div class="tier-box-corp text-right">
            <span class="tier-label">ACCESS TIER</span>
            <span class="tier-value">{{ event.price_tier?.toUpperCase() }}</span>
          </div>
        </div>

        <div class="info-grid-corp mb-12">
          <div class="info-item">
            <label class="info-label">Event Location</label>
            <p class="info-value">{{ event.venue_city }}{{ event.venue_address ? `, ${event.venue_address}` : '' }}</p>
          </div>
          <div class="info-item">
            <label class="info-label">Event Date</label>
            <p class="info-value">{{ new Date(event.event_date).toLocaleDateString('en-GB', { day: '2-digit', month: 'long', year: 'numeric' }) }}</p>
          </div>
        </div>

        <div class="description-section mb-12">
          <label class="desc-label">The Details</label>
          <p class="desc-text">"{{ event.description || 'No description provided for this event.' }}"</p>
        </div>

        <div class="registration-panel-corp pt-12 border-t-section">
          <div class="stats-grid-corp mb-12">
            <div class="stat-box-corp">
              <span class="stat-label stat-label--pink">TICKET PRICE</span>
              <span class="stat-value">₹{{ event.price }}</span>
            </div>
            <div class="stat-box-corp">
              <span class="stat-label stat-label--cyan">TIX REMAINING</span>
              <span class="stat-value">{{ event.seats_remaining }}<span class="stat-sub">/ {{ event.capacity }}</span></span>
            </div>
          </div>

          <div class="action-portal-corp">
            <template v-if="!authStore.isAuthenticated">
              <div class="auth-prompt-corp text-center">
                <p class="auth-prompt-text">You need to be logged in to book this event.</p>
                <router-link to="/login" class="btn-book">Login to Access</router-link>
              </div>
            </template>

            <template v-else-if="authStore.isUser">
              <!-- Confirmed: show status + cancel button -->
              <div v-if="registrationStatus === 'confirmed'" class="status-panel-corp">
                <div class="status-info">
                  <label class="stat-label stat-label--cyan">ENTRY STATUS</label>
                  <p class="status-text">CONFIRMED</p>
                </div>
                <!-- Inline cancel confirmation -->
                <div v-if="showCancelConfirm" class="cancel-confirm-inline">
                  <p class="cancel-confirm-text">
                    ⚠️ Cancel this ticket? Any wallet amount used will be refunded.
                  </p>
                  <div class="cancel-confirm-actions">
                    <button @click="cancelRegistration" class="btn-confirm-cancel">Yes, Cancel</button>
                    <button @click="showCancelConfirm = false" class="btn-keep-ticket">Keep Ticket</button>
                  </div>
                </div>
                <button v-else @click="showCancelConfirm = true" class="btn-cancel-ticket">
                  Cancel Ticket
                </button>
              </div>

              <!-- Pending (payment initiated but not verified yet) -->
              <div v-else-if="registrationStatus === 'pending'" class="status-panel-corp status-panel-corp--pending">
                <div class="status-info">
                  <label class="stat-label stat-label--cyan">ENTRY STATUS</label>
                  <p class="status-text status-text--pending">PAYMENT PENDING</p>
                </div>
                <button @click="retryPayment" class="btn-retry-payment">
                  Retry Payment
                </button>
              </div>

              <!-- Payment failed: show notice + let user try again -->
              <div v-else-if="registrationStatus === 'payment_failed'" class="status-panel-corp status-panel-corp--failed">
                <div class="status-info w-full">
                  <label class="stat-label" style="color:#ff007f">PAYMENT FAILED</label>
                  <p class="status-text status-text--failed">Your payment did not go through. Any wallet amount used has been refunded.</p>
                  <button @click="resetAndRegisterAgain" class="btn-book mt-4">
                    Try Registering Again
                  </button>
                </div>
              </div>

              <div v-else-if="event.seats_remaining > 0" class="registration-form">
                <h4 class="reg-heading">Booking Details</h4>

                <div class="input-stack mb-6">
                  <label class="reg-field-label">SELECT YOUR ROLE</label>
                  <select v-model="regForm.role" class="reg-input">
                    <option value="athlete">Athlete / Fan</option>
                    <option value="sub_vendor">Service Provider / Referee / Medical</option>
                  </select>
                </div>

                <div v-if="regForm.role === 'athlete'" class="input-stack mb-6">
                  <label class="reg-field-label">CREW / SQUAD NAME (OPTIONAL)</label>
                  <input type="text" v-model="regForm.role_details.team" class="reg-input" placeholder="e.g. Neon Riders" />
                </div>

                <div v-if="regForm.role === 'sub_vendor'" class="input-stack mb-6">
                  <label class="reg-field-label">SERVICE TYPE</label>
                  <select v-model="regForm.role_details.service" class="reg-input">
                    <option value="catering">Drinks & Catering</option>
                    <option value="medical">Health & Safety</option>
                    <option value="logistics">Lighting / Audio Gear</option>
                  </select>
                </div>

                <!-- Referral code -->
                <div v-if="event.price > 0" class="input-stack mb-4">
                  <label class="reg-field-label">REFERRAL CODE (OPTIONAL)</label>
                  <div class="ref-input-row">
                    <input type="text" v-model="regForm.referral_code" class="reg-input ref-input"
                      placeholder="e.g. LS-A3FX92K1"
                      @input="debouncedValidate"
                      @blur="validateReferral" />
                    <span v-if="referralLoading" class="ref-status ref-status--loading">…</span>
                    <span v-else-if="referralMsg" class="ref-status"
                      :class="referralValid ? 'ref-status--ok' : 'ref-status--err'">
                      {{ referralMsg }}
                    </span>
                  </div>
                </div>

                <!-- Wallet balance -->
                <div v-if="event.price > 0 && walletBalance > 0" class="wallet-section mb-4">
                  <label class="wallet-toggle">
                    <input type="checkbox" v-model="regForm.use_wallet" class="wallet-checkbox" />
                    <span class="wallet-label">
                      Use wallet balance
                      <strong class="wallet-bal">🪙 ₹{{ walletBalance.toFixed(2) }} available</strong>
                    </span>
                  </label>
                </div>

                <!-- Price summary -->
                <div v-if="event.price > 0" class="price-summary">
                  <div class="price-row">
                    <span>Ticket Price</span>
                    <span>₹{{ event.price }}</span>
                  </div>
                  <div v-if="referralValid && discountAmount > 0" class="price-row price-row--discount">
                    <span>Referral Discount (5%)</span>
                    <span>− ₹{{ discountAmount.toFixed(2) }}</span>
                  </div>
                  <div v-if="regForm.use_wallet && walletBalance > 0" class="price-row price-row--wallet">
                    <span>Wallet Credit</span>
                    <span>− ₹{{ walletDeduction.toFixed(2) }}</span>
                  </div>
                  <div class="price-row price-row--total">
                    <span>You Pay</span>
                    <strong>₹{{ finalPrice.toFixed(2) }}</strong>
                  </div>
                </div>

                <button @click="submitRegistrationForm" class="btn-book w-full" :disabled="bookingInProgress">
                  {{ bookingInProgress ? 'Processing...' : finalPrice === 0 ? 'Register Free' : `Pay ₹${finalPrice.toFixed(2)}` }}
                </button>
              </div>

              <div v-else class="sold-out-panel text-center">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#ff007f" stroke-width="2.5" class="mx-auto mb-6"><circle cx="12" cy="12" r="10"></circle><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"></line></svg>
                <span class="sold-out-text">GATE CLOSED — SOLD OUT</span>
              </div>
            </template>
          </div>
        </div>
      </div>

      <div v-if="event" class="similar-events-corp mt-20 animate-corp delay-200">
        <h3 class="similar-heading">Similar Events You'll Love</h3>
        <RecommendationRow :eventId="event.id" title="" :limit="4" />
      </div>
    </div>

    <RazorpayCheckout
      v-if="showCheckout"
      :is-open="showCheckout"
      :order-data="orderData"
      :event-id="String(event.id)"
      @close="showCheckout = false"
      @success="handlePaymentSuccess"
      @error="handlePaymentError"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { eventApi, registrationApi, paymentApi } from '../services/api';
import api from '../services/api';
import RazorpayCheckout from '../components/payment/RazorpayCheckout.vue';
import RecommendationRow from '../components/RecommendationRow.vue';
import { useToast } from '../composables/useToast';

const route = useRoute();
const authStore = useAuthStore();
const toast = useToast();

const event = ref<any>(null);
const loading = ref(true);
const error = ref('');
const registrationStatus = ref<string | null>(null);
const currentRegistrationId = ref<number | null>(null);
let pollInterval: any;

const bookingInProgress = ref(false);
const showCheckout = ref(false);
const orderData = ref<any>(null);
const showCancelConfirm = ref(false);

const fetchEvent = async (isPolling = false) => {
  try {
    const res = await eventApi.getById(String(route.params.id));
    event.value = res.data;
    if (authStore.isAuthenticated && authStore.isUser) checkRegistrationStatus();
  } catch (err: any) {
    if (!isPolling) error.value = 'Event not found.';
  } finally {
    if (!isPolling) loading.value = false;
  }
};

const checkRegistrationStatus = async () => {
  try {
    const res = await registrationApi.getMy();
    const reg = res.data.find((r: any) => r.event_id === event.value.id);
    if (reg) { registrationStatus.value = reg.status; currentRegistrationId.value = reg.id; }
  } catch (e) { console.error('Failed to check reg status', e); }
};

const regForm = ref({
  role: 'athlete',
  role_details: { team: '', service: 'catering' },
  referral_code: '',
  use_wallet: false,
});

// Referral validation
const referralLoading = ref(false);
const referralValid   = ref(false);
const referralMsg     = ref('');
const discountAmount  = ref(0);
const walletBalance   = ref(0);

// Computed price breakdown
const walletDeduction = computed(() => {
  if (!regForm.value.use_wallet || !walletBalance.value) return 0;
  const afterDiscount = (event.value?.price ?? 0) - discountAmount.value;
  return Math.min(walletBalance.value, afterDiscount);
});

const finalPrice = computed(() => {
  const base = event.value?.price ?? 0;
  return Math.max(0, base - discountAmount.value - walletDeduction.value);
});

// Fetch wallet balance on mount
const fetchWallet = async () => {
  try {
    const res = await api.get('/wallet');
    walletBalance.value = res.data.wallet?.balance ?? 0;
  } catch { /* not logged in */ }
};

let validateTimer: any = null;
const debouncedValidate = () => {
  clearTimeout(validateTimer);
  validateTimer = setTimeout(validateReferral, 600);
};

const validateReferral = async () => {
  const code = regForm.value.referral_code.trim().toUpperCase();
  if (!code) { referralMsg.value = ''; referralValid.value = false; discountAmount.value = 0; return; }
  referralLoading.value = true;
  try {
    const res = await api.post('/registrations/validate-referral', {
      referral_code: code,
      price: event.value?.price ?? 0,
    });
    referralValid.value  = res.data.valid;
    referralMsg.value    = res.data.message;
    discountAmount.value = res.data.valid ? res.data.discount : 0;
  } catch { referralMsg.value = 'Validation failed.'; referralValid.value = false; }
  finally { referralLoading.value = false; }
};

const submitRegistrationForm = async () => {
  bookingInProgress.value = true;
  try {
    const regData: any = {
      event_id:      event.value.id,
      role:          regForm.value.role,
      role_details:  regForm.value.role_details,
      referral_code: regForm.value.referral_code.trim().toUpperCase() || undefined,
      use_wallet:    regForm.value.use_wallet,
    };
    await registrationApi.create(regData);
    // If nothing to pay (free event or wallet covers full amount), skip payment gateway
    if (finalPrice.value === 0) {
      toast.success('Registration successful! You\'re in.');
      bookingInProgress.value = false;
      await checkRegistrationStatus();
      fetchEvent();
      fetchWallet();
      return;
    }
    initiateBooking();
  } catch (err: any) {
    if (err.response?.data?.message === 'Already registered') {
      // Only retry payment if there's actually an amount to pay
      if (finalPrice.value > 0) {
        initiateBooking();
      } else {
        // Wallet covered the full amount but backend says already registered —
        // refresh status so the UI switches from the form to the confirmed view
        toast.info('You are already registered for this event.');
        bookingInProgress.value = false;
        await checkRegistrationStatus();
        fetchEvent();
        fetchWallet();
      }
    } else {
      toast.error(err.response?.data?.message || 'Failed to submit registration.');
      bookingInProgress.value = false;
    }
  }
};

const initiateBooking = async () => {
  bookingInProgress.value = true;
  try {
    const res = await paymentApi.createOrder({
      event_id:      event.value.id,
      referral_code: regForm.value.referral_code?.trim().toUpperCase() || '',
      wallet_used:   walletDeduction.value,
    });
    // Backend returns the discounted amount — use it in the checkout modal
    orderData.value = res.data;
    showCheckout.value = true;
  } catch (err: any) { toast.error(err.response?.data?.message || 'Failed to initiate booking.'); }
  finally { bookingInProgress.value = false; }
};

const handlePaymentSuccess = () => {
  showCheckout.value = false;
  registrationStatus.value = null;
  toast.success('Payment confirmed! 🎉 Your ticket is booked.');
  fetchEvent();
  fetchWallet();
};

const handlePaymentError = async (msg: string) => {
  showCheckout.value = false;
  // Notify backend: reset reg to payment_failed and refund wallet
  if (orderData.value?.order_id) {
    try {
      await paymentApi.failOrder({ order_id: orderData.value.order_id });
    } catch { /* best-effort */ }
  }
  registrationStatus.value = 'payment_failed';
  toast.error(msg + ' Any wallet amount used has been refunded.');
};

const cancelRegistration = async () => {
  showCancelConfirm.value = false;
  try {
    const res = await registrationApi.cancel(currentRegistrationId.value!);
    const msg = res.data?.message || 'Ticket cancelled.';
    registrationStatus.value = null;
    currentRegistrationId.value = null;
    toast.success(msg);
    fetchEvent();
    fetchWallet();
  } catch (err: any) { toast.error('Failed to cancel: ' + (err.response?.data?.message ?? 'Unknown error')); }
};

const retryPayment = async () => {
  bookingInProgress.value = true;
  try {
    initiateBooking();
  } finally {
    bookingInProgress.value = false;
  }
};

const resetAndRegisterAgain = () => {
  // Clear the failed registration status so the form re-appears
  registrationStatus.value = null;
  currentRegistrationId.value = null;
};

onMounted(() => { fetchEvent(); fetchWallet(); pollInterval = setInterval(() => fetchEvent(true), 30000); });
onUnmounted(() => { if (pollInterval) clearInterval(pollInterval); });
</script>

<style scoped>
/* ── Page ── */
.event-detail-page {
  padding-top: 7rem; /* fix: clears floating navbar */
  padding-bottom: 40px;
  min-height: 100vh;
  position: relative;
  background: var(--bg-site);
  color: var(--text-main);
}

[data-theme="light"] .event-detail-page {
  background: #e2e8f0;
}

/* ── Back button ── */
.back-btn-corp {
  background: none; border: none;
  color: var(--brand-accent);
  display: flex; align-items: center; gap: 0.75rem;
  font-weight: 900; cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  text-transform: uppercase; letter-spacing: 0.15em; font-size: 0.75rem;
}
.back-btn-corp:hover { color: var(--text-primary); transform: translateX(-10px); }

[data-theme="light"] .back-btn-corp { color: #0369a1; }

/* ── Loading ── */
.loading-corp-full {
  display: flex; flex-direction: column; align-items: center;
  gap: 1.5rem; padding: 100px 0; color: var(--brand-primary);
}

.pulse-loader {
  width: 48px; height: 48px;
  border: 4px solid var(--brand-primary);
  border-radius: 50%; animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%   { transform: scale(0.9); opacity: 0.5; }
  50%  { transform: scale(1.1); opacity: 1; }
  100% { transform: scale(0.9); opacity: 0.5; }
}

/* ── Error ── */
.error-panel {
  padding: 1rem 1.5rem;
  background: rgba(255,0,127,0.08); border: 1px solid rgba(255,0,127,0.2);
  color: #ff007f; border-radius: 14px; margin-bottom: 2rem;
}

/* ── Main detail card ── */
.detail-card {
  padding: 4rem;
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-radius: 24px;
  position: relative;
}

[data-theme="dark"] .detail-card {
  background: rgba(10,5,20,0.8);
  border-color: rgba(255,0,127,0.2);
}

[data-theme="light"] .detail-card {
  background: #ffffff;
  border: 2px solid #64748b;
  box-shadow: 0 0 0 1px #94a3b8, 0 8px 32px rgba(0,0,0,0.12);
}

.card-glow {
  position: absolute; top: 0; right: 0;
  width: 16rem; height: 16rem;
  background: var(--brand-glow);
  opacity: 0.08; filter: blur(80px);
  pointer-events: none; border-radius: 50%;
}

[data-theme="light"] .card-glow { opacity: 0.03; }

/* ── Header ── */
.header-corp {
  display: flex; justify-content: space-between;
  align-items: flex-start; gap: 2rem;
}

.sport-badge {
  display: inline-flex; align-items: center;
  padding: 0.35rem 1rem; border-radius: 9999px;
  background: rgba(255,0,127,0.1); border: 1px solid rgba(255,0,127,0.2);
  color: #ff007f;
  font-size: 0.68rem; font-weight: 900;
  text-transform: uppercase; letter-spacing: 0.1em;
}

[data-theme="light"] .sport-badge {
  background: rgba(255,0,127,0.08); color: #be185d;
}

.hero-title-large {
  font-size: 3.5rem; line-height: 0.95; margin-bottom: 0.5rem;
  font-weight: 900; letter-spacing: -0.04em;
  color: var(--text-primary);
}

@media (max-width: 1024px) { .hero-title-large { font-size: 2.5rem; } }

.tier-label {
  display: block; font-size: 0.62rem; font-weight: 900;
  letter-spacing: 0.2em; text-transform: uppercase;
  color: var(--brand-accent); margin-bottom: 0.4rem;
}

[data-theme="light"] .tier-label { color: #0369a1; }

.tier-value {
  display: block; font-size: 1.75rem; font-weight: 900;
  letter-spacing: -0.03em; color: var(--text-primary);
}

/* ── Info grid ── */
.info-grid-corp {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 3rem;
  border-bottom: 2px dashed var(--border-subtle);
  padding-bottom: 3rem;
}

@media (max-width: 1024px) { .info-grid-corp { grid-template-columns: 1fr; gap: 2rem; } }

[data-theme="light"] .info-grid-corp { border-bottom-color: #94a3b8; border-bottom-width: 2px; }

.info-label {
  display: block; font-size: 0.62rem; font-weight: 900;
  letter-spacing: 0.15em; text-transform: uppercase;
  color: var(--text-muted); margin-bottom: 0.6rem;
}

.info-value {
  font-size: 1.2rem; font-weight: 800; color: var(--text-primary);
}

/* ── Description ── */
.description-section {
  background: var(--bg-panel-light);
  padding: 2rem; border-radius: 1rem;
  border: 1px solid var(--border-subtle);
}

[data-theme="light"] .description-section {
  background: #e8edf5; border: 2px solid #64748b;
}

.desc-label {
  display: block; font-size: 0.62rem; font-weight: 900;
  letter-spacing: 0.2em; text-transform: uppercase;
  color: var(--brand-primary); margin-bottom: 0.75rem;
}

[data-theme="light"] .desc-label { color: #7c3aed; }

.desc-text {
  font-size: 1.05rem; color: var(--text-dim);
  line-height: 1.7; font-style: italic;
}

/* ── Registration panel ── */
.border-t-section {
  border-top: 1px solid var(--border-subtle);
  margin-top: 3rem;
}

[data-theme="light"] .border-t-section { border-top: 2px solid #94a3b8; }

.stats-grid-corp {
  display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;
}

@media (max-width: 1024px) { .stats-grid-corp { grid-template-columns: 1fr; } }

.stat-box-corp {
  padding: 1.5rem; border-radius: 1rem;
  background: var(--bg-panel-light);
  border: 1px solid var(--border-subtle);
  transition: all 0.25s ease;
  display: flex; flex-direction: column; gap: 0.5rem;
}

.stat-box-corp:hover {
  border-color: color-mix(in srgb, var(--brand-primary) 40%, transparent);
  transform: translateY(-2px);
}

[data-theme="light"] .stat-box-corp {
  background: #ffffff; border: 2px solid #64748b;
  box-shadow: 0 0 0 1px #94a3b8, 0 4px 12px rgba(0,0,0,0.08);
}

.stat-label {
  font-size: 0.62rem; font-weight: 900;
  letter-spacing: 0.15em; text-transform: uppercase;
}

.stat-label--pink { color: #ff007f; }
.stat-label--cyan { color: var(--brand-accent); }

[data-theme="light"] .stat-label--pink { color: #be185d; }
[data-theme="light"] .stat-label--cyan { color: #0369a1; }

.stat-value {
  font-size: 3rem; font-weight: 900;
  letter-spacing: -0.04em; color: var(--text-primary); line-height: 1;
}

.stat-sub { font-size: 1.1rem; color: var(--text-muted); margin-left: 0.4rem; }

/* ── Action portal ── */
.auth-prompt-corp {
  padding: 3rem; border-radius: 1.5rem;
  background: var(--bg-panel-light);
  border: 1px solid rgba(255,0,127,0.2);
}

[data-theme="light"] .auth-prompt-corp { background: #e8edf5; border: 2px solid #64748b; }

.auth-prompt-text { font-size: 1rem; color: var(--text-dim); margin-bottom: 1.5rem; }

.btn-book {
  display: inline-flex; align-items: center; justify-content: center;
  padding: 1rem 2.5rem; border-radius: 9999px; border: none;
  background: #ff007f; color: #000;
  font-weight: 900; font-size: 1rem; font-family: inherit;
  text-transform: uppercase; letter-spacing: 0.05em;
  cursor: pointer; text-decoration: none;
  transition: background 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease;
  width: 100%; margin-top: 0.5rem;
}

.btn-book:hover:not(:disabled) {
  background: #ffffff; color: #000;
  box-shadow: 0 0 40px rgba(255,0,127,0.35);
  transform: translateY(-1px);
}

.btn-book:disabled { opacity: 0.5; cursor: not-allowed; }

/* ── Status panel ── */
.status-panel-corp {
  background: rgba(0,243,255,0.08);
  border: 1px solid rgba(0,243,255,0.25);
  padding: 2rem; border-radius: 1.5rem;
  display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 1rem;
}

[data-theme="light"] .status-panel-corp {
  background: #dbeafe; border: 2px solid #64748b;
}

.status-text {
  font-size: 2rem; font-weight: 900;
  color: var(--text-primary); margin-top: 0.35rem; letter-spacing: -0.03em;
}

.btn-cancel-ticket {
  padding: 0.65rem 1.25rem; border-radius: 10px; cursor: pointer;
  border: 1px solid rgba(255,0,127,0.35);
  color: #ff007f; background: transparent;
  font-weight: 800; font-size: 0.82rem; font-family: inherit;
  transition: background 0.15s ease, color 0.15s ease;
}

.btn-cancel-ticket:hover { background: #ff007f; color: #000; }

/* ── Payment pending / failed status variants ── */
.status-panel-corp--pending {
  background: rgba(234,179,8,0.08);
  border-color: rgba(234,179,8,0.3);
}

.status-panel-corp--failed {
  background: rgba(255,0,127,0.06);
  border-color: rgba(255,0,127,0.25);
  flex-direction: column;
  align-items: flex-start;
}

.status-text--pending { color: #eab308; font-size: 1.5rem; }

.status-text--failed {
  font-size: 0.88rem;
  font-weight: 500;
  color: var(--text-dim);
  margin-top: 0.35rem;
  letter-spacing: 0;
  line-height: 1.5;
}

.btn-retry-payment {
  padding: 0.65rem 1.25rem; border-radius: 10px; cursor: pointer;
  border: 1px solid rgba(234,179,8,0.4);
  color: #eab308; background: transparent;
  font-weight: 800; font-size: 0.82rem; font-family: inherit;
  transition: background 0.15s ease, color 0.15s ease;
}
.btn-retry-payment:hover { background: #eab308; color: #000; }

/* ── Registration form ── */
.registration-form {
  background: var(--bg-panel-light);
  padding: 2rem; border-radius: 1.5rem;
  border: 1px solid var(--border-subtle);
}

[data-theme="light"] .registration-form {
  background: #e8edf5; border: 2px solid #64748b;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}

.reg-heading {
  font-size: 1.2rem; font-weight: 900;
  color: var(--text-primary); text-transform: uppercase;
  letter-spacing: -0.02em; margin-bottom: 1.5rem;
}

.reg-field-label {
  display: block; font-size: 0.62rem; font-weight: 900;
  letter-spacing: 0.15em; text-transform: uppercase;
  color: var(--brand-accent); margin-bottom: 0.5rem;
}

[data-theme="light"] .reg-field-label { color: #0369a1; }

.reg-input {
  width: 100%; padding: 0.85rem 1rem;
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-radius: 10px; color: var(--text-primary);
  font-size: 0.95rem; font-family: inherit; outline: none;
  appearance: none;
  transition: border-color 0.15s ease;
}

.reg-input:focus { border-color: var(--brand-accent); }
.reg-input::placeholder { color: var(--text-muted); }

[data-theme="dark"] .reg-input, [data-theme="dark"] .reg-input option { background: #1c1c1f; color: #f8fafc; }
[data-theme="light"] .reg-input, [data-theme="light"] .reg-input option { background: #ffffff; color: #0f172a; border-color: #cbd5e1; }

/* ── Sold out ── */
.sold-out-panel {
  background: var(--bg-panel-light); border: 1px solid var(--border-subtle);
  padding: 3rem; border-radius: 1.5rem;
}

[data-theme="light"] .sold-out-panel { background: #e8edf5; border: 2px solid #64748b; }

.sold-out-text {
  font-size: 1.5rem; font-weight: 900;
  color: var(--text-primary); text-transform: uppercase; letter-spacing: 0.05em;
}

/* ── Similar events ── */
.similar-heading {
  font-size: 0.65rem; font-weight: 900;
  letter-spacing: 0.2em; text-transform: uppercase;
  color: var(--brand-primary); margin-bottom: 2rem;
}

[data-theme="light"] .similar-heading { color: #7c3aed; }

@media (max-width: 1024px) {
  .detail-card { padding: 2rem; }
  .header-corp { flex-direction: column; }
}

/* ── Referral input row ── */
.ref-input-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.ref-input { flex: 1; min-width: 0; }

.ref-status {
  font-size: 0.75rem;
  font-weight: 700;
  white-space: nowrap;
  flex-shrink: 0;
}

.ref-status--ok      { color: #22c55e; }
.ref-status--err     { color: #f87171; }
.ref-status--loading { color: var(--text-muted); }

/* ── Wallet toggle ── */
.wallet-section {
  background: var(--bg-panel-light);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  padding: 0.75rem 1rem;
}

[data-theme="light"] .wallet-section { background: #f1f5f9; border-color: #cbd5e1; }

.wallet-toggle {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  cursor: pointer;
  user-select: none;
}

.wallet-checkbox {
  width: 16px; height: 16px;
  accent-color: var(--brand-accent);
  cursor: pointer;
}

.wallet-label { font-size: 0.85rem; font-weight: 600; color: var(--text-primary); }
.wallet-bal   { color: var(--brand-accent); font-size: 0.82rem; display: block; margin-top: 0.1rem; }
[data-theme="light"] .wallet-bal { color: #0369a1; }

/* ── Price summary ── */
.price-summary {
  background: var(--bg-panel-light);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

[data-theme="light"] .price-summary { background: #f8fafc; border-color: #cbd5e1; }

.price-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  color: var(--text-dim);
}

.price-row--discount { color: #22c55e; }
.price-row--wallet   { color: var(--brand-accent); }
[data-theme="light"] .price-row--wallet { color: #0369a1; }

.price-row--total {
  font-size: 0.95rem;
  font-weight: 800;
  color: var(--text-primary);
  padding-top: 0.45rem;
  border-top: 1px solid var(--border-subtle);
  margin-top: 0.1rem;
}

.mb-4 { margin-bottom: 1rem; }

/* ── Inline cancel confirmation ── */
.cancel-confirm-inline {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  background: rgba(255,0,127,0.06);
  border: 1px solid rgba(255,0,127,0.3);
  border-radius: 12px;
  padding: 1rem 1.25rem;
  max-width: 320px;
  animation: fade-in-up 0.18s ease;
}

@keyframes fade-in-up {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}

.cancel-confirm-text {
  font-size: 0.85rem;
  color: var(--text-dim);
  line-height: 1.5;
  font-weight: 600;
}

.cancel-confirm-actions {
  display: flex;
  gap: 0.6rem;
}

.btn-confirm-cancel {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  border: 1px solid rgba(255,0,127,0.5);
  background: #ff007f;
  color: #000;
  font-weight: 800;
  font-size: 0.8rem;
  font-family: inherit;
  transition: filter 0.15s ease;
}
.btn-confirm-cancel:hover { filter: brightness(1.1); }

.btn-keep-ticket {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  border: 1px solid var(--border-subtle);
  background: transparent;
  color: var(--text-dim);
  font-weight: 700;
  font-size: 0.8rem;
  font-family: inherit;
  transition: background 0.15s ease, color 0.15s ease;
}
.btn-keep-ticket:hover { background: var(--border-subtle); color: var(--text-primary); }

[data-theme="light"] .cancel-confirm-inline {
  background: #fff0f5;
  border-color: rgba(190,24,93,0.3);
}

</style>