<template>
  <div class="profile-page">
    <div class="party-bg-mesh">
      <div class="aura-blob aura-1"></div>
      <div class="aura-blob aura-2"></div>
    </div>

    <div class="container py-16 relative z-10">
      <!-- Header -->
      <div class="page-header mb-12 animate-corp">
        <span class="badge-corp">Account Settings</span>
        <h1 class="page-title mt-3">Your <span class="text-gradient">Profile</span></h1>
        <p class="page-sub mt-2">Manage your personal information and avatar.</p>
      </div>

      <div class="profile-grid">
        <!-- Avatar Card -->
        <div class="dash-card avatar-card animate-corp">
          <div class="avatar-preview" @click="triggerFileInput">
            <img v-if="avatarPreview" :src="avatarPreview" alt="Avatar" class="avatar-img" />
            <span v-else class="avatar-initial">{{ nameInitial }}</span>
            <div class="avatar-overlay">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
              <span>Upload Photo</span>
            </div>
          </div>
          <input ref="fileInput" type="file" accept="image/*" class="hidden-input" @change="handleAvatarUpload" />
          <p class="avatar-hint">Click to upload. Max 2 MB. Square recommended.</p>

          <!-- Referral Code (users only) -->
          <div v-if="!authStore.isOrganizer" class="referral-box mt-8">
            <label class="field-label">YOUR REFERRAL CODE</label>
            <div class="referral-code-row">
              <span class="referral-code-text">{{ form.referral_code }}</span>
              <button class="copy-btn" @click="copyReferral" :class="{ 'copy-btn--copied': copied }">
                {{ copied ? '✓ Copied' : 'Copy' }}
              </button>
            </div>
            <p class="referral-hint">Share this code to earn 5% wallet credit when friends register for events!</p>
          </div>
        </div>

        <!-- Edit Form Card -->
        <div class="dash-card form-card animate-corp delay-100">
          <h2 class="section-title mb-8">Personal Information</h2>

          <div v-if="successMsg" class="success-banner mb-6">{{ successMsg }}</div>
          <div v-if="errorMsg" class="error-banner mb-6">{{ errorMsg }}</div>

          <div class="field-group">
            <label class="field-label" for="pf-name">FULL NAME</label>
            <input id="pf-name" v-model="form.name" type="text" class="field-input" placeholder="Your full name" />
          </div>

          <div class="field-group">
            <label class="field-label" for="pf-email">EMAIL</label>
            <input id="pf-email" :value="form.email" type="email" class="field-input field-input--readonly" readonly />
          </div>

          <div class="field-group">
            <label class="field-label" for="pf-city">CITY</label>
            <input id="pf-city" v-model="form.city" type="text" class="field-input" placeholder="e.g. Mumbai" />
          </div>

          <div class="field-group">
            <label class="field-label" for="pf-budget">BUDGET PREFERENCE</label>
            <div class="select-wrap">
              <select id="pf-budget" v-model="form.budget_preference" class="field-input field-select">
                <option value="low">Low (Under ₹500)</option>
                <option value="mid">Mid (₹500 – ₹2000)</option>
                <option value="high">High (₹2000+)</option>
              </select>
              <svg class="select-chev" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="6 9 12 15 18 9"/>
              </svg>
            </div>
          </div>

          <div class="field-group">
            <label class="field-label">PREFERRED SPORTS</label>
            <div class="sports-grid">
              <label v-for="sport in availableSports" :key="sport" class="sport-checkbox">
                <input type="checkbox" :value="sport" v-model="form.preferred_sports" />
                <span class="sport-chip" :class="{ 'sport-chip--on': form.preferred_sports.includes(sport) }">
                  {{ sport }}
                </span>
              </label>
            </div>
          </div>

          <button class="save-btn" @click="saveProfile" :disabled="saving">
            <span v-if="saving" class="btn-spinner"></span>
            {{ saving ? 'Saving...' : 'Save Changes' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '../stores/auth';
import { userApi } from '../services/api';

const authStore = useAuthStore();

const form = ref({
  name: '',
  email: '',
  city: '',
  budget_preference: 'mid',
  preferred_sports: [] as string[],
  referral_code: '',
});

const avatarPreview = ref<string | null>(null);
const fileInput = ref<HTMLInputElement | null>(null);
const saving = ref(false);
const copied = ref(false);
const successMsg = ref('');
const errorMsg = ref('');

const nameInitial = computed(() => (form.value.name || '?')[0].toUpperCase());

const availableSports = [
  'Football', 'Cricket', 'Basketball', 'Tennis', 'Badminton',
  'Running', 'Cycling', 'Swimming', 'Chess', 'eSports'
];

onMounted(async () => {
  await authStore.fetchProfile();
  const user = authStore.userObj;
  if (user) {
    form.value.name = user.name || '';
    form.value.email = user.email || '';
    form.value.city = user.city || '';
    form.value.budget_preference = user.budget_preference || 'mid';
    form.value.preferred_sports = user.preferred_sports || [];
    form.value.referral_code = user.referral_code || '';
    avatarPreview.value = user.avatar_url || null;
  }
});

const triggerFileInput = () => fileInput.value?.click();

const handleAvatarUpload = (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0];
  if (!file) return;
  if (file.size > 2 * 1024 * 1024) {
    errorMsg.value = 'Image too large. Max 2 MB.';
    return;
  }
  const reader = new FileReader();
  reader.onload = (ev) => {
    avatarPreview.value = ev.target?.result as string;
  };
  reader.readAsDataURL(file);
};

const saveProfile = async () => {
  saving.value = true;
  successMsg.value = '';
  errorMsg.value = '';
  try {
    const payload: any = {
      name: form.value.name,
      city: form.value.city,
      budget_preference: form.value.budget_preference,
      preferred_sports: form.value.preferred_sports,
    };
    if (avatarPreview.value && avatarPreview.value.startsWith('data:')) {
      payload.avatar_url = avatarPreview.value;
    }
    await userApi.updateProfile(payload);
    await authStore.fetchProfile();
    successMsg.value = 'Profile updated successfully!';
  } catch (err: any) {
    errorMsg.value = err.response?.data?.message || 'Failed to save profile.';
  } finally {
    saving.value = false;
  }
};

const copyReferral = async () => {
  try {
    await navigator.clipboard.writeText(form.value.referral_code);
    copied.value = true;
    setTimeout(() => { copied.value = false; }, 2000);
  } catch {
    copied.value = false;
  }
};
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: var(--bg-site);
  color: var(--text-main);
  padding-top: 6rem;
  padding-bottom: 4rem;
  position: relative;
}

