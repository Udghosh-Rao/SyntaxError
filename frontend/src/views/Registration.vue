<template>
  <div class="registration-form">
    <h1>Event Registration</h1>
    <div class="form-container">
      <form @submit.prevent="submitRegistration">
        <div class="form-group">
          <label for="firstName">First Name</label>
          <input v-model="form.firstName" type="text" id="firstName" required>
        </div>
        <div class="form-group">
          <label for="lastName">Last Name</label>
          <input v-model="form.lastName" type="text" id="lastName" required>
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input v-model="form.email" type="email" id="email" required>
        </div>
        <div class="form-group">
          <label for="phone">Phone Number</label>
          <input v-model="form.phone" type="tel" id="phone" required>
        </div>
        <div class="form-group">
          <label for="company">Company/Organization</label>
          <input v-model="form.company" type="text" id="company">
        </div>
        <div class="form-group">
          <label for="dietary">Dietary Preferences</label>
          <select v-model="form.dietary" id="dietary">
            <option value="">None</option>
            <option value="vegetarian">Vegetarian</option>
            <option value="vegan">Vegan</option>
            <option value="gluten-free">Gluten-Free</option>
          </select>
        </div>
        <div class="form-group checkbox">
          <input v-model="form.agreedToTerms" type="checkbox" id="terms">
          <label for="terms">I agree to the terms and conditions</label>
        </div>
        <button type="submit" class="btn-submit">Complete Registration</button>
      </form>
      <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const successMessage = ref('');
const errorMessage = ref('');

const form = ref({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  company: '',
  dietary: '',
  agreedToTerms: false
});

const submitRegistration = async () => {
  if (!form.value.agreedToTerms) {
    errorMessage.value = 'Please agree to the terms and conditions';
    return;
  }

  try {
    // API call would go here
    successMessage.value = 'Registration successful!';
    setTimeout(() => {
      router.push({ name: 'Home' });
    }, 2000);
  } catch (error) {
    errorMessage.value = 'Registration failed. Please try again.';
  }
};
</script>

<style scoped>
.registration-form {
  padding: 2rem;
  max-width: 600px;
  margin: 0 auto;
}

.form-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
}

.form-group.checkbox {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
}

.form-group.checkbox input {
  width: auto;
  margin-right: 0.5rem;
}

.form-group.checkbox label {
  margin: 0;
}

.btn-submit {
  width: 100%;
  padding: 0.75rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-submit:hover {
  background: #0056b3;
}

.success-message {
  margin-top: 1rem;
  padding: 1rem;
  background: #d4edda;
  color: #155724;
  border-radius: 4px;
}

.error-message {
  margin-top: 1rem;
  padding: 1rem;
  background: #f8d7da;
  color: #721c24;
  border-radius: 4px;
}
</style>
