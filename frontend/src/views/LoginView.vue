<template>
  <div class="login-page">

    <!-- Google onboarding overlay for new users -->
    <GoogleOnboarding
      v-if="showOnboarding"
      :name="onboardingName"
      :temp-token="onboardingToken"
      :user-id="onboardingId"
    />

    <!-- ── Left panel: branding ── -->
    <div class="login-left">
      <div class="login-left-inner">
        <router-link to="/" class="brand-logo decoration-transparent">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none"
            stroke="#00f0ff" stroke-width="3"
            stroke-linecap="round" stroke-linejoin="round">
            <path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>
          </svg>
          <span class="brand-name">LIVE<span class="brand-accent">SPORTS</span></span>
        </router-link>

        <div class="brand-copy">
          <h2 class="brand-headline">India's home<br/>for live sports.</h2>
          <p class="brand-sub">Discover tournaments, register instantly, and be part of the action.</p>
        </div>

        <div class="brand-stats">
          <div class="stat">
            <span class="stat-num">2K+</span>
            <span class="stat-label">Events</span>
          </div>
          <div class="stat-sep"></div>
          <div class="stat">
            <span class="stat-num">50K+</span>
            <span class="stat-label">Athletes</span>
          </div>
          <div class="stat-sep"></div>
          <div class="stat">
            <span class="stat-num">100+</span>
            <span class="stat-label">Cities</span>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Right panel: form ── -->
    <div class="login-right">
      <div class="login-card">

        <h1 class="card-heading">Sign in</h1>
        <p class="card-sub">Your game. Your events. Let's go.</p>

        <form @submit.prevent="handleLogin" class="login-form">

          <!-- Email -->
          <div class="field">
            <label class="field-label">Email</label>
            <input
              v-model="email"
              type="email"
              class="field-input"
              placeholder="you@example.com"
              autocomplete="email"
              required
            />
          </div>

          <!-- Password -->
          <div class="field">
            <label class="field-label">Password</label>
            <div class="password-wrap">
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                class="field-input"
                placeholder="••••••••"
                autocomplete="current-password"
                required
              />
              <button
                type="button"
                class="eye-btn"
                :title="showPassword ? 'Hide password' : 'Show password'"
                @click="showPassword = !showPassword"
              >
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

          <!-- Keep me signed in -->
          <label class="remember-row">
            <div class="checkbox-wrap">
              <input v-model="rememberMe" type="checkbox" class="sr-only" />
              <div class="custom-checkbox" :class="{ 'custom-checkbox--checked': rememberMe }">
                <svg v-if="rememberMe" width="10" height="10" viewBox="0 0 12 12"
                  fill="none" stroke="white" stroke-width="2.5"
                  stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="2 6 5 9 10 3"/>
                </svg>
              </div>
            </div>
            <span class="remember-label">Keep me signed in</span>
          </label>

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

          <!-- Sign In -->
          <button type="submit" :disabled="authStore.isLoading" class="btn-primary">
            <span v-if="authStore.isLoading" class="btn-spinner"></span>
            {{ authStore.isLoading ? 'Signing in…' : 'Sign In' }}
          </button>

          <!-- Divider -->
          <div class="divider">
            <span class="divider-line"></span>
            <span class="divider-text">or continue with</span>
            <span class="divider-line"></span>
          </div>

          <!-- Google -->
          <button type="button" class="btn-google" :disabled="googleLoading" @click="handleGoogleLogin">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
              <path d="M5.84 14.1c-.22-.66-.35-1.36-.35-2.1s.13-1.44.35-2.1V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.61z" fill="#FBBC05"/>
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
            </svg>
            {{ googleLoading ? 'Signing in…' : 'Continue with Google' }}
          </button>

        </form>

        <p class="card-footer">
          No account?
          <router-link to="/register" class="card-footer-link">Sign up free</router-link>
        </p>

      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import axios from 'axios';
import GoogleOnboarding from '../components/GoogleOnboarding.vue';

const router        = useRouter();
const authStore     = useAuthStore();
const email         = ref('');
const password      = ref('');
const error         = ref('');
const showPassword  = ref(false);
const rememberMe    = ref(false);
const googleLoading   = ref(false);
const showOnboarding  = ref(false);
const onboardingName  = ref('');
const onboardingToken = ref('');
const onboardingId    = ref(0);

const handleLogin = async () => {
  error.value = '';
  try {
    await authStore.login(email.value, password.value);
    if (!rememberMe.value) sessionStorage.setItem('session_only', '1');
    else sessionStorage.removeItem('session_only');
    redirectAfterLogin();
  } catch (err: any) {
    error.value = err.response?.data?.message || 'Invalid credentials. Please try again.';
  }
};

