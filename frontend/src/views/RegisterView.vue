<template>
  <div class="register-page">
    <div class="register-center">
      <div class="register-card">

        <!-- Logo -->
        <router-link to="/" class="card-logo decoration-transparent">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
            :style="{ color: 'var(--brand-accent)' }"
            stroke="currentColor" stroke-width="3"
            stroke-linecap="round" stroke-linejoin="round">
            <path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>
          </svg>
          <span :style="{ color: 'var(--text-primary)' }">
            LIVE<span :style="{ color: 'var(--brand-accent)' }">SPORTS</span>
          </span>
        </router-link>

        <!-- Heading -->
        <h1 class="card-heading">Create account</h1>
        <p class="card-sub">Join the platform. Your game starts here.</p>

        <form @submit.prevent="handleRegister" class="register-form">

          <!-- Display Name -->
          <div class="field">
            <label class="field-label">Display Name</label>
            <input v-model="form.name" type="text" class="field-input"
              placeholder="Your name" autocomplete="name" required />
          </div>

          <!-- Email -->
          <div class="field">
            <label class="field-label">Email</label>
            <input v-model="form.email" type="email" class="field-input"
              placeholder="you@example.com" autocomplete="email" required />
          </div>

          <!-- Password -->
          <div class="field">
            <label class="field-label">Password</label>
            <div class="password-wrap">
              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                class="field-input"
                placeholder="••••••••"
                autocomplete="new-password"
                required
              />
              <button type="button" class="eye-btn"
                :title="showPassword ? 'Hide' : 'Show'"
                @click="showPassword = !showPassword">
                <svg v-if="!showPassword" width="16" height="16" viewBox="0 0 24 24"
                  fill="none" stroke="currentColor" stroke-width="2"
                  stroke-linecap="round" stroke-linejoin="round">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
                <svg v-else width="16" height="16" viewBox="0 0 24 24"
                  fill="none" stroke="currentColor" stroke-width="2"
                  stroke-linecap="round" stroke-linejoin="round">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/>
                  <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/>
                  <line x1="1" y1="1" x2="23" y2="23"/>
                </svg>
              </button>
            </div>
          </div>

          <!-- Your Role -->
          <div class="field">
            <label class="field-label">Your Role</label>
            <div class="select-wrap">
              <select v-model="form.role" class="field-select">
                <option value="user">Participating in Events</option>
                <option value="organizer">Hosting Events (Organizer)</option>
              </select>
              <svg class="select-chevron" width="15" height="15" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="2.5"
                stroke-linecap="round" stroke-linejoin="round">
                <polyline points="6 9 12 15 18 9"/>
              </svg>
            </div>
          </div>

          <!-- User Preferences Panel -->
          <div v-if="form.role === 'user'" class="prefs-panel">
            <p class="prefs-title">Local Scene</p>

            <div class="field">
              <label class="field-label">Home City</label>
              <input v-model="form.city" type="text" class="field-input"
                placeholder="e.g. Mumbai" />
            </div>

            <div class="field">
              <label class="field-label">Event Preference</label>
              <p class="field-hint">Select all that interest you</p>

              <div class="sport-grid">
                <button
                  v-for="sport in sportOptions" :key="sport.value"
                  type="button" class="sport-btn"
                  :class="{ 'sport-btn--on': form.preferred_sports.includes(sport.value) }"
                  :style="form.preferred_sports.includes(sport.value)
                    ? { background: 'var(--brand-accent)', color: '#000', borderColor: 'var(--brand-accent)' }
                    : { background: 'transparent', color: 'var(--text-primary)', borderColor: 'var(--border-bold)' }"
                  @click="toggleSport(sport.value)"
                >
                  <span>{{ sport.emoji }}</span>
                  {{ sport.label }}
                  <svg v-if="form.preferred_sports.includes(sport.value)"
                    width="12" height="12" viewBox="0 0 24 24"
                    fill="none" stroke="currentColor" stroke-width="3"
                    stroke-linecap="round" stroke-linejoin="round"
                    class="ml-auto flex-shrink-0">
                    <polyline points="20 6 9 17 4 12"/>
                  </svg>
                </button>

                <!-- Custom tag bubbles inline -->
                <span
                  v-for="(tag, i) in customTags" :key="tag"
                  class="sport-btn sport-btn--on custom-tag"
                  :style="{ background: 'var(--brand-accent)', borderColor: 'var(--brand-accent)', color: '#000' }"
                >
                  <span>🎯</span>
                  {{ tag }}
                  <button type="button" class="tag-remove"
                    @click="removeCustomTag(i)" aria-label="Remove">×</button>
                </span>
              </div>

              <p v-if="form.preferred_sports.length > 0" class="pref-count">
                ✓ {{ form.preferred_sports.length }}
                {{ form.preferred_sports.length === 1 ? 'preference' : 'preferences' }} selected
              </p>

              <!-- Others free-text -->
              <div v-if="othersSelected" class="others-row">
                <input
                  v-model="othersText" ref="othersInputRef"
                  type="text" class="field-input others-input"
                  placeholder="e.g. Tennis, Kabaddi…" maxlength="40"
                  @keydown.enter.prevent="addCustomTag"
                />
                <button
                  type="button" class="add-btn"
                  :disabled="!othersText.trim()"
                  :style="{
                    background: othersText.trim() ? 'var(--brand-accent)' : 'var(--border-subtle)',
                    color: othersText.trim() ? '#000' : 'var(--text-muted)',
                  }"
                  @click="addCustomTag"
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" stroke-width="3"
                    stroke-linecap="round" stroke-linejoin="round">
                    <line x1="12" y1="5" x2="12" y2="19"/>
                    <line x1="5" y1="12" x2="19" y2="12"/>
                  </svg>
                  Add
                </button>
              </div>
            </div>
          </div>

          <!-- Referral Code -->
          <div class="field">
            <label class="field-label">Referral Code <span class="field-optional">(optional)</span></label>
            <input
              v-model="form.referral_code"
              type="text"
              class="field-input"
              placeholder="Enter referral code if you have one"
              autocomplete="off"
            />
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
          <button type="submit" :disabled="loading" class="btn-primary">
            <span v-if="loading" class="btn-spinner"></span>
            {{ loading ? 'Creating account…' : 'Create Account' }}
          </button>

        </form>

        <p class="card-footer">
          Already have an account?
          <router-link to="/login" class="card-footer-link">Sign in</router-link>
        </p>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router       = useRouter();
