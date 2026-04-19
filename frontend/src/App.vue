<template>
  <div
    id="app"
    :class="[isDark ? 'bg-black text-white' : 'text-gray-900']"
    :style="{ background: 'var(--bg-site)', color: 'var(--text-main)' }"
    class="min-h-screen rounded-none flex flex-col"
  >
    <!-- ── Navbar ── -->
    <nav
      class="navbar fixed top-4 left-1/2 -translate-x-1/2 w-[95%] max-w-7xl z-[100] backdrop-blur-2xl rounded-full flex items-center justify-between px-6 py-3 pointer-events-auto"
      :class="{ 'navbar--scrolled': isScrolled }"
    >
      <!-- Logo -->
      <router-link to="/" class="flex items-center gap-2 decoration-transparent">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none"
          style="color: #00f3ff"
          stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
          <path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"></path>
        </svg>
        <span><span class="tracking-tighter font-black text-2xl brand-word-live">LIVE</span><span class="tracking-tighter font-black text-2xl brand-word-sports">SPORTS</span></span>
      </router-link>

      <!-- Desktop links -->
      <div class="hidden md:flex items-center gap-6">

        <!-- Theme Toggle -->
        <button
          @click="toggleTheme"
          class="theme-toggle-btn"
          :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
          aria-label="Toggle theme"
        >
          <span v-if="isDark">☀️</span>
          <span v-else>🌙</span>
        </button>

        <!-- Unauthenticated -->
        <template v-if="!authStore.isAuthenticated">
          <router-link
            to="/"
            class="font-bold tracking-widest uppercase text-xs transition-colors decoration-transparent"
            :style="{ color: isDark ? 'rgba(255,255,255,0.75)' : 'rgba(0,0,0,0.75)' }"
          >Home</router-link>
          <!-- Login & Sign Up hidden when already on /login or /register -->
          <template v-if="!onAuthPage">
            <router-link
              to="/login"
              class="font-bold tracking-widest uppercase text-xs transition-colors decoration-transparent"
              :style="{ color: isDark ? 'rgba(255,255,255,0.75)' : 'rgba(0,0,0,0.75)' }"
            >Login</router-link>
            <router-link
              to="/register"
              class="font-black tracking-wider uppercase text-sm px-8 py-3 rounded-full transition-all duration-300 decoration-transparent"
              style="background: #ccff00; color: #000;"
            >Sign Up</router-link>
          </template>
        </template>

        <!-- Authenticated — profile dropdown -->
        <template v-else>
          <div class="profile-menu-wrap" ref="menuRef">
            <!-- Trigger button -->
            <button class="profile-trigger" @click="menuOpen = !menuOpen" :aria-expanded="menuOpen">
              <!-- Avatar circle with initial -->
              <span class="profile-avatar">
                {{ (authStore.userObj?.name || authStore.role || '?')[0].toUpperCase() }}
              </span>
              <span class="profile-name" :style="{ color: isDark ? 'rgba(255,255,255,0.85)' : 'rgba(0,0,0,0.85)' }">
                {{ authStore.userObj?.name || authStore.role }}
              </span>
              <svg class="profile-chevron" :class="{ 'profile-chevron--open': menuOpen }"
                width="14" height="14" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2.5"
                stroke-linecap="round" stroke-linejoin="round"
                :style="{ color: isDark ? 'rgba(255,255,255,0.5)' : 'rgba(0,0,0,0.5)' }">
                <polyline points="6 9 12 15 18 9"/>
              </svg>
            </button>

            <!-- Dropdown panel -->
            <transition name="dropdown">
              <div v-if="menuOpen" class="profile-dropdown">

                <!-- Header: avatar + name + email -->
                <div class="dropdown-header">
                  <div class="dropdown-avatar">
                    {{ (authStore.userObj?.name || authStore.role || '?')[0].toUpperCase() }}
                  </div>
                  <div class="dropdown-identity">
                    <p class="dropdown-display-name">{{ authStore.userObj?.name || 'User' }}</p>
                    <p class="dropdown-email">{{ authStore.userObj?.email || '' }}</p>
                  </div>
                </div>

                <!-- Menu items — role-specific (hidden for admin) -->
                <template v-if="!authStore.isAdmin">
                  <div class="dropdown-divider"></div>

                  <nav class="dropdown-nav">

                    <!-- Home — role-aware shortcut -->
                    <router-link
                      :to="authStore.isOrganizer ? '/organizer' : '/home'"
                      class="dropdown-item" @click="menuOpen = false">
                      <span class="item-icon">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>
                        </svg>
                      </span>
                      Home
                    </router-link>

                    <!-- Profile -->
                    <router-link to="/profile" class="dropdown-item" @click="menuOpen = false">
                      <span class="item-icon">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
                        </svg>
                      </span>
                      Profile
                    </router-link>

                    <!-- Wallet — user only -->
                    <router-link v-if="authStore.isUser" to="/wallet" class="dropdown-item wallet-item" @click="menuOpen = false; fetchWalletBalance()">
                      <span class="item-icon item-icon--wallet">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/>
                        </svg>
                      </span>
                      Wallet
                      <span v-if="walletBalance !== null" class="wallet-badge">
                        <span class="wallet-coin">🪙</span>
                        <span class="wallet-amount">{{ walletBalance.toFixed(0) }}</span>
                      </span>
                    </router-link>

                    <!-- Events — non-admin roles -->
                    <router-link :to="authStore.isUser ? '/events' : '/organizer/events'"
                      class="dropdown-item" @click="menuOpen = false">
                      <span class="item-icon">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>
                        </svg>
                      </span>
                      Events
                    </router-link>

                    <!-- Dashboard — non-admin roles -->
                    <router-link
                      :to="authStore.isOrganizer ? '/organizer/analytics' : '/dashboard'"
                      class="dropdown-item" @click="menuOpen = false">
                      <span class="item-icon">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
                        </svg>
                      </span>
                      Dashboard
                    </router-link>

                  </nav>

                  <div class="dropdown-divider"></div>
                </template>

                <!-- Admin gets just a divider before Logout -->
                <div v-if="authStore.isAdmin" class="dropdown-divider"></div>

                                <!-- Logout -->
                <button class="dropdown-logout" @click="handleLogout">
                  <span class="item-icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
                    </svg>
                  </span>
                  Logout
                </button>

              </div>
            </transition>
          </div>
        </template>
      </div>

      <!-- Mobile: theme toggle -->
      <div class="flex md:hidden items-center gap-3">
        <button @click="toggleTheme" class="theme-toggle-btn" aria-label="Toggle theme">
          <span v-if="isDark">☀️</span>
          <span v-else>🌙</span>
        </button>
      </div>
    </nav>

    <!-- ── Page content ── -->
    <main class="flex-1 w-full min-h-screen" :style="{ color: 'var(--text-main)' }">
      <router-view />
    </main>

    <!-- ══════════════════════════════════════════════════════════
         FOOTER
    ═══════════════════════════════════════════════════════════════ -->
    <footer class="site-footer">
      <div class="footer-inner">

        <!-- Main 3-zone row: contact | logo | socials -->
        <div class="footer-main">

          <!-- Left: contact info -->
          <div class="footer-zone footer-zone--left">
            <a href="mailto:hello@livesports.in" class="footer-contact-line">hello@livesports.in</a>
            <a href="tel:+918000000000" class="footer-contact-line">+91 80000 00000</a>
            <span class="footer-contact-line footer-addr">Bengaluru, Karnataka, India</span>
          </div>

          <!-- Centre: logo -->
          <div class="footer-zone footer-zone--center">
            <router-link to="/" class="footer-logo decoration-transparent">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none"
                :style="{ color: 'var(--brand-accent)' }"
                stroke="currentColor" stroke-width="3"
                stroke-linecap="round" stroke-linejoin="round">
                <path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>
              </svg>
              <span class="footer-logo-text">
                LIVE<span :style="{ color: 'var(--brand-accent)' }">SPORTS</span>
              </span>
            </router-link>
            <p class="footer-tagline">Beyond Thoughts</p>
          </div>

          <!-- Right: social icons -->
          <div class="footer-zone footer-zone--right">

            <!-- Instagram -->
            <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" aria-label="Instagram" class="social-btn">
              <svg width="32" height="32" viewBox="0 0 32 32">
                <defs>
                  <radialGradient id="ig-bg" cx="25%" cy="110%" r="140%">
                    <stop offset="0%"   stop-color="#fdf497"/>
                    <stop offset="20%"  stop-color="#fdf497"/>
                    <stop offset="40%"  stop-color="#fd5949"/>
                    <stop offset="65%"  stop-color="#d6249f"/>
                    <stop offset="100%" stop-color="#285AEB"/>
                  </radialGradient>
                </defs>
                <rect width="32" height="32" rx="8" fill="url(#ig-bg)"/>
                <rect x="8" y="8" width="16" height="16" rx="4" fill="none" stroke="white" stroke-width="1.6"/>
                <circle cx="16" cy="16" r="4.2" fill="none" stroke="white" stroke-width="1.6"/>
                <circle cx="21.2" cy="10.8" r="1.1" fill="white"/>
              </svg>
            </a>

            <!-- Twitter / X -->
            <a href="https://x.com" target="_blank" rel="noopener noreferrer" aria-label="Twitter / X" class="social-btn">
              <svg width="32" height="32" viewBox="0 0 32 32">
                <rect width="32" height="32" rx="8" fill="#000"/>
                <path fill="#fff" d="M22.16 8.5h2.99l-6.53 7.46 7.68 10.16h-6.02l-4.26-5.63-4.88 5.63H8.15l6.99-7.98-7.38-9.64h6.17l3.85 5.08zm-1.05 15.83h1.66L11.08 10.22H9.29z"/>
              </svg>
            </a>

            <!-- LinkedIn -->
            <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn" class="social-btn">
              <svg width="32" height="32" viewBox="0 0 32 32">
                <rect width="32" height="32" rx="8" fill="#0A66C2"/>
                <path fill="white" d="M10 13h-3v10h3V13zm-1.5-1.4a1.85 1.85 0 1 0 0-3.7 1.85 1.85 0 0 0 0 3.7zm12.5 1.4c-2 0-3.2.9-3.7 1.7V13h-3v10h3v-5.3c0-1.4 1-2.5 2.3-2.5 1.2 0 2.2 1.1 2.2 2.5V23h3v-5.5c0-2.8-1.7-4.5-4-4.5z"/>
              </svg>
            </a>

          </div>
        </div>

        <!-- Divider -->
        <div class="footer-divider"></div>

        <!-- Bottom: copyright + legal links centered -->
        <div class="footer-bottom">
          <p class="footer-copy">© {{ currentYear }} LiveSports · Beyond Thoughts · All rights reserved.</p>
          <nav class="footer-legal">
            <button class="footer-legal-link" @click="openModal('About Us')">About Us</button>
            <button class="footer-legal-link" @click="openModal('Terms of Service')">Terms of Service</button>
            <button class="footer-legal-link" @click="openModal('Privacy Policy')">Privacy Policy</button>
            <button class="footer-legal-link" @click="openModal('Contact')">Contact</button>
          </nav>
        </div>

      </div>
    </footer>

    <!-- Footer modals — Teleported to body to escape footer stacking context -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div v-if="activeModal" class="footer-modal-overlay" @click.self="activeModal = null">
          <div class="footer-modal">
            <div class="footer-modal-header">
              <h2 class="footer-modal-title">{{ activeModal }}</h2>
              <button class="footer-modal-close" @click="activeModal = null" aria-label="Close">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
            </div>
            <div class="footer-modal-body">
              <template v-if="activeModal === 'About Us'">
                <p>Welcome to <strong>LiveSports</strong> — India's premier platform for discovering, registering, and participating in live sports events across the country.</p>
                <p>Founded with a passion for sport and community, we connect athletes, fans, and organizers in one seamless experience. From grassroots tournaments to large-scale championships, LiveSports is where the action begins.</p>
                <p>Our mission is simple: make sport accessible to everyone, everywhere in India. Whether you're a seasoned competitor or a first-time participant, there's a place for you here.</p>
                <p class="footer-modal-placeholder"><em>Full content coming soon. This page is under construction.</em></p>
              </template>
              <template v-else-if="activeModal === 'Terms of Service'">
                <p>By accessing or using the LiveSports platform, you agree to be bound by these Terms of Service. Please read them carefully before registering or participating in any event.</p>
                <p><strong>1. Eligibility</strong> — You must be at least 18 years of age, or have parental consent, to register on this platform.</p>
                <p><strong>2. Account Responsibility</strong> — You are responsible for maintaining the confidentiality of your account credentials and for all activities that occur under your account.</p>
                <p><strong>3. Event Registrations</strong> — All registrations are subject to availability. Refund policies vary by event and are governed by the organizer's terms.</p>
                <p><strong>4. Prohibited Conduct</strong> — Users may not engage in fraudulent activity, misuse referral codes, or violate any applicable laws.</p>
                <p class="footer-modal-placeholder"><em>Full terms coming soon. This document is a placeholder.</em></p>
              </template>
              <template v-else-if="activeModal === 'Privacy Policy'">
                <p>LiveSports is committed to protecting your personal information. This Privacy Policy explains how we collect, use, and safeguard your data.</p>
                <p><strong>Data We Collect</strong> — We collect information you provide directly (name, email, city, sport preferences) and usage data generated through your interactions with the platform.</p>
                <p><strong>How We Use It</strong> — Your data is used to personalise event recommendations, process registrations and payments, and communicate important updates.</p>
                <p><strong>Data Sharing</strong> — We do not sell your personal data. We may share it with event organizers and payment processors strictly as needed to fulfill your registration.</p>
                <p><strong>Your Rights</strong> — You may request access to, correction of, or deletion of your personal data at any time by contacting us.</p>
                <p class="footer-modal-placeholder"><em>Full policy coming soon. This document is a placeholder.</em></p>
              </template>
              <template v-else-if="activeModal === 'Contact'">
                <p>We'd love to hear from you. Reach out to the LiveSports team through any of the channels below.</p>
                <p>📧 <strong>Email:</strong> <a href="mailto:hello@livesports.in" class="footer-modal-link">hello@livesports.in</a></p>
                <p>📞 <strong>Phone:</strong> <a href="tel:+918000000000" class="footer-modal-link">+91 80000 00000</a></p>
                <p>📍 <strong>Office:</strong> Bengaluru, Karnataka, India</p>
                <p>🕐 <strong>Support Hours:</strong> Monday – Friday, 10:00 AM – 6:00 PM IST</p>
                <p class="footer-modal-placeholder"><em>A contact form is coming soon. In the meantime, please email us directly.</em></p>
              </template>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <ChatbotWidget v-if="authStore.isAuthenticated" />
    <ToastNotification />
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref, computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from './stores/auth';
import ChatbotWidget from './components/ChatbotWidget.vue';
import ToastNotification from './components/ToastNotification.vue';
import api from './services/api';

