<template>
  <div class="create-page">
    <div class="create-center">
      <div class="create-card">

        <!-- Header -->
        <div class="text-center mb-8">
          <h1 class="create-title">Create Event</h1>
        </div>

        <form @submit.prevent="handleSubmit" class="create-form">

          <!-- Title -->
          <div class="field">
            <label class="field-label">Event Title</label>
            <input v-model="form.title" type="text" class="field-input"
              placeholder="e.g. Summer Cricket League" required />
          </div>

          <!-- Description -->
          <div class="field">
            <label class="field-label">Description</label>
            <textarea v-model="form.description" class="field-input field-textarea"
              rows="3" placeholder="Rules, format, prizes…"></textarea>
          </div>

          <!-- Date + Price -->
          <div class="field-row">
            <div class="field">
              <label class="field-label">Date & Time</label>
              <input v-model="form.date" type="datetime-local" class="field-input" required />
            </div>
            <div class="field">
              <label class="field-label">Entry Fee (₹)</label>
              <input v-model="form.price" type="number" min="0" class="field-input"
                placeholder="0 for free" required />
            </div>
          </div>

          <!-- City + Address -->
          <div class="field-row">
            <div class="field">
              <label class="field-label">City</label>
              <input v-model="form.venue_city" type="text" class="field-input"
                placeholder="e.g. Mumbai" required />
            </div>
            <div class="field">
              <label class="field-label">Venue Address</label>
              <input v-model="form.venue_address" type="text" class="field-input"
                placeholder="Full address" />
            </div>
          </div>

          <!-- Category + Capacity -->
          <div class="field-row">
            <div class="field">
              <label class="field-label">Sport Category</label>
              <div class="select-wrap">
                <select v-model="form.category" class="field-select" required>
                  <option value="Football">Football</option>
                  <option value="Basketball">Basketball</option>
                  <option value="Tennis">Tennis</option>
                  <option value="Cricket">Cricket</option>
                  <option value="Swimming">Swimming</option>
                  <option value="Other">Other</option>
                </select>
                <svg class="select-chev" width="14" height="14" viewBox="0 0 24 24"
                  fill="none" stroke="currentColor" stroke-width="2.5"
                  stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="6 9 12 15 18 9"/>
                </svg>
              </div>
            </div>
            <div class="field">
              <label class="field-label">Max Participants</label>
              <input v-model="form.max_participants" type="number" min="1"
                class="field-input" required />
            </div>
          </div>

          <!-- Sub-Vendor -->
          <div class="field">
            <label class="field-label">Select Sub-Vendor</label>
            <div class="select-wrap">
              <select v-model="form.sub_vendor" class="field-select">
                <option value="">— No sub-vendor —</option>
                <option value="equipment_supplier">Equipment Supplier</option>
                <option value="catering">Catering</option>
                <option value="photography">Photography</option>
                <option value="security">Security</option>
              </select>
              <svg class="select-chev" width="14" height="14" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="2.5"
                stroke-linecap="round" stroke-linejoin="round">
                <polyline points="6 9 12 15 18 9"/>
              </svg>
            </div>
          </div>

          <!-- Error -->
          <div v-if="error" class="error-row">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2.5"
              stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            {{ error }}
          </div>

          <!-- Actions -->
          <div class="form-actions">
            <button type="button" class="btn-cancel" @click="router.push('/organizer')">
              Cancel
            </button>
            <button type="submit" class="btn-submit" :disabled="loading">
              <span v-if="loading" class="btn-spinner"></span>
              {{ loading ? 'Creating…' : 'Create Event' }}
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

const router      = useRouter();
const eventsStore = useEventsStore();
const loading     = ref(false);
const error       = ref('');

const form = ref({
  title: '',
  description: '',
  date: '',
  venue_city: '',
  venue_address: '',
  category: 'Football',
  max_participants: 100,
  price: 0,
  sub_vendor: '',
});