const handleGoogleLogin = () => {
  googleLoading.value = true;
  error.value = '';

  const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID || '';
  if (!clientId) {
    error.value = 'Google OAuth is not configured (VITE_GOOGLE_CLIENT_ID missing).';
    googleLoading.value = false;
    return;
  }

  if (!(window as any).google?.accounts) {
    error.value = 'Google Sign-In failed to load. Please refresh.';
    googleLoading.value = false;
    return;
  }

  // Shared callback — receives the JWT id_token (credential) from Google
  const handleCredential = async (credentialResponse: { credential?: string }) => {
    if (!credentialResponse.credential) {
      error.value = 'Google Sign-In was cancelled or failed.';
      googleLoading.value = false;
      return;
    }
    try {
      // Send id_token to backend — matches backend's `data.get('id_token')` check
      const res = await axios.post('/api/auth/oauth/google', {
        id_token: credentialResponse.credential,
      });
      if (res.data.is_new_user) {
        onboardingName.value  = res.data.name;
        onboardingToken.value = res.data.temp_token;
        onboardingId.value    = res.data.user_id;
        showOnboarding.value  = true;
      } else {
        authStore.token  = res.data.access_token;
        authStore.role   = res.data.role;
        authStore.userId = res.data.user_id;
        localStorage.setItem('auth_token', res.data.access_token);
        localStorage.setItem('user_role',  res.data.role);
        localStorage.setItem('user_id',    String(res.data.user_id));
        await authStore.fetchProfile();
        redirectAfterLogin();
      }
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Google Sign-In failed.';
    } finally {
      googleLoading.value = false;
    }
  };

  // Initialize with ux_mode: 'popup' — this is what produces the exact two-screen
  // "Choose an account" → "Sign in to LifeSports.com" popup shown in the screenshots
  (window as any).google.accounts.id.initialize({
    client_id: clientId,
    callback: handleCredential,
    ux_mode: 'popup',
    cancel_on_tap_outside: false,
  });

  // Render a hidden GSI button then click it — this is the only way to open
  // the full popup account picker from a user-initiated click (popup blockers
  // require a direct user gesture on the Google-rendered iframe button)
  let host = document.getElementById('__gsi_btn_host__') as HTMLElement;
  if (!host) {
    host = document.createElement('div');
    host.id = '__gsi_btn_host__';
    host.style.cssText = 'position:fixed;top:-9999px;left:-9999px;width:200px;height:40px;overflow:visible;';
    document.body.appendChild(host);
  }

  // Re-render each time to ensure the button is fresh
  host.innerHTML = '';
  (window as any).google.accounts.id.renderButton(host, {
    type: 'standard',
    size: 'large',
    theme: 'outline',
    text: 'signin_with',
    shape: 'rectangular',
  });

  // Small delay to let the GSI iframe render before clicking
  setTimeout(() => {
    const gBtn = host.querySelector('div[role="button"]') as HTMLElement
      || host.querySelector('iframe') as HTMLElement;
    if (gBtn) {
      gBtn.click();
    } else {
      // Last resort: prompt() — shows One Tap sidebar if popup blocked
      (window as any).google.accounts.id.prompt((n: any) => {
        if (n.isNotDisplayed() || n.isSkippedMoment()) {
          error.value = 'Google Sign-In popup was blocked. Please allow popups for this site.';
          googleLoading.value = false;
        }
      });
    }
  }, 300);
};

const redirectAfterLogin = () => {
  if (authStore.isAdmin)          router.push('/admin');
  else if (authStore.isOrganizer) router.push('/organizer');
  else                            router.push('/home');
};
</script>

<style scoped>
/* ══════════════════════════════════════
   PAGE — split 50/50
══════════════════════════════════════ */
.login-page {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1fr 1fr;
  background: var(--bg-site);
}

@media (max-width: 768px) {
  .login-page            { grid-template-columns: 1fr; }
  .login-left            { display: none; }
}

