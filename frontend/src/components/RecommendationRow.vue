<template>
  <div v-if="events.length > 0" class="rec-row">

    <!-- Header -->
    <div class="rec-header">
      <h2 class="rec-title">{{ title }}</h2>
      <span class="rec-badge" :class="{ 'rec-badge--public': !authStore.isAuthenticated }">
        {{ authStore.isAuthenticated && authStore.isUser ? '✨ Personalized for You' : '🔥 Trending Now' }}
      </span>
    </div>

    <!-- Slider -->
    <div class="slider-outer">
      <!-- Left arrow -->
      <button class="slider-arrow slider-arrow--left" @click="prev" aria-label="Previous">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
          stroke="currentColor" stroke-width="2.5"
          stroke-linecap="round" stroke-linejoin="round">
          <polyline points="15 18 9 12 15 6"/>
        </svg>
      </button>

      <!-- Track viewport -->
      <div class="slider-viewport" ref="viewportRef">
        <div
          class="slider-track"
          :style="{ transform: `translateX(-${offset}px)`, transition: isAnimating ? 'transform 0.5s cubic-bezier(0.25,1,0.5,1)' : 'none' }"
        >
          <!-- Duplicated for seamless loop: original + clone -->
          <div
            v-for="(event, i) in loopedEvents"
            :key="i"
            class="slider-card"
            :style="cardWidth ? { width: cardWidth + 'px' } : {}"
          >
            <EventCard :event="event" />
          </div>
        </div>
      </div>

      <!-- Right arrow -->
      <button class="slider-arrow slider-arrow--right" @click="next" aria-label="Next">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
          stroke="currentColor" stroke-width="2.5"
          stroke-linecap="round" stroke-linejoin="round">
          <polyline points="9 18 15 12 9 6"/>
        </svg>
      </button>
    </div>

    <!-- Dots -->
    <div class="slider-dots">
      <button
        v-for="(_, i) in events"
        :key="i"
        class="dot"
        :class="{ 'dot--active': activeDot === i }"
        @click="goTo(i)"
        :aria-label="`Go to slide ${i + 1}`"
      />
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue';
import axios from 'axios';
import EventCard from './EventCard.vue';
import { useAuthStore } from '../stores/auth';

const props = defineProps({
  title:   { type: String, default: 'Recommended Events' },
  limit:   { type: Number, default: 6 },
  eventId: { type: [String, Number], default: null },
});

const authStore   = useAuthStore();
const events      = ref<any[]>([]);
const viewportRef = ref<HTMLElement | null>(null);

// ── Slider state ──────────────────────────────────────────────────────────
const VISIBLE    = 3;          // cards visible at once
const CARD_GAP   = 24;         // px, matches CSS gap
const cardWidth  = ref(0);     // measured after mount
const currentIdx = ref(0);     // logical index (0 … events.length-1)
const isAnimating = ref(false);

// Duplicate list so we can loop seamlessly
const loopedEvents = computed(() => [...events.value, ...events.value]);

const offset = computed(() => {
  const step = cardWidth.value + CARD_GAP;
  return currentIdx.value * step;
});

const activeDot = computed(() => currentIdx.value % events.value.length);

const measureCard = () => {
  if (!viewportRef.value) return;
  const vw = viewportRef.value.clientWidth;
  cardWidth.value = Math.floor((vw - CARD_GAP * (VISIBLE - 1)) / VISIBLE);
};

// Advance one card
const advance = (dir: 1 | -1) => {
  if (isAnimating.value) return;
  isAnimating.value = true;

  const len = events.value.length;
  let next = currentIdx.value + dir;

  // When we've slid through the first clone-set, jump silently back to origin
  if (next >= len) {
    // animate to the clone, then silently reset
    currentIdx.value = next;
    setTimeout(() => {
      isAnimating.value = false;
      currentIdx.value  = 0;
    }, 520);
  } else if (next < 0) {
    currentIdx.value = len - 1;
    setTimeout(() => { isAnimating.value = false; }, 520);
  } else {
    currentIdx.value = next;
    setTimeout(() => { isAnimating.value = false; }, 520);
  }
};

const next = () => advance(1);
const prev = () => advance(-1);

const goTo = (i: number) => {
  if (isAnimating.value) return;
  isAnimating.value = true;
  currentIdx.value  = i;
  setTimeout(() => { isAnimating.value = false; }, 520);
};

// Auto-advance every 3.5 s
let autoTimer: ReturnType<typeof setInterval> | null = null;

const startAuto = () => {
  autoTimer = setInterval(next, 3500);
};

const stopAuto = () => {
  if (autoTimer) clearInterval(autoTimer);
};

// ── Data fetch ────────────────────────────────────────────────────────────
onMounted(async () => {
  try {
    const config = authStore.token
      ? { headers: { Authorization: `Bearer ${authStore.token}` } }
      : {};
    const url = props.eventId ? `/api/events/${props.eventId}/similar` : '/api/events';
    const res = await axios.get(url, config);
    events.value = res.data.slice(0, props.limit);
  } catch (e) {
    console.error('Failed to load recommendations', e);
  }

  await nextTick();
  measureCard();
  window.addEventListener('resize', measureCard);
  startAuto();
});

onUnmounted(() => {
  stopAuto();
  window.removeEventListener('resize', measureCard);
});
</script>

<style scoped>
/* ── Section wrapper ── */
.rec-row {
  padding: 0.5rem 0;
}

/* ── Header ── */
.rec-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.rec-title {
  font-size: 0.75rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: var(--text-dim);
  margin: 0;
}

.rec-badge {
  background: color-mix(in srgb, #ccff00 10%, transparent);
  color: #ccff00;
  border: 1px solid color-mix(in srgb, #ccff00 25%, transparent);
  padding: 0.3rem 0.8rem;
  border-radius: 9999px;
  font-size: 0.68rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

[data-theme="light"] .rec-badge { color: #4d7c0f; background: rgba(132,204,22,0.12); border-color: rgba(132,204,22,0.3); }

.rec-badge--public {
  background: color-mix(in srgb, #00f3ff 10%, transparent);
  color: #00f3ff;
  border-color: color-mix(in srgb, #00f3ff 25%, transparent);
}

[data-theme="light"] .rec-badge--public { color: #0369a1; background: rgba(14,165,233,0.1); border-color: rgba(14,165,233,0.25); }

/* ── Slider shell ── */
.slider-outer {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

/* ── Arrow buttons ── */
.slider-arrow {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 1px solid var(--border-subtle);
  background: var(--bg-panel);
  color: var(--text-dim);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease, transform 0.15s ease;
  z-index: 2;
}

.slider-arrow:hover {
  background: var(--bg-panel-light);
  color: var(--text-primary);
  transform: scale(1.08);
}

/* ── Viewport: clips overflow ── */
.slider-viewport {
  flex: 1;
  overflow: hidden;
  border-radius: 1rem;
}

/* ── Track: flex row of cards ── */
.slider-track {
  display: flex;
  gap: 24px;
  will-change: transform;
}

/* ── Individual card slot ── */
.slider-card {
  flex-shrink: 0;
  /* Width is set dynamically by JS via inline style; this is just a sane fallback */
  width: 300px;
}

/* ── Dots ── */
.slider-dots {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1.25rem;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  border: none;
  background: var(--border-premium);
  cursor: pointer;
  transition: background 0.2s ease, transform 0.2s ease;
  padding: 0;
}

.dot--active {
  background: var(--brand-accent);
  transform: scale(1.3);
}
</style>
