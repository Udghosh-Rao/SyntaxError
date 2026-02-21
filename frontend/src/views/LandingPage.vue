<template>
  <div class="min-h-screen bg-white">
    <!-- Nav -->
    <header class="sticky top-0 z-40 border-b border-gray-100 bg-white/90 backdrop-blur-sm">
      <div class="mx-auto max-w-6xl px-6 h-14 flex items-center justify-between">
        <span class="text-base font-bold tracking-tight text-gray-900">SportsSync</span>
        <div class="flex items-center gap-2">
          <router-link to="/login">
            <button class="px-4 py-1.5 text-sm font-medium text-gray-600 hover:text-gray-900 transition">Login</button>
          </router-link>
          <router-link to="/register">
            <button class="px-4 py-1.5 text-sm font-medium bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition shadow-btn">Register</button>
          </router-link>
        </div>
      </div>
    </header>

    <!-- Hero -->
    <section class="mx-auto max-w-6xl px-6 pt-24 pb-20 text-center">
      <span class="inline-flex items-center gap-1.5 px-3 py-1 bg-green-50 text-green-700 text-xs font-semibold rounded-full ring-1 ring-green-200 mb-6">
        🏆 India's Sports Event Platform
      </span>
      <h1 class="text-5xl md:text-6xl font-extrabold tracking-tight text-gray-900 mb-5 leading-tight">
        Discover sports events<br class="hidden md:block" />
        <span class="text-primary-600">near you.</span>
      </h1>
      <p class="text-lg text-gray-500 max-w-xl mx-auto mb-9 leading-relaxed">
        Smart AI recommendations, instant registration, and secure payments — all in one platform.
      </p>
      <div class="flex items-center justify-center gap-3 flex-wrap">
        <router-link to="/register">
          <button class="px-6 py-2.5 bg-gray-900 text-white text-sm font-semibold rounded-lg hover:bg-gray-800 transition shadow-btn">
            Get Started →
          </button>
        </router-link>
        <router-link to="/login">
          <button class="px-6 py-2.5 border border-gray-200 text-gray-700 text-sm font-semibold rounded-lg hover:border-gray-300 hover:bg-gray-50 transition">
            Sign In
          </button>
        </router-link>
      </div>

      <!-- Stats -->
      <div class="mt-16 grid grid-cols-3 divide-x divide-gray-100 border border-gray-100 rounded-xl overflow-hidden max-w-lg mx-auto">
        <div class="p-5" v-for="s in stats" :key="s.label">
          <div class="text-2xl font-bold text-gray-900">{{ s.value }}</div>
          <div class="text-xs text-gray-400 mt-0.5">{{ s.label }}</div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="bg-gray-50 border-y border-gray-100 py-20">
      <div class="mx-auto max-w-6xl px-6">
        <h2 class="text-2xl font-bold text-gray-900 text-center mb-2">Everything you need</h2>
        <p class="text-gray-500 text-center mb-12">A complete platform for athletes and organizers.</p>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          <div
            v-for="f in features" :key="f.icon"
            class="bg-white rounded-xl p-6 border border-gray-100 shadow-card hover:shadow-card-hover transition-shadow"
          >
            <div class="w-10 h-10 rounded-lg bg-gray-50 border border-gray-100 flex items-center justify-center text-xl mb-4">{{ f.icon }}</div>
            <h3 class="text-sm font-semibold text-gray-900 mb-1">{{ f.title }}</h3>
            <p class="text-xs text-gray-500 leading-relaxed">{{ f.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Sports -->
    <section class="mx-auto max-w-6xl px-6 py-20">
      <h2 class="text-2xl font-bold text-gray-900 text-center mb-10">Sports we cover</h2>
      <div class="flex flex-wrap justify-center gap-3">
        <span
          v-for="s in sports" :key="s.name"
          class="inline-flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-full text-sm text-gray-700 hover:border-gray-300 transition cursor-default"
        >
          {{ s.emoji }} {{ s.name }}
        </span>
      </div>
    </section>

    <!-- Footer -->
    <footer class="border-t border-gray-100 py-8 text-center text-xs text-gray-400">
      <p class="font-semibold text-gray-700 mb-1">SportsSync</p>
      <p>SE Team 026 – Syntax Error · Sports Event Management MVP · © 2026</p>
    </footer>
  </div>
</template>

<script setup>
const stats = [
  { value: '18', label: 'AI Features' },
  { value: '26', label: 'API Endpoints' },
  { value: '100%', label: 'Secure Payments' },
]
const features = [
  { icon: '🤖', title: 'AI Recommendations', desc: 'Personalised event suggestions based on your sport, location, and budget.' },
  { icon: '💳', title: 'Secure Payments', desc: 'Register and pay instantly via Razorpay — UPI, cards, and wallets.' },
  { icon: '📊', title: 'Analytics Dashboards', desc: 'Live fill-rate, revenue, and registration trend charts for organizers.' },
  { icon: '🔍', title: 'Instant Search', desc: 'Algolia-powered typo-tolerant search across all sports and cities.' },
  { icon: '💬', title: '24/7 AI Chatbot', desc: 'LangChain RAG chatbot answers questions from a curated FAQ knowledge base.' },
  { icon: '🏅', title: 'Role-Based Access', desc: 'Three tiers: Participants, Organizers, and Admins — each with their own view.' },
]
const sports = [
  { emoji: '⚽', name: 'Football' }, { emoji: '🏏', name: 'Cricket' },
  { emoji: '🎾', name: 'Tennis' },  { emoji: '🏀', name: 'Basketball' },
  { emoji: '🏃', name: 'Running' }, { emoji: '🏸', name: 'Badminton' },
  { emoji: '🏊', name: 'Swimming' },{ emoji: '🚴', name: 'Cycling' },
]
</script>
