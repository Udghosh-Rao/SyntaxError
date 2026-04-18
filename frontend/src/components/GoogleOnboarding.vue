<template>
  <div class="onboarding-overlay">
    <div class="onboarding-card">

      <!-- Header -->
      <div class="ob-header">
        <div class="ob-avatar">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2.5"
            stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
            <circle cx="12" cy="7" r="4"/>
          </svg>
        </div>
        <div>
          <h2 class="ob-title">One last step</h2>
          <p class="ob-sub">Welcome, <strong>{{ name }}</strong>! Tell us a bit about yourself.</p>
        </div>
      </div>

      <form @submit.prevent="handleSubmit" class="ob-form">

        <!-- Role -->
        <div class="field">
          <label class="field-label">I want to</label>
          <div class="role-options">
            <button
              type="button"
              class="role-btn"
              :class="{ 'role-btn--active': form.role === 'user' }"
              @click="form.role = 'user'"
            >
              <span class="role-icon">🎟️</span>
              <span class="role-name">Attend Events</span>
              <span class="role-desc">Browse and register for sports events</span>
            </button>
            <button
              type="button"
              class="role-btn"
              :class="{ 'role-btn--active': form.role === 'organizer' }"
              @click="form.role = 'organizer'"
            >
              <span class="role-icon">🏟️</span>
              <span class="role-name">Host Events</span>
              <span class="role-desc">Create and manage your own events</span>
            </button>
          </div>
        </div>

        <!-- City -->
        <div class="field">
          <label class="field-label">Your City</label>
          <input
            v-model="form.city"
            type="text"
            class="field-input"
            placeholder="e.g. Mumbai"
          />
        </div>

        <!-- Sport preferences — users only -->
        <div v-if="form.role === 'user'" class="field prefs-field">
          <label class="field-label">Event Preferences <span class="optional">(optional)</span></label>
          <p class="field-hint">Select all that interest you</p>

          <div class="sport-grid">
            <button
              v-for="sport in sportOptions"
              :key="sport.value"
              type="button"
              class="sport-btn"
              :class="{ 'sport-btn--on': form.preferred_sports.includes(sport.value) }"
              :style="form.preferred_sports.includes(sport.value)
                ? { background: 'var(--brand-accent)', color: '#000', borderColor: 'var(--brand-accent)' }
                : { background: 'transparent', color: 'var(--text-primary)', borderColor: 'var(--border-bold)' }"
              @click="toggleSport(sport.value)"
            >
              <span>{{ sport.emoji }}</span>
              {{ sport.label }}
              <svg v-if="form.preferred_sports.includes(sport.value)"
                width="11" height="11" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="3"
                stroke-linecap="round" stroke-linejoin="round"
                class="ml-auto flex-shrink-0">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
            </button>

            <!-- Custom tag bubbles -->
            <span
              v-for="(tag, i) in customTags"
              :key="tag"
              class="sport-btn sport-btn--on custom-tag"
              :style="{ background: 'var(--brand-accent)', borderColor: 'var(--brand-accent)', color: '#000' }"
            >
              {{ tag }}
              <button type="button" class="tag-remove" @click="removeCustomTag(i)">×</button>
            </span>
          </div>

          <p v-if="form.preferred_sports.length" class="pref-count">
            ✓ {{ form.preferred_sports.length }}
            {{ form.preferred_sports.length === 1 ? 'preference' : 'preferences' }} selected
          </p>

          <!-- Others free-text -->
          <div v-if="othersSelected" class="others-row">
            <input
              v-model="othersText"
              ref="othersInputRef"
              type="text"
              class="field-input others-input"
              placeholder="e.g. Tennis, Kabaddi…"
              maxlength="40"
              @keydown.enter.prevent="addCustomTag"
            />
            <button
              type="button"
              class="add-btn"
              :disabled="!othersText.trim()"
              :style="{
                background: othersText.trim() ? 'var(--brand-accent)' : 'var(--border-subtle)',
                color: othersText.trim() ? '#000' : 'var(--text-muted)',
              }"
              @click="addCustomTag"
            >
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="3"
                stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"/>
                <line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
              Add
            </button>
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

        <!-- Submit -->
        <button type="submit" class="btn-primary" :disabled="loading">
          <span v-if="loading" class="btn-spinner"></span>
          {{ loading ? 'Setting up…' : 'Get Started' }}
          <svg v-if="!loading" width="15" height="15" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2.5"
            stroke-linecap="round" stroke-linejoin="round">
            <line x1="5" y1="12" x2="19" y2="12"/>
            <polyline points="12 5 19 12 12 19"/>
          </svg>
        </button>

      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const props = defineProps<{
  name:      string;
  tempToken: string;
  userId:    number;
}>();

