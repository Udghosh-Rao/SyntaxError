<template>
  <div>
    <!-- FAB -->
    <button
      @click="store.toggleChat"
      class="fixed bottom-6 right-6 z-50 w-12 h-12 rounded-full bg-gray-900 text-white shadow-lg hover:bg-gray-800 transition flex items-center justify-center text-lg"
      :title="store.isOpen ? 'Close' : 'AI Assistant'"
    >
      <span v-if="!store.isOpen">💬</span>
      <span v-else class="text-base">✕</span>
    </button>

    <!-- Chat window -->
    <transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 translate-y-4 scale-95"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100 translate-y-0 scale-100"
      leave-to-class="opacity-0 translate-y-4 scale-95"
    >
      <div v-if="store.isOpen"
        class="fixed bottom-22 right-6 z-50 w-80 bg-white border border-gray-100 rounded-2xl shadow-card-hover flex flex-col overflow-hidden"
        style="height:440px; bottom:88px;"
      >
        <!-- Header -->
        <div class="px-4 py-3 border-b border-gray-100 flex items-center justify-between">
          <div class="flex items-center gap-2.5">
            <div class="w-8 h-8 rounded-full bg-gray-900 flex items-center justify-center text-sm">🤖</div>
            <div>
              <p class="text-xs font-semibold text-gray-900">SportsSync AI</p>
              <p class="text-xs text-gray-400">GPT-4o-mini · RAG</p>
            </div>
          </div>
          <button @click="store.toggleChat" class="text-gray-400 hover:text-gray-600 text-lg leading-none transition">×</button>
        </div>

        <!-- Messages -->
        <div class="flex-1 overflow-y-auto p-4 space-y-3" ref="messagesEl">
          <div v-if="!store.messages.length" class="flex justify-start">
            <div class="bg-gray-100 text-gray-700 text-xs rounded-2xl rounded-tl-sm px-3 py-2 max-w-[80%] leading-relaxed">
              Hi! I can help with events, payments, and registrations. What do you need?
            </div>
          </div>

          <div
            v-for="(msg, i) in store.messages" :key="i"
            class="flex"
            :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
          >
            <div
              class="text-xs rounded-2xl px-3 py-2 max-w-[80%] leading-relaxed"
              :class="msg.role === 'user'
                ? 'bg-gray-900 text-white rounded-tr-sm'
                : 'bg-gray-100 text-gray-700 rounded-tl-sm'"
            >
              {{ msg.text }}
              <p v-if="msg.escalated" class="mt-1 text-yellow-600 text-[10px]">📋 Escalated to support team</p>
            </div>
          </div>

          <!-- Typing indicator -->
          <div v-if="store.loading" class="flex justify-start">
            <div class="bg-gray-100 text-gray-400 rounded-2xl rounded-tl-sm px-4 py-2.5 flex gap-1">
              <span class="w-1.5 h-1.5 rounded-full bg-gray-400 animate-bounce"></span>
              <span class="w-1.5 h-1.5 rounded-full bg-gray-400 animate-bounce" style="animation-delay:.15s"></span>
              <span class="w-1.5 h-1.5 rounded-full bg-gray-400 animate-bounce" style="animation-delay:.3s"></span>
            </div>
          </div>
        </div>

        <!-- Input -->
        <div class="p-3 border-t border-gray-100 flex gap-2">
          <input
            v-model="inputText"
            @keydown.enter="sendMessage"
            :disabled="store.loading"
            class="flex-1 px-3 py-2 bg-gray-50 border border-gray-100 rounded-xl text-xs placeholder-gray-400 outline-none focus:ring-2 focus:ring-gray-200 transition"
            placeholder="Type a message…"
          />
          <button
            @click="sendMessage"
            :disabled="!inputText.trim() || store.loading"
            class="w-8 h-8 rounded-xl bg-gray-900 text-white text-xs disabled:opacity-40 hover:bg-gray-800 transition flex items-center justify-center"
          >→</button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { useChatbotStore } from '@/stores/chatbot'

const store = useChatbotStore()
const inputText = ref('')
const messagesEl = ref(null)

async function sendMessage() {
  if (!inputText.value.trim() || store.loading) return
  const t = inputText.value.trim(); inputText.value = ''
  await store.sendMessage(t)
  await nextTick()
  if (messagesEl.value) messagesEl.value.scrollTop = messagesEl.value.scrollHeight
}
watch(() => store.messages.length, async () => {
  await nextTick()
  if (messagesEl.value) messagesEl.value.scrollTop = messagesEl.value.scrollHeight
})
</script>