/* ══════════════════════════════════════
   LEFT PANEL — dark brand panel
══════════════════════════════════════ */
.login-left {
  background: linear-gradient(145deg, #070710 0%, #0c1018 50%, #060c14 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  position: relative;
  overflow: hidden;
}

[data-theme="light"] .login-left {
  background: linear-gradient(145deg, #e8ecf0 0%, #dde3ea 50%, #e4e9ef 100%);
}

.login-left::before {
  content: '';
  position: absolute;
  top: -15%; left: -15%;
  width: 65%; height: 65%;
  background: radial-gradient(circle, rgba(0,240,255,0.07) 0%, transparent 70%);
  pointer-events: none;
}

[data-theme="light"] .login-left::before {
  background: radial-gradient(circle, rgba(99,102,241,0.08) 0%, transparent 70%);
}

.login-left::after {
  content: '';
  position: absolute;
  bottom: -15%; right: -15%;
  width: 60%; height: 60%;
  background: radial-gradient(circle, rgba(204,255,0,0.05) 0%, transparent 70%);
  pointer-events: none;
}

[data-theme="light"] .login-left::after {
  background: radial-gradient(circle, rgba(14,165,233,0.07) 0%, transparent 70%);
}

.login-left-inner {
  position: relative;
  z-index: 1;
  max-width: 340px;
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
  padding-top: 2rem;
}

.brand-logo {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  font-weight: 900;
  letter-spacing: -0.03em;
}

.brand-name   { color: #fff; }
.brand-accent { color: #00f0ff; }

[data-theme="light"] .brand-name  { color: #0f172a; }
[data-theme="light"] .brand-accent { color: #0284c7; }

.brand-headline {
  font-size: clamp(1.8rem, 2.5vw, 2.4rem);
  font-weight: 900;
  letter-spacing: -0.04em;
  line-height: 1.1;
  color: #fff;
  margin-bottom: 0.75rem;
}

[data-theme="light"] .brand-headline { color: #0f172a; }

.brand-sub {
  font-size: 0.88rem;
  color: rgba(255,255,255,0.4);
  line-height: 1.65;
}

[data-theme="light"] .brand-sub { color: rgba(15,23,42,0.55); }

.brand-stats {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255,255,255,0.07);
}

[data-theme="light"] .brand-stats { border-top-color: rgba(15,23,42,0.1); }

.stat { display: flex; flex-direction: column; gap: 0.15rem; }

.stat-num {
  font-size: 1.2rem;
  font-weight: 900;
  letter-spacing: -0.03em;
  color: #00f0ff;
}

[data-theme="light"] .stat-num { color: #0284c7; }

.stat-label {
  font-size: 0.65rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: rgba(255,255,255,0.3);
}

[data-theme="light"] .stat-label { color: rgba(15,23,42,0.45); }

.stat-sep {
  width: 1px;
  height: 30px;
  background: rgba(255,255,255,0.08);
}

[data-theme="light"] .stat-sep { background: rgba(15,23,42,0.12); }

/* ══════════════════════════════════════
   RIGHT PANEL — form
══════════════════════════════════════ */
.login-right {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6rem 2rem 3rem; /* top padding clears the floating navbar */
  background: var(--bg-site);
}

.login-card {
  width: 100%;
  max-width: 360px;
  display: flex;
  flex-direction: column;
}

.card-heading {
  font-size: 1.8rem;
  font-weight: 900;
  letter-spacing: -0.04em;
  /* Hardcoded so no global light-mode override can touch it */
  color: #0f172a !important;
  margin-bottom: 0.3rem;
}

/* Dark mode: heading should be white */
@media (prefers-color-scheme: dark) {
  .card-heading { color: #ffffff !important; }
}

/* Use data-theme attribute for reliable override */
[data-theme="dark"] .card-heading  { color: #ffffff !important; }
[data-theme="light"] .card-heading { color: #0f172a !important; }

.card-sub {
  font-size: 0.83rem;
  color: var(--text-muted);
  margin-bottom: 2rem;
}

/* ══════════════════════════════════════
   FIELDS
══════════════════════════════════════ */
.login-form { display: flex; flex-direction: column; }

.field {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin-bottom: 1.1rem;
}

.field-label {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  color: var(--text-dim);
}

.password-wrap { position: relative; }

.field-input {
  width: 100%;
  padding: 0.75rem 1rem;
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

/* ── Keep me signed in ── */
.remember-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  cursor: pointer;
  margin-bottom: 1.25rem;
  user-select: none;
}

.sr-only {
  position: absolute;
  width: 1px; height: 1px;
  padding: 0; margin: -1px;
  overflow: hidden;
  clip: rect(0,0,0,0);
  border: 0;
}

.checkbox-wrap { display: flex; align-items: center; }

.custom-checkbox {
  width: 17px; height: 17px;
  border-radius: 5px;
  border: 1.5px solid var(--border-premium);
  background: var(--bg-panel-light);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s ease, border-color 0.15s ease;
  flex-shrink: 0;
}

.custom-checkbox--checked {
  background: var(--brand-accent);
  border-color: var(--brand-accent);
}

.remember-label {
  font-size: 0.82rem;
  color: var(--text-dim);
}

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

/* ── Sign In button ── */
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
  letter-spacing: 0.01em;
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

/* ── Divider ── */
.divider {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  margin: 1.1rem 0;
}

.divider-line {
  flex: 1;
  height: 1px;
  background: var(--border-subtle);
}

.divider-text {
  font-size: 0.7rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  white-space: nowrap;
}

/* ── Google button ── */
.btn-google {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.65rem;
  padding: 0.75rem;
  background: var(--bg-panel-light);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  color: var(--text-primary);
  font-weight: 600;
  font-size: 0.88rem;
  font-family: inherit;
  cursor: pointer;
  transition: background 0.15s ease, border-color 0.15s ease, transform 0.15s ease;
}

.btn-google:hover:not(:disabled) {
  background: var(--bg-panel);
  border-color: var(--border-premium);
  transform: translateY(-1px);
}

.btn-google:disabled { opacity: 0.5; cursor: not-allowed; }

/* ── Footer ── */
.card-footer {
  margin-top: 1.75rem;
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
</style>