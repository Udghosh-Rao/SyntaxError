<template>
  <div class="bg-white/5 border border-white/10 rounded-3xl p-6 md:p-8 backdrop-blur-2xl hover:bg-white/10 hover:border-white/20 hover:-translate-y-2 transition-all duration-500 group relative overflow-hidden flex flex-col text-left">
    <!-- Ambient Glow on Hover -->
    <div class="absolute inset-0 bg-gradient-to-br from-[#ccff00]/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"></div>

    <div class="flex justify-between items-start mb-8 relative z-10 w-full">
      <div class="flex items-center gap-2 bg-[#ccff00]/10 text-[#ccff00] border border-[#ccff00]/20 px-3 py-1.5 rounded-full backdrop-blur-md shadow-[0_0_15px_rgba(204,255,0,0.1)]">
        <svg v-if="event.sport_category === 'Football'" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z"></path><path d="M12 12l8.5-5"></path><path d="M12 12l-8.5-5"></path><path d="M12 12V2.5"></path><path d="M12 12l6 8.5"></path><path d="M12 12l-6 8.5"></path></svg>
        <svg v-else-if="event.sport_category === 'Cricket'" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2v20"></path><path d="M8 2v20"></path><path d="M16 2v20"></path><path d="M4 6h16"></path><path d="M4 18h16"></path></svg>
        <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle></svg>
        <span class="font-black tracking-[0.1em] text-[0.65rem] uppercase">{{ event.sport_category }}</span>
      </div>

      <div class="flex gap-1.5 pt-1">
        <span v-for="i in 3" :key="i" class="w-3 h-1.5 rounded-full transition-all duration-300" :class="i <= getPriceTier(event.price_tier) ? 'bg-[#00f3ff] shadow-[0_0_10px_rgba(0,243,255,0.6)]' : 'bg-white/10'"></span>
      </div>
    </div>

    <div class="flex-grow flex flex-col justify-center relative z-10">
      <h3 class="text-3xl font-black mb-6 text-white tracking-tighter leading-[1.1] group-hover:text-[#ccff00] transition-colors duration-300">{{ event.title }}</h3>
      
      <div class="flex flex-col gap-3 mb-8">
        <div class="flex items-center gap-3 text-white/60 font-medium text-sm">
          <span class="text-xl filter drop-shadow-md">📍</span>
          <span>{{ event.venue_city }}</span>
        </div>
        <div class="flex items-center gap-3 text-white/60 font-medium text-sm">
          <span class="text-xl filter drop-shadow-md">📅</span>
          <span>{{ formattedDate }}</span>
        </div>
      </div>
    </div>

    <div class="pt-6 border-t border-white/10 flex justify-between items-end relative z-10 w-full mt-auto">
      <div class="flex flex-col">
        <span class="text-[0.65rem] font-black tracking-[0.15em] text-[#00f3ff] uppercase mb-1">Entry</span>
        <span class="text-2xl font-black leading-none text-white tracking-tighter">₹{{ event.price }}</span>
      </div>
      
      <router-link :to="`/events/${event.id}`" class="bg-white text-black hover:bg-[#ccff00] font-black text-xs px-6 py-3 rounded-full transition-all duration-300 shadow-[0_0_20px_rgba(255,255,255,0.1)] hover:shadow-[0_0_30px_rgba(204,255,0,0.4)] flex items-center gap-2 hover:scale-105 active:scale-95">
        Details
        <span class="text-sm">&rarr;</span>
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
  event: Object as () => any
});

const formattedDate = computed(() => {
  if (!props.event.event_date) return 'TBD';
  const date = new Date(props.event.event_date);
  return date.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
});

const getPriceTier = (tier: string) => {
  if (tier === 'cheap') return 1;
  if (tier === 'mid') return 2;
  if (tier === 'premium') return 3;
  return 1;
};
</script>
