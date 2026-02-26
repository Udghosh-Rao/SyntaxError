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
      
      <div v-else-if="error" class="error-panel-inline bg-[#ff007f]/10 border-[#ff007f]/20 text-[#ff007f]">{{ error }}</div>
      
      <div v-else-if="event" class="card-premium detail-card-corp animate-corp relative overflow-hidden">
        <div class="absolute top-0 right-0 w-64 h-64 bg-[var(--brand-glow)] opacity-10 blur-[100px] pointer-events-none"></div>
        
        <div class="header-corp mb-12">
          <div class="header-main">
            <span class="badge-corp bg-[#ff007f]/10 text-[#ff007f] border-[#ff007f]/20">{{ event.sport_category }}</span>
            <h1 class="hero-title-large mt-6 text-white font-900 uppercase tracking-tighter">{{ event.title }}</h1>
          </div>
          <div class="tier-box-corp text-right">
             <span class="label-muted text-[10px] tracking-widest text-[#00f3ff]">ACCESS TIER</span>
             <span class="text-gradient font-900 text-3xl mt-2 block">{{ event.price_tier?.toUpperCase() }}</span>
          </div>
        </div>

        <div class="info-grid-corp mb-12">
          <div class="info-item">
            <label class="label-muted mb-3 text-[10px] tracking-widest text-white/40 uppercase font-800">Event Location</label>
            <p class="text-xl font-800 text-white">{{ event.venue_city }}{{ event.venue_address ? `, ${event.venue_address}` : '' }}</p>
          </div>
          <div class="info-item">
            <label class="label-muted mb-3 text-[10px] tracking-widest text-white/40 uppercase font-800">Event Date</label>
            <p class="text-xl font-800 text-white">{{ new Date(event.event_date).toLocaleDateString('en-GB', { day: '2-digit', month: 'long', year: 'numeric' }) }}</p>
          </div>
        </div>

        <div class="description-section mb-12 bg-white/5 p-8 rounded-2xl border border-white/5">
          <label class="label-muted mb-4 block text-[10px] tracking-widest text-[#ccff00] uppercase font-900">The Details</label>
          <p class="text-white/70 text-lg leading-relaxed max-w-4xl font-500 italic">"{{ event.description || 'No description provided for this event.' }}"</p>
        </div>

        <div class="registration-panel-corp pt-12 border-t border-white/10">
          <div class="stats-grid-corp mb-12">
            <div class="stat-box-corp p-6 bg-black/40 rounded-2xl border border-white/5">
              <span class="label-muted mb-4 text-[10px] tracking-widest text-[#ff007f] block font-900">TICKET PRICE</span>
              <span class="value text-5xl font-900 text-white">₹{{ event.price }}</span>
            </div>
            <div class="stat-box-corp p-6 bg-black/40 rounded-2xl border border-white/5">
              <span class="label-muted mb-4 text-[10px] tracking-widest text-[#00f3ff] block font-900">TIX REMAINING</span>
              <span class="value text-5xl font-900 text-white">{{ event.seats_remaining }}<span class="text-xl text-white/30 ml-2">/ {{ event.capacity }}</span></span>
            </div>
          </div>

          <div class="action-portal-corp">
            <template v-if="!authStore.isAuthenticated">
              <div class="auth-prompt-corp text-center p-12 bg-black/60 rounded-3xl border border-[#ff007f]/20">
                <p class="text-white/70 text-lg mb-8 font-600">You need to be logged in to book this event.</p>
                <router-link to="/login" class="btn-corp bg-[#ff007f] text-black px-12 py-4 font-900 uppercase tracking-widest hover:bg-white transition-all shadow-[0_0_30px_rgba(255,0,127,0.3)]">Login to Access</router-link>
              </div>
            </template>
            <template v-else-if="authStore.isUser">
              <div v-if="registrationStatus" class="status-panel-corp animate-corp bg-[#00f3ff]/10 border-[#00f3ff]/30 p-8 rounded-3xl flex justify-between items-center">
                <div class="status-info">
                   <label class="label-muted text-[10px] tracking-widest text-[#00f3ff] font-900">ENTRY STATUS</label>
                   <p class="status-text text-3xl text-white font-900 mt-2">{{ registrationStatus.toUpperCase() }}</p>
                </div>
                <button v-if="registrationStatus === 'confirmed'" @click="cancelRegistration" class="btn-corp-link-danger text-[#ff007f] font-900 uppercase tracking-widest border border-[#ff007f]/30 px-6 py-3 rounded-xl hover:bg-[#ff007f] hover:text-black transition-all">
                  Cancel Ticket
                </button>
              </div>
              
              <!-- UNIFIED REGISTRATION FORM -->
              <div v-else-if="event.seats_remaining > 0" class="registration-form mt-4 mb-8 text-left bg-black/40 p-8 rounded-3xl border border-white/5">
                <h4 class="mb-8 text-xl font-900 text-white uppercase tracking-tight">Booking Details</h4>
                <div class="input-stack mb-6">
                  <label class="label-muted text-[10px] tracking-widest text-[#00f3ff] mb-3 block font-900">SELECT YOUR ROLE</label>
                  <select v-model="regForm.role" class="input-corp w-full bg-black/80 border-white/10 focus:border-[#00f3ff] py-4">
                    <option value="athlete">Athlete / Fan</option>
                    <option value="sub_vendor">Service Provider / Referee / Medical</option>
                  </select>
                </div>
                
                <div v-if="regForm.role === 'athlete'" class="input-stack mb-6">
                  <label class="label-muted text-[10px] tracking-widest text-[#00f3ff] mb-3 block font-900">CREW / SQUAD NAME (OPTIONAL)</label>
                  <input type="text" v-model="regForm.role_details.team" class="input-corp w-full bg-black/80 border-white/10 focus:border-[#00f3ff] py-4" placeholder="e.g. Neon Riders" />
                </div>
                
                <div v-if="regForm.role === 'sub_vendor'" class="input-stack mb-6">
                  <label class="label-muted text-[10px] tracking-widest text-[#00f3ff] mb-3 block font-900">SERVICE TYPE</label>
                  <select v-model="regForm.role_details.service" class="input-corp w-full bg-black/80 border-white/10 focus:border-[#00f3ff] py-4">
                    <option value="catering">Drinks & Catering</option>
                    <option value="medical">Health & Safety</option>
                    <option value="logistics">Lighting / Audio Gear</option>
                  </select>
                </div>
                
                <button 
                  @click="submitRegistrationForm" 
                  class="btn-corp bg-[#ff007f] text-black w-full py-6 text-xl mt-8 font-900 uppercase tracking-tighter hover:bg-white hover:shadow-[0_0_40px_rgba(255,0,127,0.4)] transition-all"
                  :disabled="bookingInProgress"
                >
                  {{ bookingInProgress ? 'Processing Payment...' : 'Secure My Ticket' }}
                </button>
              </div>
              <div v-else class="sold-out-panel bg-white/5 border border-white/10 p-12 text-center rounded-3xl">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#ff007f" stroke-width="2.5" class="mx-auto mb-6"><circle cx="12" cy="12" r="10"></circle><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"></line></svg>
                <span class="text-2xl font-900 text-white uppercase tracking-widest">GATE CLOSED - SOLD OUT</span>
              </div>
            </template>
          </div>
        </div>
      </div>
      
      <div v-if="event" class="similar-events-corp mt-20 animate-corp delay-200">
        <h3 class="label-muted text-[10px] tracking-widest text-[#ccff00] mb-10 font-900 uppercase">Similar Events You'll Love</h3>
        <RecommendationRow 
          :eventId="event.id" 
          title="" 
          :limit="4" 
        />
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
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { eventApi, registrationApi, paymentApi } from '../services/api';
import RazorpayCheckout from '../components/payment/RazorpayCheckout.vue';
import RecommendationRow from '../components/RecommendationRow.vue';

