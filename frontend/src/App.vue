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
        <span class="tracking-tighter font-black text-2xl"
          :style="{ color: isDark ? '#ffffff' : '#000000' }">
          LIVE<span style="color: #00f3ff">SPORTS</span>
        </span>
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

        <!-- Authenticated -->
        <template v-else>
          <router-link
            v-if="authStore.isUser"
            to="/home"
            class="font-bold tracking-widest uppercase text-xs transition-colors decoration-transparent"
            :style="{ color: isDark ? 'rgba(255,255,255,0.75)' : 'rgba(0,0,0,0.75)' }"
          >Browse</router-link>

          <router-link
            v-if="authStore.isOrganizer"
            to="/organizer"
            class="font-bold tracking-widest uppercase text-xs transition-colors decoration-transparent"
            :style="{ color: isDark ? 'rgba(255,255,255,0.75)' : 'rgba(0,0,0,0.75)' }"
          >Dashboard</router-link>

          <router-link
            v-if="authStore.isAdmin"
            to="/admin"
            class="font-bold tracking-widest uppercase text-xs transition-colors decoration-transparent"
            :style="{ color: isDark ? 'rgba(255,255,255,0.75)' : 'rgba(0,0,0,0.75)' }"
          >Admin</router-link>

          <button
            @click="handleLogout"
            class="px-8 py-3 rounded-full font-black tracking-wider uppercase text-sm transition-all duration-300"
            :style="{
              border: '1px solid #ff007f',
              color: '#ff007f',
              background: 'transparent',
            }"
          >Logout</button>
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
            <a href="#" aria-label="Instagram" class="social-btn">
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
            <a href="#" aria-label="Twitter / X" class="social-btn">
              <svg width="32" height="32" viewBox="0 0 32 32">
                <rect width="32" height="32" rx="8" fill="#000"/>
                <path fill="#fff" d="M22.16 8.5h2.99l-6.53 7.46 7.68 10.16h-6.02l-4.26-5.63-4.88 5.63H8.15l6.99-7.98-7.38-9.64h6.17l3.85 5.08zm-1.05 15.83h1.66L11.08 10.22H9.29z"/>
              </svg>
            </a>

            <!-- LinkedIn -->
            <a href="#" aria-label="LinkedIn" class="social-btn">
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
            <a href="#" class="footer-legal-link">About Us</a>
            <a href="#" class="footer-legal-link">Terms of Service</a>
            <a href="#" class="footer-legal-link">Privacy Policy</a>
            <a href="#" class="footer-legal-link">Contact</a>
          </nav>
        </div>

      </div>
    </footer>

    <ChatbotWidget v-if="authStore.isAuthenticated" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from './stores/auth';
import ChatbotWidget from './components/ChatbotWidget.vue';

const router = useRouter();
const route  = useRoute();
const authStore = useAuthStore();
const isScrolled = ref(false);
const isDark = ref(true);

const currentYear = computed(() => new Date().getFullYear());

// true when on /login or /register — used to trim navbar links
const onAuthPage = computed(() => ['/login', '/register'].includes(route.path));

// ── Theme persistence ──
const applyTheme = (dark: boolean) => {
  isDark.value = dark;
  document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
  localStorage.setItem('livesports_theme', dark ? 'dark' : 'light');
};

const toggleTheme = () => {
  applyTheme(!isDark.value);
};

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20;
};

onMounted(() => {
  authStore.initializeAuth();
  window.addEventListener('scroll', handleScroll);
  const saved = localStorage.getItem('livesports_theme') || 'dark';
  applyTheme(saved === 'dark');
});

const handleLogout = () => {
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
</style>