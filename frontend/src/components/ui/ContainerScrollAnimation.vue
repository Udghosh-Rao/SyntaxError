<script setup lang="ts">
/**
 * ContainerScrollAnimation.vue
 *
 * Vue 3 adaptation of the React ContainerScroll component.
 * Uses motion-v (the Vue-native framer-motion) for scroll-driven 3D tilt animations.
 *
 * Usage:
 *   <ContainerScrollAnimation>
 *     <template #title>
 *       <h1>Your Title Here</h1>
 *     </template>
 *     <!-- card content goes here -->
 *     <img src="..." />
 *   </ContainerScrollAnimation>
 */
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useScroll, useTransform, Motion } from "motion-v";

// ─── Scroll tracking ────────────────────────────────────────────────────────
const containerRef = ref<HTMLDivElement | null>(null);

const { scrollYProgress } = useScroll({
  target: containerRef,
});

// ─── Mobile detection ────────────────────────────────────────────────────────
const isMobile = ref(false);
const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768;
};

onMounted(() => {
  checkMobile();
  window.addEventListener("resize", checkMobile);
});

onUnmounted(() => {
  window.removeEventListener("resize", checkMobile);
});

// ─── Motion transforms ───────────────────────────────────────────────────────
const scaleDimensions = computed(() =>
  isMobile.value ? [0.7, 0.9] : [1.05, 1]
);

const rotate = useTransform(scrollYProgress, [0, 1], [20, 0]);
const scale = useTransform(
  scrollYProgress,
  [0, 1],
  scaleDimensions.value
);
const translateY = useTransform(scrollYProgress, [0, 1], [0, -100]);
</script>

<template>
  <!-- Scroll container -->
  <div
    ref="containerRef"
    class="h-[60rem] md:h-[80rem] flex items-center justify-center relative p-2 md:p-20"
  >
    <div
      class="py-10 md:py-40 w-full relative"
      style="perspective: 1000px"
    >
      <!-- ── Title / Header ─────────────────────────────────────────────── -->
      <Motion
        :style="{ translateY }"
        class="max-w-5xl mx-auto text-center"
      >
        <slot name="title" />
      </Motion>

      <!-- ── Card (3D tilt effect) ──────────────────────────────────────── -->
      <Motion
        :style="{
          rotateX: rotate,
          scale,
          boxShadow:
            '0 0 #0000004d, 0 9px 20px #0000004a, 0 37px 37px #00000042, 0 84px 50px #00000026, 0 149px 60px #0000000a, 0 233px 65px #00000003',
        }"
        class="max-w-5xl mt-8 mx-auto h-[30rem] md:h-[40rem] w-full border-4 border-[#6C6C6C] p-2 md:p-6 bg-[#222222] rounded-[30px] shadow-2xl"
      >
        <div
          class="h-full w-full overflow-hidden rounded-2xl bg-gray-100 dark:bg-zinc-900 md:rounded-2xl md:p-4"
        >
          <!-- card content slot -->
          <slot />
        </div>
      </Motion>
    </div>
  </div>
</template>
