<template>
  <div class="checkout-modal animate-corp" v-if="isOpen">
    <div class="luxury-bg-mesh">
      <div class="aura-blob aura-1"></div>
      <div class="aura-blob aura-2"></div>
    </div>
    
    <div class="card-premium checkout-card animate-corp">
      <div class="checkout-header mb-10">
        <div class="header-text">
          <span class="badge-corp">Secure Payment</span>
          <h3 class="hero-title-small mt-4">Complete Registration</h3>
        </div>
        <button class="close-btn-corp" @click="$emit('close')">&times;</button>
      </div>
      
      <div class="order-telemetry mb-10">
        <div class="meta-item-corp mb-4">
          <span class="label-muted">Order ID</span>
          <span class="value font-800">{{ orderData.order_id }}</span>
        </div>
        <div class="meta-item-corp">
          <span class="label-muted">Amount</span>
          <span class="value text-gradient font-950 text-3xl">₹{{ (orderData.amount / 100).toLocaleString() }}</span>
        </div>
      </div>

      <div class="simulation-panel p-8 border-luxury">
        <h4 class="label-muted mb-4">Powered by Razorpay</h4>
        <p class="text-dim text-sm mb-8">
          You will be redirected to a secure Razorpay payment page.
          Supports UPI, Cards, Net Banking, and Wallets.
        </p>
        
        <button 
          class="btn-corp btn-corp-primary w-full py-4" 
          @click="openRazorpay"
          :disabled="processing || !razorpayLoaded"
        >
          {{ processing ? 'Processing...' : !razorpayLoaded ? 'Loading...' : 'Pay Now' }}
        </button>
        
        <p v-if="errorMsg" class="text-red-400 text-sm mt-4 text-center">{{ errorMsg }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../../stores/auth';

const props = defineProps<{
  isOpen: boolean;
  orderData: {
    order_id: string;
    amount: number;
    key_id: string;
  };
  eventId: string;
}>();

const emit = defineEmits(['close', 'success', 'error']);
const authStore = useAuthStore();
const processing = ref(false);
const razorpayLoaded = ref(false);
const errorMsg = ref('');

// Dynamically load Razorpay checkout.js script
const loadRazorpayScript = (): Promise<void> => {
  return new Promise((resolve, reject) => {
    if ((window as any).Razorpay) {
      resolve(); // Already loaded
      return;
    }
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
  } catch (err) {
    errorMsg.value = 'Could not load payment SDK. Check your connection.';
  }
});

const openRazorpay = () => {
  errorMsg.value = '';
  
  const options = {
    key: props.orderData.key_id,          // Your rzp_test_... key from backend
    amount: props.orderData.amount,        // Amount in paise
    currency: 'INR',
    name: 'SyntaxError Events',
    description: 'Event Registration',
    order_id: props.orderData.order_id,    // Razorpay order_id from backend

    handler: async function (response: any) {
      // This fires after successful payment on Razorpay's side
      // Now verify signature on your backend
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

    theme: {
      color: '#0070f3',
    },

    modal: {
      ondismiss: () => {
        // User closed the Razorpay popup without paying
        emit('close');
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
.checkout-modal {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(12px);
}

.checkout-card {
  width: 100%;
  max-width: 500px;
  padding: 4rem;
  position: relative;
  z-index: 10;
}

.checkout-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.close-btn-corp {
  background: none;
  border: none;
  font-size: 2rem;
  color: var(--text-dim);
  cursor: pointer;
  line-height: 0.5;
  transition: color 0.3s;
}

.close-btn-corp:hover {
  color: white;
}

.order-telemetry {
  background: rgba(255, 255, 255, 0.02);
  padding: 2.5rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-subtle);
}

.meta-item-corp {
  display: flex;
  flex-direction: column;
}

.text-3xl { font-size: 2rem; }
.font-800 { font-weight: 800; }
.font-950 { font-weight: 950; }

.simulation-panel {
  background: rgba(0, 112, 243, 0.03);
  border-radius: var(--radius-md);
  text-align: center;
}

.border-luxury {
  border: 1px solid rgba(0, 112, 243, 0.1);
}

.hero-title-small {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.05em;
}

.text-red-400 { color: #f87171; }
</style>