const handleSubmit = async () => {
  loading.value = true;
  error.value   = '';
  try {
    await eventsStore.createEvent({
      title:        form.value.title,
      description:  form.value.description,
      sport_category: form.value.category,
      venue_city:   form.value.venue_city,
      venue_address: form.value.venue_address,
      event_date:   new Date(form.value.date).toISOString(),
      capacity:     form.value.max_participants,
      price:        form.value.price,
      sub_vendor:   form.value.sub_vendor,
      tags: [],
    });
    router.push('/organizer');
  } catch {
    error.value = eventsStore.error || 'Failed to create event.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* ── Page ── */
.create-page {
  min-height: 100vh;
  background: var(--bg-site);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 7rem 1rem 3rem; /* top clears floating navbar */
}

.create-center {
  width: 100%;
  max-width: 680px;
}

/* ── Card ── */
.create-card {
  background: var(--bg-panel-solid);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  padding: 2.5rem 2rem;
  box-shadow: 0 4px 32px rgba(0,0,0,0.08);
}

[data-theme="light"] .create-card {
  background: #ffffff;
  border-color: #94a3b8;
  box-shadow: 0 4px 24px rgba(0,0,0,0.09);
}

/* ── Header ── */
.create-badge {
  display: inline-block;
  font-size: 0.65rem;
  font-weight: 900;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  padding: 0.35rem 0.85rem;
  border-radius: 9999px;
  border: 1px solid var(--border-subtle);
  background: var(--bg-panel);
  color: var(--text-dim);
}

.create-title {
  font-size: 1.75rem;
  font-weight: 900;
  letter-spacing: -0.04em;
  color: var(--text-primary);
}

.create-sub {
  font-size: 0.83rem;
  color: var(--text-muted);
}

/* ── Form ── */
.create-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Fields */
.field {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.field-label {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  color: var(--text-dim);
}

.field-input {
  width: 100%;
  padding: 0.72rem 0.95rem;
  background: var(--bg-panel-light);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  color: var(--text-primary);
  font-size: 0.9rem;
  font-family: inherit;
  outline: none;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.field-input::placeholder { color: var(--text-muted); }

.field-input:focus {
  border-color: var(--brand-accent);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--brand-accent) 10%, transparent);
}

[data-theme="light"] .field-input { background: #f8fafc; border-color: #cbd5e1; }
[data-theme="light"] .field-input:focus { border-color: var(--brand-accent); background: #ffffff; }

.field-textarea { resize: vertical; min-height: 90px; }

/* Two-column row */
.field-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

@media (max-width: 560px) { .field-row { grid-template-columns: 1fr; } }

/* Selects */
.select-wrap { position: relative; }

.field-select {
  width: 100%;
  padding: 0.72rem 2.5rem 0.72rem 0.95rem;
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  font-size: 0.9rem;
  font-family: inherit;
  outline: none;
  appearance: none;
  cursor: pointer;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
  background: var(--bg-panel-light);
  color: var(--text-primary);
}

.field-select:focus {
  border-color: var(--brand-accent);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--brand-accent) 10%, transparent);
}

[data-theme="dark"] .field-select,
[data-theme="dark"] .field-select option { background: #1c1c1f; color: #f8fafc; }

[data-theme="light"] .field-select,
[data-theme="light"] .field-select option { background: #f8fafc; color: #0f172a; border-color: #cbd5e1; }

[data-theme="light"] .field-select:focus { background: #ffffff; border-color: var(--brand-accent); }

.select-chev {
  position: absolute; right: 0.8rem; top: 50%;
  transform: translateY(-50%);
  pointer-events: none; color: var(--text-muted);
}

/* Error */
.error-row {
  display: flex; align-items: center; gap: 0.5rem;
  font-size: 0.8rem; color: #f87171;
  background: rgba(248,113,113,0.07);
  border: 1px solid rgba(248,113,113,0.18);
  border-radius: 8px; padding: 0.65rem 0.85rem;
}

/* Actions */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding-top: 1.25rem;
  border-top: 1px solid var(--border-subtle);
  margin-top: 0.5rem;
}

.btn-cancel {
  padding: 0.75rem 1.5rem;
  border-radius: 9999px;
  border: 1px solid var(--border-premium);
  background: transparent;
  color: var(--text-dim);
  font-weight: 700;
  font-size: 0.88rem;
  font-family: inherit;
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease;
}

.btn-cancel:hover { background: var(--bg-panel-light); color: var(--text-primary); }

.btn-submit {
  display: inline-flex; align-items: center; gap: 0.5rem;
  padding: 0.75rem 1.75rem;
  border-radius: 9999px; border: none;
  background: var(--brand-accent); color: #000;
  font-weight: 800; font-size: 0.9rem; font-family: inherit;
  cursor: pointer;
  transition: opacity 0.15s ease, transform 0.15s ease, box-shadow 0.15s ease;
}

.btn-submit:hover:not(:disabled) {
  opacity: 0.88; transform: translateY(-1px);
  box-shadow: 0 6px 20px color-mix(in srgb, var(--brand-accent) 25%, transparent);
}

.btn-submit:disabled { opacity: 0.45; cursor: not-allowed; }

.btn-spinner {
  width: 14px; height: 14px;
  border: 2px solid rgba(0,0,0,0.25);
  border-top-color: #000;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }
</style>