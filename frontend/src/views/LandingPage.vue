<template>
  <div class="landing-root">

    <!-- ═══════════════════════════════════════════════════════════════
         HERO + CONTAINER SCROLL
    ════════════════════════════════════════════════════════════════════ -->
    <ContainerScrollAnimation>

      <!-- ── Title slot ────────────────────────────────────────────── -->
      <template #title>

        <!-- Live badge -->
        <div class="live-badge">
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#ccff00] opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-[#ccff00]"></span>
          </span>
          <span class="live-badge-text">The Ultimate Sports Platform</span>
        </div>

        <!-- Headline -->
        <h1 class="hero-headline">
          Experience The <br />
          <span class="headline-gradient animate-gradient-x">Best Events.</span>
        </h1>

        <!-- Sub-headline -->
        <p class="hero-sub">
          Discover massive sports tournaments, secure your tickets instantly, and experience the hype.
        </p>
      </template>

      <!-- ── Hero image ─────────────────────────────────────────────── -->
      <img
        src="/sports-hero.jpg"
        alt="Elite athlete on a stadium track ready to sprint"
        class="w-full h-full object-cover object-center rounded-2xl"
        draggable="false"
      />
    </ContainerScrollAnimation>

    <!-- ═══════════════════════════════════════════════════════════════
         FEATURE CARDS
    ════════════════════════════════════════════════════════════════════ -->
    <div class="features-section">
      <div class="container mx-auto px-6 max-w-7xl">

        <!-- Section header -->
        <div class="text-center mb-20">
          <h2 class="section-title">Your Ticket To The Action</h2>
          <p class="section-sub">Everything you need to enjoy the best sports events</p>
        </div>

        <!-- Cards grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-32">

          <!-- Card 1 -->
          <div class="feature-card group">
            <div class="feature-card-glow from-[#ccff00]/5"></div>
            <div class="feature-img-wrap group-hover:shadow-[0_0_20px_rgba(204,255,0,0.2)]">
              <img src="/football.png" alt="Football Pitch" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out" />
              <div class="feature-img-overlay"></div>
            </div>
            <h3 class="feature-title">Massive Tournaments</h3>
            <p class="feature-body">Gain access to the most exclusive football tournaments and massive stadium events across the city.</p>
          </div>

          <!-- Card 2 -->
          <div class="feature-card group">
            <div class="feature-card-glow from-[#00f3ff]/5"></div>
            <div class="feature-img-wrap group-hover:shadow-[0_0_20px_rgba(0,243,255,0.2)]">
              <img src="/basketball.png" alt="Basketball Court" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out" />
              <div class="feature-img-overlay"></div>
            </div>
            <h3 class="feature-title">Instant Ticketing</h3>
            <p class="feature-body">Secure your spot instantly with our seamless digital ticketing system. No lines, no hassle.</p>
          </div>

          <!-- Card 3 -->
          <div class="feature-card group">
            <div class="feature-card-glow from-[#ccff00]/5"></div>
            <div class="feature-img-wrap group-hover:shadow-[0_0_20px_rgba(204,255,0,0.2)]">
              <img src="/cricket.png" alt="Cricket Pitch" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out" />
              <div class="feature-img-overlay"></div>
            </div>
            <h3 class="feature-title">Pure Hype</h3>
            <p class="feature-body">Experience the energy of live sports. From boundary side seats to VIP access, we bring you closer.</p>
          </div>
        </div>


      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import ContainerScrollAnimation from "@/components/ui/ContainerScrollAnimation.vue";
</script>

<style scoped>
/* ══════════════════════════════════════════
   GRADIENT ANIMATION
══════════════════════════════════════════ */
@keyframes gradient-x {
  0%, 100% { background-position: 0% 50%; }
  50%       { background-position: 100% 50%; }
}
.animate-gradient-x {
  animation: gradient-x 6s ease infinite;
}

/* ══════════════════════════════════════════
   ROOT WRAPPER
══════════════════════════════════════════ */
.landing-root {
  background: var(--bg-site);
  color: var(--text-main);
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
  transition: background 0.3s ease, color 0.3s ease;
}

/* ══════════════════════════════════════════
   HERO — LIVE BADGE
══════════════════════════════════════════ */
.live-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem 1.25rem;
  border-radius: 9999px;
  border: 1px solid var(--border-subtle);
  background: var(--bg-panel);
  backdrop-filter: blur(24px);
  box-shadow: 0 8px 32px rgba(0,0,0,0.12);
  margin-bottom: 2rem;
  transition: background 0.2s ease, border-color 0.2s ease;
}

.live-badge:hover {
  background: var(--bg-panel-light);
  border-color: var(--border-premium);
}

.live-badge-text {
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--text-main);
}

