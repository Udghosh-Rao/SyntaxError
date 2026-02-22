<template>
  <div class="checkout-modal animate-corp" v-if="isOpen">
    <div class="luxury-bg-mesh">
      <div class="aura-blob aura-1"></div>
      <div class="aura-blob aura-2"></div>
    </div>
    
    <div class="card-premium checkout-card animate-corp">
      <div class="checkout-header mb-10">
        <div class="header-text">
          <span class="badge-corp">Financial Interface</span>
          <h3 class="hero-title-small mt-4">Complete Commitment</h3>
        </div>
        <button class="close-btn-corp" @click="$emit('close')">&times;</button>
      </div>
      
      <div class="order-telemetry mb-10">
        <div class="meta-item-corp mb-4">
          <span class="label-muted">Mission ID</span>
          <span class="value font-800">{{ orderData.order_id }}</span>
        </div>
        <div class="meta-item-corp">
          <span class="label-muted">Aggregated Yield</span>
          <span class="value text-gradient font-950 text-3xl">₹{{ (orderData.amount / 100).toLocaleString() }}</span>
        </div>
      </div>

      <div class="simulation-panel p-8 border-luxury">
        <h4 class="label-muted mb-4">Architect Mode: Simulation Environment</h4>
        <p class="text-dim text-sm mb-8">This is a sandbox deployment. Authorize to simulate a successful throughput.</p>
        
        <button 
          class="btn-corp btn-corp-primary w-full py-4" 
          @click="simulateSuccess"
          :disabled="processing"
        >
          {{ processing ? 'Synchronizing...' : 'Authorize Commitment' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
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

const simulateSuccess = async () => {
  processing.value = true;
  try {
    const mockPayload = {
      razorpay_order_id: props.orderData.order_id,
      razorpay_payment_id: `pay_${Math.random().toString(36).substr(2, 9)}`,
      razorpay_signature: "test_signature"
    };

    const response = await axios.post(
      'http://localhost:8000/api/payments/verify', 
      mockPayload,
      { headers: { Authorization: `Bearer ${authStore.token}` } }
    );

    emit('success', response.data);
  } catch (err: any) {
    emit('error', err.response?.data?.message || 'Interface verification failed.');
  } finally {
    processing.value = false;
  }
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
</style>