const router = useRouter();
const route  = useRoute();
const authStore = useAuthStore();
const isScrolled = ref(false);
const isDark = ref(true);
const menuOpen = ref(false);
const menuRef  = ref<HTMLElement | null>(null);
const walletBalance = ref<number | null>(null);

const currentYear = computed(() => new Date().getFullYear());
const onAuthPage = computed(() => ['/login', '/register'].includes(route.path));

const fetchWalletBalance = async () => {
  if (!authStore.isAuthenticated || (!authStore.isUser && !authStore.isAdmin)) return;
  try {
    const res = await api.get('/wallet');
    walletBalance.value = res.data.wallet?.balance ?? 0;
  } catch { walletBalance.value = null; }
};

// Refresh wallet balance whenever the route changes (e.g. after checkout)
watch(() => route.path, fetchWalletBalance);

// Also refresh instantly when WalletView fires a wallet-updated event (after top-up)
window.addEventListener('wallet-updated', (e: Event) => {
  const detail = (e as CustomEvent).detail;
  if (typeof detail?.balance === 'number') {
    walletBalance.value = detail.balance;
  } else {
    fetchWalletBalance();
  }
});

// Close dropdown when clicking outside
const handleClickOutside = (e: MouseEvent) => {
  if (menuRef.value && !menuRef.value.contains(e.target as Node)) {
    menuOpen.value = false;
  }
};