/* ══════════════════════════════════════════
   HERO — HEADLINE
══════════════════════════════════════════ */
.hero-headline {
  font-size: clamp(2.8rem, 8vw, 5.5rem);
  font-weight: 900;
  color: var(--text-primary);
  letter-spacing: -0.04em;
  line-height: 0.9;
  margin-bottom: 1.5rem;
  filter: drop-shadow(0 2px 8px rgba(0,0,0,0.15));
}

.headline-gradient {
  /* Dark mode: lime→cyan gradient */
  background: linear-gradient(90deg, #ccff00, #00f3ff, #ccff00);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Light mode: use a richer, darker gradient so it pops on white */
[data-theme="light"] .headline-gradient {
  background: linear-gradient(90deg, #5b21b6, #0284c7, #5b21b6);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* ══════════════════════════════════════════
   HERO — SUB-HEADLINE
══════════════════════════════════════════ */
.hero-sub {
  font-size: clamp(1rem, 2vw, 1.2rem);
  color: var(--text-dim);
  font-weight: 500;
  max-width: 42rem;
  margin: 0 auto 2.5rem auto;
  line-height: 1.65;
}

/* ══════════════════════════════════════════
   HERO — CTA BUTTONS
══════════════════════════════════════════ */
.cta-primary {
  position: relative;
  padding: 1rem 2.5rem;
  background: var(--brand-primary);
  color: #000;
  font-weight: 900;
  font-size: 1.1rem;
  border-radius: 9999px;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 0 40px color-mix(in srgb, var(--brand-primary) 35%, transparent);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
}

.cta-primary:hover {
  transform: scale(1.02);
  box-shadow: 0 0 60px color-mix(in srgb, var(--brand-primary) 55%, transparent);
}

.cta-primary:active { transform: scale(0.98); }

.cta-secondary {
  padding: 1rem 2.5rem;
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  color: var(--text-primary);
  font-weight: 700;
  font-size: 1.1rem;
  border-radius: 9999px;
  transition: background 0.2s ease, border-color 0.2s ease, transform 0.2s ease;
  backdrop-filter: blur(24px);
  box-shadow: 0 8px 32px rgba(0,0,0,0.08);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
}

.cta-secondary:hover {
  background: var(--bg-panel-light);
  border-color: var(--border-premium);
  transform: scale(1.02);
}

.cta-secondary:active { transform: scale(0.98); }

/* ══════════════════════════════════════════
   FEATURES SECTION WRAPPER
══════════════════════════════════════════ */
.features-section {
  position: relative;
  z-index: 20;
  background: var(--bg-site);
  border-top: 1px solid var(--border-subtle);
  padding: 6rem 0 2rem;
  transition: background 0.3s ease;
}

/* ══════════════════════════════════════════
   SECTION HEADER
══════════════════════════════════════════ */
.section-title {
  font-size: clamp(2rem, 5vw, 3.5rem);
  font-weight: 900;
  letter-spacing: -0.04em;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.section-sub {
  color: var(--brand-accent);
  text-transform: uppercase;
  letter-spacing: 0.3em;
  font-size: 0.8rem;
  font-weight: 900;
}

/* Light mode: section-sub uses a visible purple accent */
[data-theme="light"] .section-sub {
  color: var(--brand-primary);
}

/* ══════════════════════════════════════════
   FEATURE CARDS
══════════════════════════════════════════ */
.feature-card {
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-radius: 1.5rem;
  padding: 1.5rem 2rem;
  backdrop-filter: blur(24px);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  text-align: center;
  transition: background 0.3s ease, border-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  background: var(--bg-panel-light);
  transform: translateY(-8px);
  box-shadow: var(--shadow-luxury);
}

.feature-card-glow {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom right, var(--from-color, transparent), transparent);
  opacity: 0;
  transition: opacity 0.5s ease;
  pointer-events: none;
}

.feature-card:hover .feature-card-glow {
  opacity: 1;
}

.feature-img-wrap {
  width: 100%;
  height: 12rem;
  border-radius: 1rem;
  background: var(--bg-panel-solid);
  border: 1px solid var(--border-subtle);
  overflow: hidden;
  margin-bottom: 2rem;
  transition: box-shadow 0.5s ease;
  box-shadow: 0 8px 30px rgba(0,0,0,0.15);
  position: relative;
  isolation: isolate;
}

.feature-img-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0.1) 40%, transparent 100%);
}

/* Light mode: lighter overlay so images aren't too dark */
[data-theme="light"] .feature-img-overlay {
  background: linear-gradient(to top, rgba(0,0,0,0.25) 0%, transparent 60%);
}

.feature-title {
  font-size: 1.4rem;
  font-weight: 900;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  margin-bottom: 1rem;
  position: relative;
  z-index: 10;
}

.feature-body {
  color: var(--text-dim);
  line-height: 1.65;
  font-weight: 500;
  font-size: 0.95rem;
  position: relative;
  z-index: 10;
}
</style>