/* ── Header ── */
.page-header { }
.badge-corp {
  display: inline-block;
  font-size: 0.65rem; font-weight: 900;
  letter-spacing: 0.15em; text-transform: uppercase;
  padding: 0.35rem 0.85rem; border-radius: 9999px;
  border: 1px solid var(--border-subtle);
  background: var(--bg-panel); color: var(--text-dim);
}
.page-title {
  font-size: clamp(1.8rem, 4vw, 2.8rem);
  font-weight: 900; letter-spacing: -0.04em;
  color: var(--text-primary); line-height: 1.1;
}
.text-gradient {
  background: linear-gradient(135deg, var(--brand-primary), var(--brand-accent));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.page-sub { font-size: 0.9rem; color: var(--text-dim); }

/* ── Grid ── */
.profile-grid {
  display: grid;
  grid-template-columns: 340px 1fr;
  gap: 1.5rem;
}
@media (max-width: 900px) { .profile-grid { grid-template-columns: 1fr; } }

/* ── Cards ── */
.dash-card {
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-radius: 1.25rem;
  padding: 2rem;
  transition: background 0.25s ease, border-color 0.25s ease;
}
[data-theme="light"] .dash-card {
  background: #ffffff; border: 2px solid #94a3b8;
  box-shadow: 0 4px 16px rgba(0,0,0,0.07);
}

/* ── Avatar ── */
.avatar-card { display: flex; flex-direction: column; align-items: center; }

.avatar-preview {
  position: relative; width: 140px; height: 140px;
  border-radius: 50%; cursor: pointer; overflow: hidden;
  border: 3px solid var(--brand-accent);
  background: var(--bg-panel-light);
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 1rem;
  transition: border-color 0.2s ease;
}
.avatar-preview:hover .avatar-overlay { opacity: 1; }

.avatar-img { width: 100%; height: 100%; object-fit: cover; }

.avatar-initial {
  font-size: 3rem; font-weight: 900;
  color: var(--brand-accent);
}

.avatar-overlay {
  position: absolute; inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 0.4rem; opacity: 0;
  transition: opacity 0.2s ease;
  font-size: 0.75rem; font-weight: 700;
  color: #fff; text-transform: uppercase; letter-spacing: 0.05em;
}

.hidden-input { display: none; }

.avatar-hint {
  font-size: 0.72rem; color: var(--text-muted);
  text-align: center; max-width: 200px;
}

/* ── Referral box ── */
.referral-box {
  width: 100%;
  padding: 1.25rem; border-radius: 1rem;
  background: color-mix(in srgb, var(--brand-accent) 6%, transparent);
  border: 1px solid color-mix(in srgb, var(--brand-accent) 20%, transparent);
}
[data-theme="light"] .referral-box {
  background: #e0f2fe; border-color: #7dd3fc;
}

.referral-code-row {
  display: flex; align-items: center; justify-content: space-between;
  gap: 0.75rem; margin-top: 0.5rem; margin-bottom: 0.5rem;
}

.referral-code-text {
  font-size: 1.1rem; font-weight: 900;
  letter-spacing: 0.08em; color: var(--brand-accent);
  font-family: monospace;
}
[data-theme="light"] .referral-code-text { color: #0369a1; }

.copy-btn {
  padding: 0.35rem 0.85rem; border-radius: 9999px;
  font-size: 0.72rem; font-weight: 800;
  background: var(--brand-accent); color: #000;
  border: none; cursor: pointer;
  transition: background 0.15s ease, transform 0.15s ease;
}
.copy-btn:hover { opacity: 0.85; transform: scale(1.04); }
.copy-btn--copied { background: #00dfd8; }

.referral-hint {
  font-size: 0.72rem; color: var(--text-muted); line-height: 1.5;
}

/* ── Form ── */
.section-title {
  font-size: 0.7rem; font-weight: 900;
  text-transform: uppercase; letter-spacing: 0.15em;
  color: var(--text-primary);
}

.field-group { margin-bottom: 1.4rem; }

.field-label {
  display: block; font-size: 0.62rem; font-weight: 900;
  letter-spacing: 0.15em; text-transform: uppercase;
  color: var(--brand-accent); margin-bottom: 0.5rem;
}
[data-theme="light"] .field-label { color: #0369a1; }

.field-input {
  width: 100%; padding: 0.85rem 1rem;
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-radius: 10px; color: var(--text-primary);
  font-size: 0.95rem; font-family: inherit; outline: none;
  appearance: none;
  transition: border-color 0.15s ease;
}
.field-input:focus { border-color: var(--brand-accent); }
.field-input::placeholder { color: var(--text-muted); }
.field-input--readonly { opacity: 0.55; cursor: not-allowed; }

[data-theme="dark"] .field-input { background: #1c1c1f; color: #f8fafc; }
[data-theme="light"] .field-input { background: #ffffff; color: #0f172a; border-color: #cbd5e1; }

.select-wrap { position: relative; }
.field-select { cursor: pointer; }
.select-chev {
  position: absolute; right: 0.9rem; top: 50%;
  transform: translateY(-50%); pointer-events: none; color: var(--text-muted);
}

/* ── Sports checkboxes ── */
.sports-grid {
  display: flex; flex-wrap: wrap; gap: 0.5rem;
}
.sport-checkbox { cursor: pointer; }
.sport-checkbox input { display: none; }
.sport-chip {
  display: inline-block; padding: 0.35rem 0.85rem;
  border-radius: 9999px; font-size: 0.75rem; font-weight: 700;
  border: 1px solid var(--border-subtle);
  color: var(--text-dim);
  background: var(--bg-panel-light);
  transition: all 0.15s ease; cursor: pointer;
}
.sport-chip--on {
  background: color-mix(in srgb, var(--brand-accent) 15%, transparent);
  border-color: var(--brand-accent); color: var(--brand-accent);
}
[data-theme="light"] .sport-chip--on { background: #dbeafe; border-color: #3b82f6; color: #1d4ed8; }

/* ── Save button ── */
.save-btn {
  width: 100%; padding: 1rem; border-radius: 10px; border: none;
  background: #ff007f; color: #000;
  font-weight: 900; font-size: 1rem; font-family: inherit;
  text-transform: uppercase; letter-spacing: 0.05em;
  cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 0.6rem;
  transition: background 0.2s ease, transform 0.15s ease;
  margin-top: 0.5rem;
}
.save-btn:hover:not(:disabled) { background: #fff; color: #000; box-shadow: 0 0 30px rgba(255,0,127,0.3); transform: translateY(-1px); }
.save-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-spinner {
  width: 16px; height: 16px;
  border: 2px solid rgba(0,0,0,0.3);
  border-top-color: #000; border-radius: 50%;
  animation: spin 0.7s linear infinite; flex-shrink: 0;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Banners ── */
.success-banner {
  padding: 0.85rem 1rem; border-radius: 10px;
  background: rgba(0,223,216,0.1); border: 1px solid rgba(0,223,216,0.3);
  color: #00dfd8; font-size: 0.88rem; font-weight: 600;
}
.error-banner {
  padding: 0.85rem 1rem; border-radius: 10px;
  background: rgba(255,0,127,0.08); border: 1px solid rgba(255,0,127,0.25);
  color: #ff007f; font-size: 0.88rem; font-weight: 600;
}

/* ── Background auras (shared with other pages) ── */
.party-bg-mesh {
  position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden;
}
.aura-blob {
  position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.06; pointer-events: none;
}
.aura-1 {
  width: 500px; height: 500px;
  background: var(--brand-primary); top: -100px; right: -100px;
}
.aura-2 {
  width: 400px; height: 400px;
  background: var(--brand-accent); bottom: 0; left: -100px;
}
</style>