const applyTheme = (dark: boolean) => {
  isDark.value = dark;
  document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
  localStorage.setItem('livesports_theme', dark ? 'dark' : 'light');
};

const toggleTheme = () => applyTheme(!isDark.value);
const handleScroll = () => { isScrolled.value = window.scrollY > 20; };

// ── 5-minute inactivity logout ──────────────────────────────
const INACTIVITY_MS = 5 * 60 * 1000;
let inactivityTimer: ReturnType<typeof setTimeout> | null = null;

const resetTimer = () => {
  if (!authStore.isAuthenticated) return;
  if (inactivityTimer) clearTimeout(inactivityTimer);
  inactivityTimer = setTimeout(() => {
    authStore.logout();
    router.push('/login');
  }, INACTIVITY_MS);
};

const ACTIVITY_EVENTS = ['mousemove', 'keydown', 'mousedown', 'touchstart', 'scroll'];

onMounted(() => {
  authStore.initializeAuth();
  if (authStore.isAuthenticated) {
    authStore.fetchProfile();
    fetchWalletBalance();
    resetTimer();
    ACTIVITY_EVENTS.forEach(e => window.addEventListener(e, resetTimer, { passive: true }));
  }
  window.addEventListener('scroll', handleScroll);
  document.addEventListener('click', handleClickOutside);
  const saved = localStorage.getItem('livesports_theme') || 'dark';
  applyTheme(saved === 'dark');
});

