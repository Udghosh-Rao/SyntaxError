<template>
  <div class="create-event-page">
    <div class="luxury-bg-mesh">
      <div class="aura-blob aura-1"></div>
      <div class="aura-blob aura-2"></div>
      <div class="aura-blob aura-3"></div>
    </div>

    <div class="container py-12">
      <div class="card-premium form-container animate-corp">
        <div class="section-header text-center mb-10">
          <span class="badge-corp">Strategic Deployment</span>
          <h1 class="hero-title-small mt-4">Create New Event</h1>
          <p class="text-dim mt-2">Set up your next tournament and start accepting registrations.</p>
        </div>

        <form @submit.prevent="handleSubmit" class="event-form">
          <div class="input-stack">
            <label class="label-muted">Event Designation (Title)</label>
            <input v-model="form.title" type="text" class="input-corp" placeholder="e.g., Summer Corporate League" required />
          </div>
          
          <div class="input-stack">
            <label class="label-muted">Strategic Briefing (Description)</label>
            <textarea v-model="form.description" class="input-corp" rows="4" placeholder="Details about rules, format, prizes..."></textarea>
          </div>
          
          <div class="grid-2-col">
            <div class="input-stack">
              <label class="label-muted">Temporal Window (Date & Time)</label>
              <input v-model="form.date" type="datetime-local" class="input-corp" required />
            </div>
            <div class="input-stack">
              <label class="label-muted">Commitment Fee (INR)</label>
              <input v-model="form.price" type="number" min="0" class="input-corp" placeholder="0 for free" required />
            </div>
          </div>
          
          <div class="grid-2-col">
            <div class="input-stack">
              <label class="label-muted">Venue Bio-Region (City)</label>
              <input v-model="form.venue_city" type="text" class="input-corp" placeholder="e.g., Mumbai" required />
            </div>
            <div class="input-stack">
              <label class="label-muted">Specific Coordinates (Address)</label>
              <input v-model="form.venue_address" type="text" class="input-corp" placeholder="Full address" />
            </div>
          </div>
          
          <div class="grid-2-col">
            <div class="input-stack">
              <label class="label-muted">Sport Category</label>
              <select v-model="form.category" class="input-corp" required>
                <option value="Football">Football</option>
                <option value="Basketball">Basketball</option>
                <option value="Tennis">Tennis</option>
                <option value="Cricket">Cricket</option>
                <option value="Swimming">Swimming</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div class="input-stack">
              <label class="label-muted">Sector Capacity (Max Participants)</label>
              <input v-model="form.max_participants" type="number" min="1" class="input-corp" required />
            </div>
          </div>

          <div v-if="error" class="error-panel-inline mb-8 animate-corp">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
            <span>{{ error }}</span>
          </div>
          
          <div class="actions mt-10">
            <button type="button" class="btn-corp btn-corp-outline px-10" @click="router.push('/organizer')">Abort</button>
            <button type="submit" class="btn-corp btn-corp-primary px-10" :disabled="loading">
              {{ loading ? 'Deploying...' : 'Deploy Event' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useEventsStore } from '@/stores/events';

const router = useRouter();
const eventsStore = useEventsStore();

const loading = ref(false);
const error = ref('');

const form = ref({
  title: '',
  description: '',
  date: '',
  venue_city: '',
  venue_address: '',
  category: 'Football',
  max_participants: 100,
  price: 0
});

const handleSubmit = async () => {
  loading.value = true;
  error.value = '';
  
  try {
    const payload = {
      title: form.value.title,
      description: form.value.description,
      sport_category: form.value.category,
      venue_city: form.value.venue_city,
      venue_address: form.value.venue_address,
      event_date: new Date(form.value.date).toISOString(),
      capacity: form.value.max_participants,
      price: form.value.price,
      tags: []
    };
    
    await eventsStore.createEvent(payload);
    router.push('/organizer');
  } catch (err: any) {
    error.value = eventsStore.error || 'Failed to create event';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.create-event-page {
  min-height: 100vh;
  position: relative;
  display: flex;
  align-items: center;
}

.form-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 4rem;
}

.hero-title-small {
  font-size: 2.5rem;
  font-weight: 800;
  letter-spacing: -0.05em;
  line-height: 1.1;
}

.grid-2-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.error-panel-inline {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #ff5555;
  font-size: 0.85rem;
  padding: 1rem;
  background: rgba(255, 85, 85, 0.05);
  border: 1px solid rgba(255, 85, 85, 0.1);
  border-radius: var(--radius-sm);
}

.actions {
  display: flex;
  gap: 1.5rem;
  justify-content: flex-end;
  padding-top: 2rem;
  border-top: 1px solid var(--border-subtle);
}

@media (max-width: 768px) {
  .form-container {
    padding: 2.5rem;
  }
  .grid-2-col {
    grid-template-columns: 1fr;
    gap: 0;
  }
}
</style>
