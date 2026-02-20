<template>
  <div class="payment-page">
    <h1>Event Payment</h1>
    <div class="payment-container">
      <div class="order-summary">
        <h2>Order Summary</h2>
        <div class="summary-item">
          <span>Event: {{ event.title }}</span>
          <span>₹{{ event.registrationFee }}</span>
        </div>
        <div class="summary-item">
          <span>Quantity: {{ quantity }}</span>
          <span>₹{{ event.registrationFee * quantity }}</span>
        </div>
        <div class="summary-total">
          <span>Total Amount</span>
          <span>₹{{ totalAmount }}</span>
        </div>
      </div>
      <div class="payment-methods">
        <h2>Payment Method</h2>
        <div class="method-selector">
          <label>
            <input v-model="paymentMethod" type="radio" value="razorpay" checked>
            Razorpay (Credit/Debit Card, UPI, etc.)
          </label>
          <label>
            <input v-model="paymentMethod" type="radio" value="netbanking">
            Net Banking
          </label>
          <label>
            <input v-model="paymentMethod" type="radio" value="wallet">
            Digital Wallet
          </label>
        </div>
      </div>
      <div class="promo-section">
        <input v-model="promoCode" type="text" placeholder="Enter promo code (optional)" class="promo-input">
        <button @click="applyPromo" class="btn-apply">Apply</button>
      </div>
      <div v-if="discount > 0" class="discount-info">
        <p>Discount: -₹{{ discount }}</p>
        <p class="final-amount">Final Amount: ₹{{ finalAmount }}</p>
      </div>
      <button @click="processPayment" class="btn-pay">Pay ₹{{ finalAmount }}</button>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const event = ref<any>({
  title: 'Sample Event',
  registrationFee: 500
});
const quantity = ref(1);
const paymentMethod = ref('razorpay');
const promoCode = ref('');
const discount = ref(0);
const errorMessage = ref('');
const successMessage = ref('');

const totalAmount = computed(() => event.value.registrationFee * quantity.value);
const finalAmount = computed(() => totalAmount.value - discount.value);

const applyPromo = async () => {
  // Validate promo code
  if (promoCode.value === 'SAVE10') {
    discount.value = totalAmount.value * 0.1;
    errorMessage.value = '';
  } else if (promoCode.value === 'SAVE20') {
    discount.value = totalAmount.value * 0.2;
    errorMessage.value = '';
  } else if (promoCode.value) {
    errorMessage.value = 'Invalid promo code';
    discount.value = 0;
  }
};

const processPayment = async () => {
  try {
    // Razorpay integration would go here
    successMessage.value = 'Payment processing...';
    setTimeout(() => {
      router.push({ name: 'Home' });
    }, 2000);
  } catch (error) {
    errorMessage.value = 'Payment failed. Please try again.';
  }
};
</script>

<style scoped>
.payment-page {
  padding: 2rem;
  max-width: 600px;
  margin: 0 auto;
}

.payment-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.order-summary {
  background: #f9f9f9;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 2rem;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #eee;
}

.summary-total {
  display: flex;
  justify-content: space-between;
  padding: 1rem 0;
  margin-top: 1rem;
  font-weight: bold;
  font-size: 1.1rem;
  border-top: 2px solid #ddd;
}

.payment-methods {
  margin-bottom: 2rem;
}

.method-selector label {
  display: block;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.method-selector label:hover {
  background: #f5f5f5;
}

.method-selector input {
  margin-right: 0.5rem;
}

.promo-section {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.promo-input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.btn-apply {
  padding: 0.75rem 1.5rem;
  background: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.discount-info {
  background: #d4edda;
  color: #155724;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.final-amount {
  font-size: 1.2rem;
  font-weight: bold;
  margin: 0.5rem 0 0 0;
}

.btn-pay {
  width: 100%;
  padding: 1rem;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-pay:hover {
  background: #218838;
}

.error-message {
  margin-top: 1rem;
  padding: 1rem;
  background: #f8d7da;
  color: #721c24;
  border-radius: 4px;
}

.success-message {
  margin-top: 1rem;
  padding: 1rem;
  background: #d4edda;
  color: #155724;
  border-radius: 4px;
}
</style>
