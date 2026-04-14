<template>
  <div class="create-page">
    <div class="create-center">
      <div class="create-card">

        <!-- Header -->
        <div class="text-center mb-8">
          <h1 class="create-title">{{ isEdit ? 'Edit Event' : 'Create Event' }}</h1>
        </div>

        <div v-if="loadingEvent" class="loading-state">
          <div class="btn-spinner btn-spinner--lg"></div>
          <span class="loading-label">Loading event…</span>
        </div>

        <form v-else @submit.prevent="handleSubmit" class="create-form">

          <!-- Title -->
          <div class="field">
            <label class="field-label">Event Title *</label>
            <input v-model="form.title" type="text" class="field-input"
              placeholder="e.g. Summer Cricket League" required />
          </div>

          <!-- Description -->
          <div class="field">
            <label class="field-label">Description</label>
            <textarea v-model="form.description" class="field-input field-textarea"
              rows="3" placeholder="Rules, format, prizes…"></textarea>
          </div>

          <!-- Sport + Date -->
          <div class="field-row">
            <div class="field">
              <label class="field-label">Sport Category</label>
              <div class="select-wrap">
                <select v-model="form.sport_category" class="field-select">
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
              <label class="field-label">Date & Time *</label>
              <input v-model="form.event_date" type="datetime-local" class="field-input" required />
            </div>
          </div>

          <!-- City + Address -->
          <div class="field-row">
            <div class="field">
              <label class="field-label">City</label>
              <input v-model="form.venue_city" type="text" class="field-input"
                placeholder="e.g. Mumbai" />
            </div>
            <div class="field">
              <label class="field-label">Venue Address</label>
              <input v-model="form.venue_address" type="text" class="field-input"
                placeholder="Full address" />
            </div>
          </div>

          <!-- Capacity + Price -->
          <div class="field-row">
            <div class="field">
              <label class="field-label">Capacity *</label>
              <input v-model="form.capacity" type="number" min="1" class="field-input" required />
            </div>
            <div class="field">
              <label class="field-label">Entry Fee (₹) *</label>
              <input v-model="form.price" type="number" min="0" class="field-input"
                placeholder="0 for free" required />
            </div>
          </div>

          <!-- Banner URL + Organizer ID -->
          <div class="field-row">
            <div class="field">
              <label class="field-label">Banner URL</label>
              <input v-model="form.banner_url" type="text" class="field-input"
                placeholder="https://…" />
            </div>
            <div class="field">
              <label class="field-label">Organizer User ID</label>
              <input v-model="form.organizer_id" type="number" class="field-input"
                placeholder="Leave blank to assign to self" />
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
            <button v-if="isEdit" type="button" class="btn-delete"
              @click="handleDelete" :disabled="loading">
              Delete Event
            </button>
            <div class="form-actions-right">
              <button type="button" class="btn-cancel" @click="router.push('/admin')">
                Cancel
              </button>
              <button type="submit" class="btn-submit" :disabled="loading">
                <span v-if="loading" class="btn-spinner"></span>
                {{ loading ? (isEdit ? 'Saving…' : 'Creating…') : (isEdit ? 'Save Changes' : 'Create Event') }}
              </button>
            </div>
          </div>

        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { eventApi } from '../services/api';

const router  = useRouter();
const route   = useRoute();
const eventId = route.params.id as string | undefined;
const isEdit  = computed(() => !!eventId);

const loading      = ref(false);
const loadingEvent = ref(false);
const error        = ref('');

const form = ref({
  title: '',
  description: '',
  sport_category: 'Football',
  event_date: '',
  venue_city: '',
  venue_address: '',
  capacity: 100,
  price: 0,
  banner_url: '',
  organizer_id: '' as string | number,
});

onMounted(async () => {
  if (!isEdit.value) return;
  loadingEvent.value = true;
  try {
    const res = await eventApi.getById(eventId!);
    const e = res.data;
    form.value = {
      title:          e.title,
      description:    e.description || '',
      sport_category: e.sport_category,
      event_date:     e.event_date?.slice(0, 16) || '',
      venue_city:     e.venue_city || '',
      venue_address:  e.venue_address || '',
      capacity:       e.capacity,
      price:          e.price,
      banner_url:     e.banner_url || '',
      organizer_id:   e.organizer_id,
    };
  } catch {
    error.value = 'Failed to load event data.';
  } finally {
    loadingEvent.value = false;
  }
});