const authStore    = useAuthStore();
const loading      = ref(false);
const error        = ref('');
const showPassword = ref(false);

const sportOptions = [
  { value: 'cricket',  label: 'Cricket',  emoji: '🏏' },
  { value: 'football', label: 'Football', emoji: '⚽' },
  { value: 'comedy',   label: 'Comedy',   emoji: '🎭' },
  { value: 'others',   label: 'Others',   emoji: '🎯' },
];

const form = ref({
  name: '',
  email: '',
  password: '',
  role: 'user',
  city: '',
  budget_preference: 'mid',
  preferred_sports: [] as string[],
  referral_code: '',
});


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

const handleRegister = async () => {
  loading.value = true;
  error.value   = '';
  try {
    const sportsPayload = form.value.preferred_sports.flatMap((s) => {
      if (s === 'others') {
        return customTags.value.length
          ? customTags.value.map((t) => `others:${t}`)
          : ['others'];
      }
      return [s];
    });
    await authStore.register({ ...form.value, preferred_sports: sportsPayload });
    if (authStore.isAdmin)          router.push('/admin');
    else if (authStore.isOrganizer) router.push('/organizer');
    else                            router.push('/home');
  } catch (err: any) {
    error.value = err.response?.data?.message || authStore.error || 'Registration failed. Please try again.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* ── Page ── */
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  background: var(--bg-site);
  padding: 6rem 1rem 3rem;
}

.register-center {
  width: 100%;
  max-width: 440px;
}

/* ── Card ── */
.register-card {
  background: var(--bg-panel-solid);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  padding: 2.5rem 2rem;
  box-shadow: 0 4px 32px rgba(0,0,0,0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.card-logo {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 1.05rem;
  font-weight: 900;
  letter-spacing: -0.03em;
  margin-bottom: 1.5rem;
}

.card-heading {
  font-size: 1.65rem;
  font-weight: 900;
  letter-spacing: -0.04em;
  color: var(--text-primary);
  margin-bottom: 0.3rem;
  text-align: center;
}

.card-sub {
  font-size: 0.82rem;
  color: var(--text-muted);
  margin-bottom: 1.75rem;
  text-align: center;
}

/* ── Form ── */
.register-form {
  width: 100%;
  display: flex;
  flex-direction: column;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin-bottom: 1rem;
}

.field-label {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  color: var(--text-dim);
}

.field-optional {
  font-weight: 500;
  text-transform: none;
  letter-spacing: 0;
  color: var(--text-muted);
  font-size: 0.68rem;
}

.field-hint {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-top: -0.1rem;
  margin-bottom: 0.4rem;
}

/* ── Inputs ── */
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

/* Password toggle */
.password-wrap { position: relative; }

.eye-btn {
  position: absolute;
  right: 0.8rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-muted);
  padding: 0.2rem;
  display: flex;
  align-items: center;
  transition: color 0.15s ease;
}

.eye-btn:hover { color: var(--text-primary); }

/* ── Selects — dark mode dropdown fix ── */
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
  /* Use explicit colours so browser-native dropdown list inherits them */
  background-color: var(--bg-panel-light);
  color: var(--text-primary);
}

/* Dark mode: force both the control and native dropdown list to be dark */
[data-theme="dark"] .field-select,
[data-theme="dark"] .field-select option {
  background-color: #1c1c1f;
  color: #f8fafc;
}

/* Light mode */
[data-theme="light"] .field-select,
[data-theme="light"] .field-select option {
  background-color: #ffffff;
  color: #0f172a;
}

.field-select:focus {
  border-color: var(--brand-accent);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--brand-accent) 10%, transparent);
}