const route = useRoute();
const authStore = useAuthStore();

const event = ref<any>(null);
const loading = ref(true);
const error = ref('');
const registrationStatus = ref<string | null>(null);
const currentRegistrationId = ref<number | null>(null);
let pollInterval: any;

const bookingInProgress = ref(false);
const showCheckout = ref(false);
const orderData = ref<any>(null);

const fetchEvent = async (isPolling = false) => {
  try {
    const res = await eventApi.getById(String(route.params.id));
    event.value = res.data;
    if (authStore.isAuthenticated && authStore.isUser) {
      checkRegistrationStatus();
    }
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
    if (reg) {
      registrationStatus.value = reg.status;
      currentRegistrationId.value = reg.id;
    }
  } catch (e) {
    console.error("Failed to check reg status", e);
  }
};

const regForm = ref({
  role: 'athlete',
  role_details: {
    team: '',
    service: 'catering'
  }
});

const submitRegistrationForm = async () => {
  bookingInProgress.value = true;
  try {
    await registrationApi.create({ 
      event_id: event.value.id,
      role: regForm.value.role,
      role_details: regForm.value.role_details
    });
    
    if (event.value.price === 0) {
      alert('Registration successful! (Free Event)');
      bookingInProgress.value = false;
      fetchEvent();
      return;
    }
    
    initiateBooking();
  } catch (err: any) {
    if (err.response?.data?.message === 'Already registered') {
       if (event.value.price > 0) {
          initiateBooking();
       } else {
         alert('You are already registered!');
         bookingInProgress.value = false;
       }
    } else {
      alert(err.response?.data?.message || 'Failed to submit registration');
      bookingInProgress.value = false;
    }
  }
};

