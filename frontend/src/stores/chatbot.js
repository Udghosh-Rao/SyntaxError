import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'

export const useChatbotStore = defineStore('chatbot', () => {
  const messages = ref([])  // { role: 'user'|'bot', text: string, escalated?: bool }
  const isOpen = ref(false)
  const loading = ref(false)

  function toggleChat() {
    isOpen.value = !isOpen.value
  }

  function addMessage(role, text, escalated = false) {
    messages.value.push({ role, text, escalated, timestamp: new Date() })
  }

  async function sendMessage(text) {
    addMessage('user', text)
    loading.value = true

    // Build session context from last 5 messages
    const context = messages.value
      .slice(-10)
      .map(m => `${m.role}: ${m.text}`)
      .join('\n')

    try {
      const res = await api.post('/chatbot', {
        message: text,
        session_context: context,
      })
      addMessage('bot', res.data.response, res.data.escalated)
    } catch {
      addMessage('bot', 'Sorry, I am unable to process your request right now. Please try again later.')
    } finally {
      loading.value = false
    }
  }

  function clearMessages() {
    messages.value = []
  }

  return {
    messages, isOpen, loading,
    toggleChat, sendMessage, addMessage, clearMessages,
  }
})