const router    = useRouter();
const authStore = useAuthStore();
const loading   = ref(false);
const error     = ref('');

const form = ref({
  role:             'user',
  city:             '',
  preferred_sports: [] as string[],
  budget_preference: 'mid',
});

// ── Sport options ──────────────────────────────────────────────────────────
const sportOptions = [
  { value: 'cricket',  label: 'Cricket',  emoji: '🏏' },
  { value: 'football', label: 'Football', emoji: '⚽' },
  { value: 'comedy',   label: 'Comedy',   emoji: '🎭' },
  { value: 'others',   label: 'Others',   emoji: '' },
];

const othersText     = ref('');
const othersInputRef = ref<HTMLInputElement | null>(null);
const customTags     = ref<string[]>([]);
const othersSelected = computed(() => form.value.preferred_sports.includes('others'));

const toggleSport = (value: string) => {
  const idx = form.value.preferred_sports.indexOf(value);
  if (idx === -1) {
    form.value.preferred_sports.push(value);
  } else {
    form.value.preferred_sports.splice(idx, 1);
    if (value === 'others') { othersText.value = ''; customTags.value = []; }
  }
};

const addCustomTag = async () => {
  const tag = othersText.value.trim();
  if (!tag) return;
  if (!customTags.value.includes(tag)) customTags.value.push(tag);
  othersText.value = '';
  await nextTick();
  othersInputRef.value?.focus();
};

const removeCustomTag = (i: number) => customTags.value.splice(i, 1);

// ── Submit ──────────────────────────────────────────────────────────────────
const handleSubmit = async () => {
  loading.value = true;
  error.value   = '';

  try {
    const sportsPayload = form.value.preferred_sports.flatMap(s => {
      if (s === 'others') {
        return customTags.value.length
          ? customTags.value.map(t => t)
          : ['others'];
      }
      return [s];
    });

    const res = await axios.post(
      '/api/auth/oauth/google/complete',
      { ...form.value, preferred_sports: sportsPayload },
      { headers: { Authorization: `Bearer ${props.tempToken}` } }
    );

    // Save to auth store + localStorage
    authStore.token  = res.data.access_token;
    authStore.role   = res.data.role;
    authStore.userId = res.data.user_id;
    localStorage.setItem('auth_token', res.data.access_token);
    localStorage.setItem('user_role',  res.data.role);
    localStorage.setItem('user_id',    String(res.data.user_id));
    await authStore.fetchProfile();

    // Redirect based on role
    if (res.data.role === 'organizer') router.push('/organizer');
    else router.push('/home');

  } catch (err: any) {
    error.value = err.response?.data?.message || 'Setup failed. Please try again.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* ── Overlay ── */
.onboarding-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  z-index: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

/* ── Card ── */
.onboarding-card {
  background: var(--bg-panel-solid);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  padding: 2.25rem 2rem;
  width: 100%;
  max-width: 480px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.4);
  scrollbar-width: none;
}

.onboarding-card::-webkit-scrollbar { display: none; }

[data-theme="light"] .onboarding-card {
  background: #ffffff;
  border-color: #94a3b8;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.15);
}

/* ── Header ── */
.ob-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.75rem;
}

.ob-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: color-mix(in srgb, var(--brand-accent) 15%, transparent);
  border: 1px solid color-mix(in srgb, var(--brand-accent) 25%, transparent);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--brand-accent);
  flex-shrink: 0;
}

.ob-title {
  font-size: 1.3rem;
  font-weight: 900;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  margin-bottom: 0.2rem;
}

.ob-sub {
  font-size: 0.82rem;
  color: var(--text-muted);
}

.ob-sub strong { color: var(--text-primary); font-weight: 700; }

/* ── Form ── */
.ob-form { display: flex; flex-direction: column; gap: 1.1rem; }

.field { display: flex; flex-direction: column; gap: 0.4rem; }

.field-label {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  color: var(--text-dim);
}

.optional { font-weight: 500; text-transform: none; letter-spacing: 0; color: var(--text-muted); }

.field-hint { font-size: 0.75rem; color: var(--text-muted); margin-top: -0.1rem; }