onUnmounted(() => {
  if (inactivityTimer) clearTimeout(inactivityTimer);
  ACTIVITY_EVENTS.forEach(e => window.removeEventListener(e, resetTimer));
  document.removeEventListener('click', handleClickOutside);
});

const activeModal = ref<string | null>(null);
const openModal = (name: string) => { activeModal.value = name; };

const handleLogout = () => {
  menuOpen.value = false;
  authStore.logout();
  router.push('/');
};
</script>

<style scoped>
/* ══════════════════════════════════════════
   FOOTER
══════════════════════════════════════════ */
.site-footer {
  background: var(--bg-panel-solid);
  border-top: 1px solid var(--border-subtle);
  transition: background 0.3s ease, border-color 0.3s ease;
  position: relative;
  z-index: 10;
}

/* Dark mode: give the footer a clearly distinct background from the black page */
[data-theme="dark"] .site-footer {
  background: #111113;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* Light mode: contrasting grey gradient */
[data-theme="light"] .site-footer {
  background: linear-gradient(160deg, #e2e8f0 0%, #cbd5e1 100%);
  border-top: none;
}

.footer-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 3.5rem 2rem 2rem;
}

/* ── Main 3-zone row ── */
.footer-main {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 2rem;
  margin-bottom: 2.5rem;
}

.footer-zone { display: flex; flex-direction: column; gap: 0.45rem; }
.footer-zone--left  { align-items: flex-start; }
.footer-zone--center { align-items: center; }
.footer-zone--right {
  align-items: flex-end;
  flex-direction: row;
  justify-content: flex-end;
  gap: 0.6rem;
}

/* ── Contact lines ── */
.footer-contact-line {
  font-size: 0.82rem;
  color: var(--text-dim);
  text-decoration: none;
  letter-spacing: 0.01em;
  line-height: 1.6;
  transition: color 0.15s ease;
  border-bottom: 1px solid var(--border-subtle);
  padding-bottom: 1px;
}

.footer-contact-line:hover { color: var(--text-primary); }
.footer-addr { border-bottom: none; cursor: default; }

/* ── Centre logo ── */
.footer-logo {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 1.3rem;
  font-weight: 900;
  letter-spacing: -0.04em;
  text-decoration: none;
}

.footer-logo-text { color: var(--text-primary); }

.footer-tagline {
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--text-muted);
  text-align: center;
  margin-top: 0.15rem;
}

