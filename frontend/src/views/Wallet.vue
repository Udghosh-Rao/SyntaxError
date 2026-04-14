<template>
  <div class="wallet-page min-h-screen pt-28 pb-16 px-4 md:px-8">
    <div class="max-w-2xl mx-auto space-y-8">
      
      <section class="glass-panel p-10 rounded-3xl text-center space-y-4">
        <h1 class="text-3xl font-black tracking-tight text-white">Your Wallet</h1>
        <p class="text-gray-400">Manage your seamless event registrations</p>
        
        <div class="balance-display my-8 p-8 rounded-2xl bg-black/40 border border-gray-800">
          <p class="text-sm uppercase tracking-widest text-gray-500 font-bold mb-2">Current Balance</p>
          <div class="text-6xl font-black headline-gradient">
            <span class="text-3xl mr-2">🪙</span>{{ walletBalance.toFixed(2) }}
          </div>
        </div>

        <div class="add-funds-widget pt-4">
          <label class="block text-sm font-semibold text-gray-300 mb-3 text-left">Top Up Amount (₹)</label>
          <div class="flex items-center gap-4">
            <input 
              v-model.number="topUpAmount" 
              type="number" 
              min="1" 
              class="custom-input flex-1 text-2xl font-bold"
              placeholder="e.g. 500"
            />
            <button 
              @click="initiateAddFunds" 
              class="save-btn whitespace-nowrap"
              :disabled="isProcessing || topUpAmount <= 0"
            >
              {{ isProcessing ? 'Processing...' : 'Add Funds' }}
            </button>
          </div>
          <p v-if="errorMsg" class="text-red-400 text-sm mt-4 text-left">{{ errorMsg }}</p>
        </div>
      </section>
      
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '../stores/auth';
import axios from 'axios';

const authStore = useAuthStore();
const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const topUpAmount = ref(0);
const isProcessing = ref(false);
const errorMsg = ref('');

const walletBalance = computed(() => {
  return authStore.userObj?.wallet_balance || 0;
});

// Load Razorpay Script
const loadRazorpayScript = (): Promise<void> => {
  return new Promise((resolve, reject) => {
    if ((window as any).Razorpay) {
      resolve();
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
  await loadRazorpayScript();
  if (authStore.isAuthenticated) {
    await authStore.fetchProfile();
  }
});

const initiateAddFunds = async () => {
  if (topUpAmount.value <= 0) return;
  errorMsg.value = '';
  isProcessing.value = true;

  try {
    // 1. Create order on backend
    const res = await axios.post(`${apiBase}/api/wallet/add-funds`, 
      { amount: topUpAmount.value },
      { headers: { Authorization: `Bearer ${authStore.token}` } }
    );
    
    const orderData = res.data;

    // 2. Open Razorpay Checkout
    const options = {
      key: orderData.key_id,
      amount: orderData.amount, // in paise
      currency: orderData.currency,
      name: 'SyntaxError Wallet',
      description: 'Wallet Top Up',
      order_id: orderData.order_id,
      handler: async function (response: any) {
        // 3. Verify on UI
        try {
          const verifyRes = await axios.post(`${apiBase}/api/wallet/verify-funds`,
            {
              razorpay_order_id: response.razorpay_order_id,
              razorpay_payment_id: response.razorpay_payment_id,
              razorpay_signature: response.razorpay_signature,
              amount: topUpAmount.value
            },
            { headers: { Authorization: `Bearer ${authStore.token}` } }
          );
          
          if (authStore.userObj) {
            authStore.userObj.wallet_balance = verifyRes.data.wallet_balance;
          }
          topUpAmount.value = 0;
          alert('Funds added successfully!');
        } catch (err: any) {
          errorMsg.value = err.response?.data?.message || 'Verification failed';
        } finally {
          isProcessing.value = false;
        }
      },
      prefill: {
        name: authStore.userObj?.name || '',
        email: authStore.userObj?.email || '',
      },
      theme: { color: '#00f3ff' },
      modal: {
        ondismiss: () => {
          isProcessing.value = false;
        }
      }
    };

    const rzp = new (window as any).Razorpay(options);
    rzp.on('payment.failed', (response: any) => {
      errorMsg.value = response.error?.description || 'Payment failed.';
      isProcessing.value = false;
    });
    rzp.open();

  } catch (err: any) {
    errorMsg.value = err.response?.data?.message || 'Could not initiate top up';
    isProcessing.value = false;
  }
};
</script>

<style scoped>
.glass-panel {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
}
[data-theme="light"] .glass-panel {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
}

.headline-gradient {
  background: linear-gradient(135deg, #fff 0%, #a1a1aa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
[data-theme="light"] .headline-gradient {
  background: linear-gradient(135deg, #000 0%, #4b5563 100%);
}

.custom-input {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  outline: none;
  transition: all 0.2s ease;
}
.custom-input:focus {
  border-color: var(--brand-accent);
  box-shadow: 0 0 0 2px rgba(0, 243, 255, 0.15);
}
[data-theme="light"] .custom-input {
  background: #f8fafc;
  border-color: #e2e8f0;
  color: #000;
}

.save-btn {
  background: var(--brand-accent);
  color: #000;
  font-weight: 800;
  padding: 1.1rem 2rem;
  border-radius: 12px;
  transition: all 0.2s ease;
}
.save-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 243, 255, 0.3);
}
.save-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>