.field-input {
  width: 100%;
  padding: 0.7rem 0.9rem;
  background: var(--bg-panel-light);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  color: var(--text-primary);
  font-size: 0.9rem;
  font-family: inherit;
  outline: none;
  transition: border-color 0.15s ease;
}

.field-input::placeholder { color: var(--text-muted); }
.field-input:focus { border-color: var(--brand-accent); }

[data-theme="light"] .field-input { background: #f8fafc; border-color: #cbd5e1; }

/* ── Role buttons ── */
.role-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.role-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.3rem;
  padding: 1.1rem 0.75rem;
  border-radius: 12px;
  border: 1.5px solid var(--border-subtle);
  background: var(--bg-panel-light);
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.15s ease;
  font-family: inherit;
}

.role-btn:hover { border-color: var(--border-premium); }

.role-btn--active {
  border-color: var(--brand-accent) !important;
  background: color-mix(in srgb, var(--brand-accent) 10%, transparent) !important;
}

.role-icon { font-size: 1.6rem; line-height: 1; }

.role-name {
  font-size: 0.88rem;
  font-weight: 800;
  color: var(--text-primary);
}

.role-desc {
  font-size: 0.72rem;
  color: var(--text-muted);
  line-height: 1.4;
}

/* ── Sport grid ── */
.prefs-field { margin-top: 0.25rem; }

.sport-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 0.55rem;
  margin-top: 0.5rem;
}

.sport-btn {
  display: flex; align-items: center; gap: 0.4rem;
  padding: 0.6rem 0.85rem;
  border-radius: 10px; border: 1.5px solid;
  font-size: 0.82rem; font-weight: 700;
  cursor: pointer; transition: all 0.15s ease;
  user-select: none; white-space: nowrap; font-family: inherit;
}

.sport-btn:hover { transform: translateY(-1px); }
.sport-btn--on   { font-weight: 800; }

.pref-count { font-size: 0.75rem; color: var(--brand-accent); margin-top: 0.5rem; }

.custom-tag { justify-content: space-between; }

.tag-remove {
  background: none; border: none; cursor: pointer;
  font-size: 1rem; line-height: 1; padding: 0 0 0 0.2rem;
  color: rgba(0,0,0,0.5); margin-left: auto; flex-shrink: 0;
  transition: color 0.15s ease;
}

.tag-remove:hover { color: rgba(0,0,0,0.9); }

/* ── Others row ── */
.others-row {
  display: flex; gap: 0.5rem; align-items: center; margin-top: 0.6rem;
}

.others-input { flex: 1; min-width: 0; }

.add-btn {
  display: inline-flex; align-items: center; gap: 0.3rem;
  padding: 0.65rem 0.9rem; border-radius: 10px; border: none;
  font-size: 0.82rem; font-weight: 800; cursor: pointer;
  white-space: nowrap; flex-shrink: 0; font-family: inherit;
  transition: transform 0.15s ease, opacity 0.15s ease;
}

.add-btn:not(:disabled):hover { transform: translateY(-1px); }
.add-btn:disabled { cursor: not-allowed; opacity: 0.5; }

/* ── Error ── */
.error-row {
  display: flex; align-items: center; gap: 0.5rem;
  font-size: 0.8rem; color: #f87171;
  background: rgba(248,113,113,0.07);
  border: 1px solid rgba(248,113,113,0.18);
  border-radius: 8px; padding: 0.65rem 0.85rem;
}

/* ── Submit ── */
.btn-primary {
  width: 100%; margin-top: 0.25rem;
  display: inline-flex; align-items: center; justify-content: center; gap: 0.5rem;
  padding: 0.82rem 1.5rem;
  background: var(--brand-accent); color: #000;
  font-weight: 800; font-size: 0.92rem; font-family: inherit;
  border: none; border-radius: 10px; cursor: pointer;
  transition: opacity 0.15s ease, transform 0.15s ease, box-shadow 0.15s ease;
}

.btn-primary:hover:not(:disabled) {
  opacity: 0.88; transform: translateY(-1px);
  box-shadow: 0 6px 20px color-mix(in srgb, var(--brand-accent) 25%, transparent);
}

.btn-primary:disabled { opacity: 0.45; cursor: not-allowed; }

.btn-spinner {
  width: 14px; height: 14px;
  border: 2px solid rgba(0,0,0,0.25); border-top-color: #000;
  border-radius: 50%; animation: spin 0.6s linear infinite; flex-shrink: 0;
}

@keyframes spin { to { transform: rotate(360deg); } }
</style>