/* ── Social buttons ── */
.social-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 9px;
  overflow: hidden;
  transition: transform 0.18s ease, box-shadow 0.18s ease;
  text-decoration: none;
  flex-shrink: 0;
}

.social-btn svg {
  width: 32px;
  height: 32px;
  display: block;
}

.social-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 18px rgba(0,0,0,0.3);
}

/* ── Divider ── */
.footer-divider {
  height: 1px;
  background: var(--border-subtle);
  margin-bottom: 1.5rem;
}

/* ── Bottom bar ── */
.footer-bottom {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  text-align: center;
}

.footer-copy {
  font-size: 0.75rem;
  color: var(--text-muted);
}

/* Legal links row */
.footer-legal {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
  justify-content: center;
}

.footer-legal-link {
  font-size: 0.78rem;
  color: var(--text-dim);
  text-decoration: none;
  border-bottom: 1px solid var(--border-subtle);
  padding-bottom: 1px;
  transition: color 0.15s ease, border-color 0.15s ease;
}

.footer-legal-link:hover {
  color: var(--text-primary);
  border-color: var(--text-primary);
}

/* ── Responsive ── */
@media (max-width: 640px) {
  .footer-inner { padding: 2.5rem 1.25rem 1.75rem; }
  .footer-main {
    grid-template-columns: 1fr;
    justify-items: center;
    text-align: center;
  }
  .footer-zone--left  { align-items: center; }
  .footer-zone--right { justify-content: center; }
  .footer-legal { gap: 1rem; }
}

