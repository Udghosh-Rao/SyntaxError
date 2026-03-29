<template>
  <div class="event-card group">
    <!-- Hover glow -->
    <div class="card-glow"></div>

    <!-- Top row: sport badge + price tier dots -->
    <div class="card-top">
      <div class="sport-badge">
        <svg v-if="event.sport_category === 'Football'" width="13" height="13"
          viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z"/>
          <path d="M12 12l8.5-5"/><path d="M12 12l-8.5-5"/>
          <path d="M12 12V2.5"/><path d="M12 12l6 8.5"/><path d="M12 12l-6 8.5"/>
        </svg>
        <svg v-else-if="event.sport_category === 'Cricket'" width="13" height="13"
          viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M12 2v20"/><path d="M8 2v20"/><path d="M16 2v20"/>
          <path d="M4 6h16"/><path d="M4 18h16"/>
        </svg>
        <svg v-else width="13" height="13" viewBox="0 0 24 24"
          fill="none" stroke="currentColor" stroke-width="2.5">
          <circle cx="12" cy="12" r="10"/>
        </svg>
        <span class="sport-label">{{ event.sport_category }}</span>
      </div>

      <div class="tier-dots">
        <span
          v-for="i in 3" :key="i"
          class="tier-dot"
          :class="i <= getPriceTier(event.price_tier) ? 'tier-dot--on' : 'tier-dot--off'"
        />
      </div>
    </div>

    <!-- Title + meta -->
    <div class="card-body">
      <h3 class="card-title">{{ event.title }}</h3>
      <div class="card-meta">
        <span class="meta-item">
          <span class="meta-icon">📍</span>
          {{ event.venue_city }}
        </span>
        <span class="meta-item">
          <span class="meta-icon">📅</span>
          {{ formattedDate }}
        </span>
      </div>
    </div>

    <!-- Footer: price + CTA -->
    <div class="card-footer">
      <div class="price-block">
        <span class="price-label">Entry</span>
        <span class="price-value">₹{{ event.price }}</span>
      </div>
      <router-link :to="`/events/${event.id}`" class="details-btn">
        Details <span>&rarr;</span>
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({ event: Object as () => any });

const formattedDate = computed(() => {
  if (!props.event.event_date) return 'TBD';
  return new Date(props.event.event_date).toLocaleDateString('en-GB', {
    day: '2-digit', month: 'short', year: 'numeric',
  });
});

const getPriceTier = (tier: string) => ({ cheap: 1, mid: 2, premium: 3 }[tier] ?? 1);
</script>

<style scoped>
/* ══════════════════════════════════════════
   CARD SHELL — fixed height so all cards
   in the slider are identical size
══════════════════════════════════════════ */
.event-card {
  /* Fixed height ensures uniform cards in the slider */
  height: 280px;
  display: flex;
  flex-direction: column;

  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-radius: 1.5rem;
  padding: 1.5rem;
  position: relative;
  overflow: hidden;
  transition: background 0.25s ease, border-color 0.25s ease, transform 0.25s ease, box-shadow 0.25s ease;
  text-align: left;
  cursor: default;
}

.event-card:hover {
  transform: translateY(-4px);
  border-color: var(--border-premium);
  box-shadow: var(--shadow-luxury);
}

[data-theme="light"] .event-card {
  background: #ffffff;
  border-color: #cbd5e1;
  box-shadow: 0 2px 10px rgba(0,0,0,0.06);
}

[data-theme="light"] .event-card:hover {
  border-color: #94a3b8;
  box-shadow: 0 6px 24px rgba(0,0,0,0.1);
}

/* Hover glow — dark mode only */
.card-glow {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(204,255,0,0.05) 0%, transparent 70%);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.4s ease;
}

.event-card:hover .card-glow { opacity: 1; }
[data-theme="light"] .event-card:hover .card-glow { opacity: 0; }

/* ══════════════════════════════════════════
   TOP ROW
══════════════════════════════════════════ */
.card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  flex-shrink: 0;
}

/* Sport badge */
.sport-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.3rem 0.75rem;
  border-radius: 9999px;
  /* Dark mode — lime neon */
  background: rgba(204,255,0,0.1);
  border: 1px solid rgba(204,255,0,0.2);
  color: #ccff00;
  transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease;
}

/* Light mode — replace neon lime with readable dark green */
[data-theme="light"] .sport-badge {
  background: rgba(22,163,74,0.1);
  border-color: rgba(22,163,74,0.25);
  color: #15803d;
}

.sport-label {
  font-size: 0.62rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

/* Price tier dots */
.tier-dots { display: flex; gap: 4px; align-items: center; }

.tier-dot {
  width: 10px;
  height: 6px;
  border-radius: 9999px;
  transition: background 0.2s ease;
}

.tier-dot--on {
  background: #00f3ff;
  box-shadow: 0 0 6px rgba(0,243,255,0.5);
}

[data-theme="light"] .tier-dot--on {
  background: #0284c7;
  box-shadow: none;
}

.tier-dot--off { background: var(--border-premium); }

/* ══════════════════════════════════════════
   BODY — flex-grows to fill remaining space
══════════════════════════════════════════ */
.card-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 0;
  overflow: hidden;
}

.card-title {
  font-size: 1.15rem;
  font-weight: 900;
  letter-spacing: -0.02em;
  line-height: 1.2;
  color: var(--text-primary);
  margin-bottom: 0.75rem;
  /* Clamp to 2 lines so varying title lengths don't shift layout */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color 0.2s ease;
}

.event-card:hover .card-title {
  color: var(--brand-primary);
}

[data-theme="light"] .event-card:hover .card-title {
  color: #7c3aed;
}

.card-meta {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--text-dim);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.meta-icon { font-size: 0.9rem; flex-shrink: 0; }

/* ══════════════════════════════════════════
   FOOTER ROW — always pinned to bottom
══════════════════════════════════════════ */
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding-top: 0.85rem;
  border-top: 1px solid var(--border-subtle);
  flex-shrink: 0;
  margin-top: auto;
}

.price-block {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.price-label {
  font-size: 0.58rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--brand-accent);
}

[data-theme="light"] .price-label { color: #0369a1; }

.price-value {
  font-size: 1.4rem;
  font-weight: 900;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  line-height: 1;
}

/* Details button */
.details-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: var(--text-primary);
  color: var(--bg-site);
  font-weight: 900;
  font-size: 0.75rem;
  padding: 0.55rem 1.1rem;
  border-radius: 9999px;
  text-decoration: none;
  transition: background 0.2s ease, color 0.2s ease, transform 0.15s ease, box-shadow 0.15s ease;
}

.details-btn:hover {
  background: var(--brand-primary);
  color: #000;
  transform: scale(1.05);
  box-shadow: 0 0 20px color-mix(in srgb, var(--brand-primary) 30%, transparent);
}
</style>
