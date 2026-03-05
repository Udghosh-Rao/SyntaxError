<script setup lang="ts">
/**
 * HeroScrollDemo.vue
 *
 * Demo usage of ContainerScrollAnimation in the Vue 3 project.
 * Drop this into any view or integrate it directly in LandingPage.vue.
 *
 * Best place: between the hero section and the feature cards in LandingPage.vue
 */
import ContainerScrollAnimation from "@/components/ui/ContainerScrollAnimation.vue";
</script>

<template>
  <div class="flex flex-col overflow-hidden bg-black">
    <ContainerScrollAnimation>
      <!-- Title slot -->
      <template #title>
        <h1 class="text-4xl font-semibold text-white">
          Discover the power of <br />
          <span
            class="text-4xl md:text-[6rem] font-black mt-1 leading-none
                   text-transparent bg-clip-text
                   bg-gradient-to-r from-[#ccff00] via-[#00f3ff] to-[#ccff00]"
          >
            Scroll Animations
          </span>
        </h1>
      </template>

      <!-- Card content -->
      <img
        src="https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=1400&q=80"
        alt="Sports Event"
        class="mx-auto rounded-2xl object-cover h-full w-full object-center"
        draggable="false"
      />
    </ContainerScrollAnimation>
  </div>
</template>