/* ── Navbar — dark mode ── */
.navbar {
  background: rgba(0, 0, 0, 0.70) !important;
  border: 1.5px solid rgba(255, 255, 255, 0.14) !important;
  box-shadow: none;
  transition: background 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
}

.navbar.navbar--scrolled {
  background: rgba(0, 0, 0, 0.88) !important;
  border-color: rgba(0, 243, 255, 0.4) !important;
  box-shadow: 0 0 30px rgba(0, 243, 255, 0.12) !important;
}

/* ── Navbar — light mode overrides ── */
[data-theme="light"] .navbar {
  background: rgba(255, 255, 255, 0.88) !important;
  border: 1.5px solid rgba(0, 0, 0, 0.15) !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
}

[data-theme="light"] .navbar.navbar--scrolled {
  background: rgba(255, 255, 255, 0.96) !important;
  border-color: rgba(0, 0, 0, 0.22) !important;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.14) !important;
}

/* Theme toggle button inside navbar */
.theme-toggle-btn {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.18) !important;
  background: rgba(255, 255, 255, 0.06) !important;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  transition: background 0.2s ease, transform 0.2s ease;
  flex-shrink: 0;
}

[data-theme="light"] .theme-toggle-btn {
  border: 1px solid rgba(0, 0, 0, 0.15) !important;
  background: rgba(0, 0, 0, 0.05) !important;
}

.theme-toggle-btn:hover {
  background: rgba(255, 255, 255, 0.12) !important;
  transform: scale(1.1);
}