const handleSubmit = async () => {
  loading.value = true;
  error.value   = '';
  try {
    const payload: any = {
      ...form.value,
      event_date: new Date(form.value.event_date).toISOString(),
    };
    if (payload.organizer_id === '' || payload.organizer_id === null || payload.organizer_id === undefined) {
      delete payload.organizer_id;
    } else {
      payload.organizer_id = Number(payload.organizer_id);
    }
    if (isEdit.value) {
      await eventApi.update(eventId!, payload);
    } else {
      await eventApi.create(payload);
    }
    router.push('/admin');
  } catch (err: any) {
    error.value = err.response?.data?.message || 'Something went wrong.';
  } finally {
    loading.value = false;
  }
};

const handleDelete = async () => {
  if (!confirm(`Delete "${form.value.title}"? This cannot be undone.`)) return;
  loading.value = true;
  try {
    await eventApi.delete(eventId!);
    router.push('/admin');
  } catch (err: any) {
    error.value = err.response?.data?.message || 'Failed to delete event.';
    loading.value = false;
  }
};
</script>

<style scoped>
.create-page {
  min-height: 100vh;
  background: var(--bg-site);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 7rem 1rem 3rem;
}

.create-center {
  width: 100%;
  max-width: 680px;
}

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

.create-title {
  font-size: 1.75rem;
  font-weight: 900;
  letter-spacing: -0.04em;
  color: var(--text-primary);
}

/* Loading */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 3rem 0;
}

.loading-label {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--text-muted);
}

/* Form */
.create-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

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
  border-color: #7000ff;
  box-shadow: 0 0 0 3px rgba(112,0,255,0.1);
}

[data-theme="light"] .field-input { background: #f8fafc; border-color: #cbd5e1; }
[data-theme="light"] .field-input:focus { border-color: #7000ff; background: #ffffff; }

.field-textarea { resize: vertical; min-height: 90px; }

.field-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

@media (max-width: 560px) { .field-row { grid-template-columns: 1fr; } }

/* Select */
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
  border-color: #7000ff;
  box-shadow: 0 0 0 3px rgba(112,0,255,0.1);
}

[data-theme="dark"] .field-select,
[data-theme="dark"] .field-select option { background: #1c1c1f; color: #f8fafc; }

[data-theme="light"] .field-select,
[data-theme="light"] .field-select option { background: #f8fafc; color: #0f172a; border-color: #cbd5e1; }

[data-theme="light"] .field-select:focus { background: #ffffff; border-color: #7000ff; }

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
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
  padding-top: 1.25rem;
  border-top: 1px solid var(--border-subtle);
  margin-top: 0.5rem;
}

.form-actions-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-left: auto;
}

.btn-delete {
  padding: 0.75rem 1.5rem;
  border-radius: 9999px;
  border: 1px solid rgba(239, 68, 68, 0.35);
  background: rgba(239, 68, 68, 0.08);
  color: #ef4444;
  font-weight: 700;
  font-size: 0.88rem;
  font-family: inherit;
  cursor: pointer;
  transition: background 0.15s ease, border-color 0.15s ease;
}

.btn-delete:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.18);
  border-color: rgba(239, 68, 68, 0.6);
}

.btn-delete:disabled { opacity: 0.45; cursor: not-allowed; }

.btn-cancel {
  padding: 0.75rem 1.5rem;
  border-radius: 9999px;
  border: 1px solid var(--border-subtle);
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
  background: #7000ff; color: #fff;
  font-weight: 800; font-size: 0.9rem; font-family: inherit;
  cursor: pointer;
  transition: opacity 0.15s ease, transform 0.15s ease, box-shadow 0.15s ease;
}

.btn-submit:hover:not(:disabled) {
  opacity: 0.88; transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(112,0,255,0.3);
}

.btn-submit:disabled { opacity: 0.45; cursor: not-allowed; }

.btn-spinner {
  width: 14px; height: 14px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

.btn-spinner--lg {
  width: 32px; height: 32px;
  border-width: 3px;
  border-color: var(--border-subtle);
  border-top-color: #7000ff;
}

@keyframes spin { to { transform: rotate(360deg); } }
</style>