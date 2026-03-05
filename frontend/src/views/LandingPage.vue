<template>
  <div class="bg-black text-white flex flex-col selection:bg-[#ccff00] selection:text-black overflow-x-hidden">

    <!-- ═══════════════════════════════════════════════════════════════
         HERO + CONTAINER SCROLL — the scroll animation IS the hero
    ════════════════════════════════════════════════════════════════════ -->
    <ContainerScrollAnimation>
      <!-- ── Title slot ────────────────────────────────────────────── -->
      <template #title>
        <!-- Live badge -->
        <div class="inline-flex items-center gap-3 px-5 py-2.5 rounded-full border border-white/10 bg-white/5 backdrop-blur-2xl shadow-2xl hover:bg-white/10 hover:border-white/20 transition-all duration-300 mb-8">
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#ccff00] opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-[#ccff00]"></span>
          </span>
          <span class="text-xs font-bold tracking-[0.2em] text-white/90 uppercase">The Ultimate Sports Platform</span>
        </div>

        <!-- Headline -->
        <h1 class="text-5xl sm:text-7xl md:text-[5.5rem] font-black text-white tracking-tighter leading-[0.9] mb-6 drop-shadow-2xl">
          Experience The <br />
          <span
            class="text-transparent bg-clip-text bg-gradient-to-r from-[#ccff00] via-[#00f3ff] to-[#ccff00] bg-[length:200%_auto] animate-gradient-x"
          >Best Events.</span>
        </h1>

        <!-- Sub-headline -->
        <p class="text-lg md:text-xl text-white/60 font-medium max-w-2xl mx-auto leading-relaxed mb-10">
          Discover massive sports tournaments, secure your tickets instantly, and experience the hype.
        </p>

        <!-- CTAs -->
        <div class="flex flex-col sm:flex-row justify-center gap-4 items-center mb-4">
          <router-link
            to="/register"
            class="group relative px-10 py-4 bg-[#ccff00] text-black font-black text-lg rounded-full overflow-hidden transition-all duration-300 hover:scale-[1.02] active:scale-[0.98] shadow-[0_0_40px_rgba(204,255,0,0.35)] hover:shadow-[0_0_60px_rgba(204,255,0,0.55)]"
          >
            <div class="absolute inset-0 bg-white/40 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ease-out"></div>
            <span class="relative z-10 flex items-center gap-2">
              Sign Up
              <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
              </svg>
            </span>
          </router-link>

          <router-link
            to="/login"
            class="group px-10 py-4 bg-white/5 backdrop-blur-2xl border border-white/10 text-white font-bold text-lg rounded-full transition-all duration-300 hover:bg-white/10 hover:border-white/20 hover:scale-[1.02] active:scale-[0.98] shadow-2xl"
          >
            <span class="flex items-center gap-2">
              Login
              <span class="opacity-70 group-hover:opacity-100 group-hover:text-[#ccff00] transition-all">👋</span>
            </span>
          </router-link>
        </div>
      </template>

      <!-- ── Card content: the user's sports hero image ────────────── -->
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
    <div class="relative z-20 bg-black/80 backdrop-blur-3xl border-t border-white/5 pt-24 pb-24">
      <div class="container mx-auto px-6 max-w-7xl">

        <!-- Section header -->
        <div class="text-center mb-20">
          <h2 class="text-5xl md:text-6xl font-black tracking-tighter text-white mb-4">Your Ticket To The Action</h2>
          <p class="text-[#00f3ff] uppercase tracking-[0.3em] text-sm font-black">Everything you need to enjoy the best sports events</p>
        </div>

        <!-- Cards grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-32">

          <!-- Card 1 -->
          <div class="bg-white/5 border border-white/10 rounded-3xl p-6 md:p-8 backdrop-blur-2xl hover:bg-white/10 hover:border-[#ccff00]/30 hover:-translate-y-2 transition-all duration-500 group relative overflow-hidden flex flex-col text-center">
            <div class="absolute inset-0 bg-gradient-to-br from-[#ccff00]/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div class="w-full h-48 rounded-2xl bg-black/50 border border-white/5 overflow-hidden mb-8 group-hover:shadow-[0_0_20px_rgba(204,255,0,0.2)] transition-all duration-500 shadow-xl relative isolate">
              <img src="/football.png" alt="Football Pitch" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out" />
              <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent"></div>
            </div>
            <h3 class="text-2xl font-black mb-4 text-white tracking-tight relative z-10">Massive Tournaments</h3>
            <p class="text-white/60 leading-relaxed font-medium text-base relative z-10">Gain access to the most exclusive football tournaments and massive stadium events across the city.</p>
          </div>

          <!-- Card 2 -->
          <div class="bg-white/5 border border-white/10 rounded-3xl p-6 md:p-8 backdrop-blur-2xl hover:bg-white/10 hover:border-[#00f3ff]/30 hover:-translate-y-2 transition-all duration-500 group relative overflow-hidden flex flex-col text-center">
            <div class="absolute inset-0 bg-gradient-to-br from-[#00f3ff]/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div class="w-full h-48 rounded-2xl bg-black/50 border border-white/5 overflow-hidden mb-8 group-hover:shadow-[0_0_20px_rgba(0,243,255,0.2)] transition-all duration-500 shadow-xl relative isolate">
              <img src="/basketball.png" alt="Basketball Court" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out" />
              <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent"></div>
            </div>
            <h3 class="text-2xl font-black mb-4 text-white tracking-tight relative z-10">Instant Ticketing</h3>
            <p class="text-white/60 leading-relaxed font-medium text-base relative z-10">Secure your spot instantly with our seamless digital ticketing system. No lines, no hassle.</p>
          </div>

          <!-- Card 3 -->
          <div class="bg-white/5 border border-white/10 rounded-3xl p-6 md:p-8 backdrop-blur-2xl hover:bg-white/10 hover:border-[#ccff00]/30 hover:-translate-y-2 transition-all duration-500 group relative overflow-hidden flex flex-col text-center">
            <div class="absolute inset-0 bg-gradient-to-br from-[#ccff00]/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div class="w-full h-48 rounded-2xl bg-black/50 border border-white/5 overflow-hidden mb-8 group-hover:shadow-[0_0_20px_rgba(204,255,0,0.2)] transition-all duration-500 shadow-xl relative isolate">
              <img src="/cricket.png" alt="Cricket Pitch" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out" />
              <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent"></div>
            </div>
            <h3 class="text-2xl font-black mb-4 text-white tracking-tight relative z-10">Pure Hype</h3>
            <p class="text-white/60 leading-relaxed font-medium text-base relative z-10">Experience the energy of live sports. From boundary side seats to VIP access, we bring you closer.</p>
          </div>
        </div>

        <!-- CTA Banner -->
        <div class="max-w-4xl mx-auto">
          <div class="bg-gradient-to-br from-[#ccff00]/10 to-transparent border border-[#ccff00]/20 rounded-[2.5rem] p-12 md:p-16 relative overflow-hidden group hover:border-[#ccff00]/40 transition-all duration-500 backdrop-blur-3xl flex flex-col items-center text-center">
            <div class="absolute top-0 right-0 w-96 h-96 bg-[#ccff00] rounded-full mix-blend-screen blur-[120px] opacity-10 group-hover:opacity-20 transition-opacity duration-500"></div>
            <div class="flex items-center justify-center mb-8 relative z-10">
              <span class="bg-[#ccff00]/10 text-[#ccff00] border border-[#ccff00]/20 font-black tracking-[0.2em] px-6 py-3 uppercase text-sm rounded-full shadow-[0_0_20px_rgba(204,255,0,0.2)]">Don't Miss Out 🔥</span>
            </div>
            <h3 class="font-black text-5xl md:text-7xl mb-8 text-white relative z-10 tracking-tighter leading-tight drop-shadow-2xl">Secure Your Spot <br/> Today</h3>
            <p class="text-white/60 font-medium leading-relaxed relative z-10 text-xl max-w-2xl mx-auto mb-14 drop-shadow-md">Create an account right now to browse upcoming tournaments, book your tickets, and experience the hype of live sports.</p>
            <router-link
              to="/register"
              class="bg-white text-black hover:bg-[#ccff00] font-black inline-flex justify-between items-center gap-8 text-xl px-12 py-6 rounded-full transition-all duration-300 relative z-10 group/btn shadow-[0_0_30px_rgba(255,255,255,0.2)] hover:shadow-[0_0_50px_rgba(204,255,0,0.4)] hover:scale-105 active:scale-95"
            >
              <span>Sign Up Now</span>
              <span class="text-3xl group-hover/btn:translate-x-2 transition-transform">&rarr;</span>
            </router-link>
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
@keyframes gradient-x {
  0%, 100% { background-position: 0% 50%; }
  50%       { background-position: 100% 50%; }
}
.animate-gradient-x {
  animation: gradient-x 6s ease infinite;
}
</style>