const initiateBooking = async () => {
  bookingInProgress.value = true;
  try {
    const res = await paymentApi.createOrder({ event_id: event.value.id });
    orderData.value = res.data;
    showCheckout.value = true;
  } catch (err: any) {
    alert(err.response?.data?.message || 'Failed to initiate booking');
  } finally {
    bookingInProgress.value = false;
  }
};

const handlePaymentSuccess = () => {
  showCheckout.value = false;
  alert('Payment successful! Your ticket is confirmed.');
  fetchEvent();
};

const handlePaymentError = (msg: string) => {
  showCheckout.value = false;
  alert(msg);
};

const cancelRegistration = async () => {
  if (!confirm('Are you sure you want to cancel this ticket?')) return;
  try {
    await registrationApi.cancel(currentRegistrationId.value!);
    alert('Ticket cancelled.');
    fetchEvent();
  } catch (err: any) {
    alert('Failed to cancel: ' + err.response?.data?.message);
  }
};

onMounted(() => {
  fetchEvent();
  pollInterval = setInterval(() => {
    fetchEvent(true);
  }, 30000);
});

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval);
});
</script>

<style scoped>
.event-detail-page {
  padding: 80px 0 40px;
  min-height: 100vh;
  position: relative;
}

.back-btn-corp {
  background: none;
  border: none;
  color: #00f3ff;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 900;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  text-transform: uppercase;
  letter-spacing: 0.15em;
  font-size: 0.75rem;
}

.back-btn-corp:hover {
  color: white;
  transform: translateX(-10px);
}

.detail-card-corp {
  padding: 4rem;
  background: rgba(10, 5, 20, 0.8);
  border: 1px solid rgba(255, 0, 127, 0.2);
}

.hero-title-large {
  font-size: 3.5rem;
  line-height: 0.95;
  margin-bottom: 0.5rem;
}

.info-grid-corp {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  border-bottom: 2px dashed rgba(255, 255, 255, 0.05);
  padding-bottom: 3rem;
}

.registration-panel-corp {
  margin-top: 3rem;
}

.stat-box-corp {
  transition: all 0.3s ease;
}

.stat-box-corp:hover {
  border-color: rgba(204, 255, 0, 0.3);
  transform: translateY(-2px);
}

.loading-corp-full {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  padding: 100px 0;
  color: #ccff00;
}

.pulse-loader {
  width: 48px;
  height: 48px;
  border: 4px solid #ccff00;
  border-radius: 50%;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { transform: scale(0.9); opacity: 0.5; }
  50% { transform: scale(1.1); opacity: 1; box-shadow: 0 0 20px #ccff00; }
  100% { transform: scale(0.9); opacity: 0.5; }
}

@media (max-width: 1024px) {
  .detail-card-corp { padding: 2rem; }
  .hero-title-large { font-size: 2.5rem; }
  .info-grid-corp, .stats-grid-corp { grid-template-columns: 1fr; gap: 2rem; }
}
</style>