.select-chevron {
  position: absolute;
  right: 0.85rem;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
  color: var(--text-muted);
}

/* ── Sub-vendor / prefs animations ── */
.subvendor-field,
.prefs-panel,
.others-row {
  animation: slideDown 0.2s ease forwards;
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-6px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── Prefs panel ── */
.prefs-panel {
  background: var(--bg-panel-light);
  border: 1px solid var(--border-subtle);
  border-radius: 14px;
  padding: 1.25rem;
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
}

.prefs-title {
  font-size: 0.68rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--brand-accent);
  margin-bottom: 1rem;
}

/* ── Sport grid ── */
.sport-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 0.55rem;
}

.sport-btn {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.6rem 0.85rem;
  border-radius: 10px;
  border: 1.5px solid;
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
  user-select: none;
  white-space: nowrap;
  font-family: inherit;
}

.sport-btn:hover     { transform: translateY(-2px); }
.sport-btn--on       { font-weight: 800; }

.pref-count {
  font-size: 0.75rem;
  color: var(--brand-accent);
  margin-top: 0.6rem;
}

.custom-tag {
  animation: popIn 0.18s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
  justify-content: space-between;
}

@keyframes popIn {
  from { opacity: 0; transform: scale(0.7); }
  to   { opacity: 1; transform: scale(1); }
}

.tag-remove {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
  padding: 0 0 0 0.2rem;
  color: rgba(0,0,0,0.5);
  margin-left: auto;
  flex-shrink: 0;
  transition: color 0.15s ease, transform 0.15s ease;
}

.tag-remove:hover { color: rgba(0,0,0,0.9); transform: scale(1.2); }

/* ── Others row ── */
.others-row {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  margin-top: 0.75rem;
}

.others-input { flex: 1; min-width: 0; }

.add-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.65rem 0.9rem;
  border-radius: 10px;
  border: none;
  font-size: 0.82rem;
  font-weight: 800;
  cursor: pointer;
  white-space: nowrap;
  flex-shrink: 0;
  font-family: inherit;
  transition: transform 0.15s ease, opacity 0.15s ease;
}

.add-btn:not(:disabled):hover { transform: translateY(-1px); }
.add-btn:disabled { cursor: not-allowed; opacity: 0.5; }

/* ── Error ── */
.error-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: #f87171;
  background: rgba(248,113,113,0.07);
  border: 1px solid rgba(248,113,113,0.18);
  border-radius: 8px;
  padding: 0.65rem 0.85rem;
  margin-bottom: 1rem;
}

/* ── Submit ── */
.btn-primary {
  width: 100%;
  padding: 0.8rem;
  background: var(--brand-accent);
  color: #000;
  font-weight: 800;
  font-size: 0.92rem;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
  font-family: inherit;
  transition: opacity 0.15s ease, transform 0.15s ease, box-shadow 0.15s ease;
}

.btn-primary:hover:not(:disabled) {
  opacity: 0.88;
  transform: translateY(-1px);
  box-shadow: 0 6px 20px color-mix(in srgb, var(--brand-accent) 25%, transparent);
}

.btn-primary:disabled { opacity: 0.45; cursor: not-allowed; }

.btn-spinner {
  width: 14px; height: 14px;
  border: 2px solid rgba(0,0,0,0.25);
  border-top-color: #000;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  flex-shrink: 0;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* ── Footer ── */
.card-footer {
  margin-top: 1.5rem;
  font-size: 0.8rem;
  color: var(--text-muted);
  text-align: center;
}

.card-footer-link {
  color: var(--brand-accent);
  font-weight: 700;
  text-decoration: none;
  margin-left: 0.25rem;
  transition: opacity 0.15s ease;
}

.card-footer-link:hover { opacity: 0.75; }

@media (max-width: 480px) {
  .register-card { padding: 1.75rem 1.25rem; }
  .sport-grid    { grid-template-columns: repeat(2, 1fr); }
}
</style>
