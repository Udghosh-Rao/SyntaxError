<template>
  <router-view />
  <ChatbotWidget v-if="authStore.isLoggedIn && authStore.userRole === 'user'" />
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import ChatbotWidget from '@/components/ChatbotWidget.vue'
const authStore = useAuthStore()
</script>