[data-theme="light"] .theme-toggle-btn:hover {
  background: rgba(0, 0, 0, 0.1) !important;
}

/* ══════════════════════════════════════════
   PROFILE DROPDOWN
══════════════════════════════════════════ */
/* ── Nav brand ── */
.nav-brand-text   { color: #ffffff; }
.nav-brand-accent { color: #00f3ff; }

[data-theme="light"] .nav-brand-text   { color: #0284c7; }
[data-theme="light"] .nav-brand-accent { color: #0284c7; }

/* Navbar brand — !important beats Tailwind text-white cascade from #app */
.brand-word-live   { color: #ffffff !important; }
.brand-word-sports { color: #00f3ff !important; }

[data-theme="light"] .brand-word-live   { color: #000000 !important; }
[data-theme="light"] .brand-word-sports { color: #0284c7 !important; }

.profile-menu-wrap {
  position: relative;
}

/* Trigger button */
.profile-trigger {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.14);
  border-radius: 9999px;
  padding: 0.35rem 0.75rem 0.35rem 0.35rem;
  cursor: pointer;
  transition: background 0.15s ease, border-color 0.15s ease;
}

.profile-trigger:hover {
  background: rgba(255,255,255,0.12);
  border-color: rgba(255,255,255,0.25);
}

[data-theme="light"] .profile-trigger {
  background: rgba(0,0,0,0.05);
  border-color: rgba(0,0,0,0.15);
}

[data-theme="light"] .profile-trigger:hover {
  background: rgba(0,0,0,0.08);
}

.profile-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--brand-accent);
  color: #000;
  font-size: 0.75rem;
  font-weight: 900;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.profile-name {
  font-size: 0.82rem;
  font-weight: 700;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.profile-chevron {
  transition: transform 0.2s ease;
  flex-shrink: 0;
}

.profile-chevron--open {
  transform: rotate(180deg);
}

/* Dropdown panel */
.profile-dropdown {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  width: 240px;
  background: #18181b;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
  z-index: 200;
}

[data-theme="light"] .profile-dropdown {
  background: #ffffff;
  border-color: #cbd5e1;
  box-shadow: 0 12px 40px rgba(0,0,0,0.15);
}

/* Header */
.dropdown-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1rem 0.75rem;
}

.dropdown-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: var(--brand-accent);
  color: #000;
  font-size: 0.9rem;
  font-weight: 900;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.dropdown-identity { overflow: hidden; }

.dropdown-display-name {
  font-size: 0.88rem;
  font-weight: 700;
  color: #ffffff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

[data-theme="light"] .dropdown-display-name { color: #0f172a; }

.dropdown-email {
  font-size: 0.72rem;
  color: rgba(255,255,255,0.45);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

[data-theme="light"] .dropdown-email { color: #64748b; }

/* Divider */
.dropdown-divider {
  height: 1px;
  background: rgba(255,255,255,0.07);
  margin: 0.25rem 0;
}

[data-theme="light"] .dropdown-divider { background: #e2e8f0; }

/* Nav items */
.dropdown-nav {
  padding: 0.35rem 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.65rem 1rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: rgba(255,255,255,0.75);
  text-decoration: none;
  transition: background 0.12s ease, color 0.12s ease;
  cursor: pointer;
}

.dropdown-item:hover {
  background: rgba(255,255,255,0.07);
  color: #ffffff;
}

[data-theme="light"] .dropdown-item { color: #374151; }
[data-theme="light"] .dropdown-item:hover { background: #f1f5f9; color: #0f172a; }

/* Active route highlight */
.dropdown-item.router-link-active {
  background: rgba(0,243,255,0.08);
  color: var(--brand-accent);
}

[data-theme="light"] .dropdown-item.router-link-active {
  background: rgba(3,105,161,0.08);
  color: #0369a1;
}

/* Icon wrapper */
.item-icon {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: rgba(255,255,255,0.06);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: background 0.12s ease;
}

.dropdown-item:hover .item-icon {
  background: rgba(255,255,255,0.12);
}

[data-theme="light"] .item-icon { background: #f1f5f9; }
[data-theme="light"] .dropdown-item:hover .item-icon { background: #e2e8f0; }

/* Logout button */
.dropdown-logout {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.65rem 1rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: #ff007f;
  background: none;
  border: none;
  cursor: pointer;
  transition: background 0.12s ease;
  font-family: inherit;
  margin-bottom: 0.25rem;
}

.dropdown-logout:hover { background: rgba(255,0,127,0.08); }

.dropdown-logout .item-icon {
  background: rgba(255,0,127,0.1);
  color: #ff007f;
}

.dropdown-logout:hover .item-icon { background: rgba(255,0,127,0.18); }

/* Slide-down animation */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-6px) scale(0.97);
}

/* ── Wallet badge ── */
.wallet-item {
  justify-content: flex-start;
}

.wallet-badge {
  margin-left: auto;
  display: inline-flex;
  align-items: center;
  gap: 3px;
  background: rgba(234, 179, 8, 0.15);
  border: 1px solid rgba(234, 179, 8, 0.35);
  border-radius: 9999px;
  padding: 2px 8px 2px 5px;
  font-size: 0.72rem;
  font-weight: 800;
  color: #eab308;
  line-height: 1;
  transition: background 0.15s ease;
}

.wallet-item:hover .wallet-badge {
  background: rgba(234, 179, 8, 0.25);
}

[data-theme="light"] .wallet-badge {
  background: rgba(161, 98, 7, 0.1);
  border-color: rgba(161, 98, 7, 0.3);
  color: #a16207;
}

.wallet-coin { font-size: 0.75rem; }
.wallet-amount { letter-spacing: -0.01em; }

.item-icon--wallet {
  background: rgba(234, 179, 8, 0.1);
  color: #eab308;
}

.dropdown-item:hover .item-icon--wallet {
  background: rgba(234, 179, 8, 0.2);
}

[data-theme="light"] .item-icon--wallet {
  background: rgba(161, 98, 7, 0.1);
  color: #a16207;
}


/* ── Footer legal buttons ── */
.footer-legal-link {
  background: none;
  border: none;
  cursor: pointer;
  font-family: inherit;
}

</style>

<style>

/* ── Footer modal ── */
.footer-modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 3000;
  background: rgba(0, 0, 0, 0.55);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.footer-modal {
  width: 100%;
  max-width: 560px;
  max-height: 80vh;
  background: var(--bg-panel-solid);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.4);
}

[data-theme="light"] .footer-modal {
  background: #fffaf3;
  border: 1px solid #cbd5e1;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.15);
}

.footer-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 1.75rem 1.25rem;
  border-bottom: 1px solid var(--border-subtle);
  flex-shrink: 0;
}

.footer-modal-title {
  font-size: 1.35rem;
  font-weight: 900;
  letter-spacing: -0.03em;
  color: var(--text-primary);
}

.footer-modal-close {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-panel-light);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  cursor: pointer;
  color: var(--text-muted);
  flex-shrink: 0;
  transition: background 0.15s ease, color 0.15s ease;
}
.footer-modal-close:hover { background: var(--border-subtle); color: var(--text-primary); }

.footer-modal-body {
  padding: 1.5rem 1.75rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
  font-size: 0.9rem;
  line-height: 1.7;
  color: var(--text-dim);
}

.footer-modal-placeholder {
  font-size: 0.8rem;
  color: var(--text-muted);
  padding-top: 0.5rem;
  border-top: 1px solid var(--border-subtle);
  margin-top: 0.25rem;
}

.footer-modal-link {
  color: var(--brand-accent);
  text-decoration: none;
  font-weight: 600;
}
.footer-modal-link:hover { text-decoration: underline; }

/* ── Modal transition ── */
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.2s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }
</style>