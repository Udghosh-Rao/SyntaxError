<template>
  <div class="chatbot-widget">
    <!-- Chat Button -->
    <button 
      v-if="!isOpen" 
      class="chat-toggle-btn animate-corp"
      @click="isOpen = true"
    >
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
      Support Interface
    </button>

    <!-- Chat Window -->
    <div v-else class="chat-window card-premium animate-corp">
      <div class="chat-header-corp">
        <div class="header-main">
          <span class="badge-corp text-xs">AI Core</span>
          <h4 class="font-800 mt-2">Support Terminal</h4>
        </div>
        <button class="close-btn-corp" @click="isOpen = false">&times;</button>
      </div>

      <div class="chat-messages-corp" ref="messagesContainer">
        <div 
          v-for="(msg, index) in messages" 
          :key="index"
          :class="['message-corp', msg.role]"
        >
          <div class="msg-content">{{ msg.content }}</div>
          <div v-if="msg.escalated" class="escalation-warning-corp">
             PROTOCOL ALERT: Transferred to Human Operator
          </div>
        </div>
        <div v-if="loading" class="message-corp bot loading-indicator">
          Synchronizing response...
        </div>
      </div>

      <div class="chat-input-area-corp input-stack">
        <label class="label-muted mb-2">Query Prompt</label>
        <div class="input-action-group">
          <input 
            v-model="inputMsg" 
            @keyup.enter="sendMessage"
            type="text" 
            placeholder="Input operational inquiry..."
            class="input-corp"
            :disabled="loading"
          />
          <button @click="sendMessage" :disabled="!inputMsg.trim() || loading" class="btn-corp btn-corp-primary px-6">
             <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();
const isOpen = ref(false);
const loading = ref(false);
const inputMsg = ref('');
const messagesContainer = ref<HTMLElement | null>(null);

type Message = {
  role: 'user' | 'bot';
  content: string;
  escalated?: boolean;
};

const messages = ref<Message[]>([
  { role: 'bot', content: 'Operational Support Ready. How can I assist with your deployments today?' }
]);

const scrollToBottom = async () => {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

const sendMessage = async () => {
  const txt = inputMsg.value.trim();
  if (!txt) return;

  messages.value.push({ role: 'user', content: txt });
  inputMsg.value = '';
  loading.value = true;
  await scrollToBottom();

  try {
    const config = authStore.token 
        ? { headers: { Authorization: `Bearer ${authStore.token}` } } 
        : {};

    const res = await axios.post(
      '/api/chatbot',
      { message: txt },
      config
    );

    messages.value.push({ 
      role: 'bot', 
      content: res.data.response,
      escalated: res.data.escalated
    });
  } catch (err) {
    messages.value.push({ 
      role: 'bot', 
      content: 'Critical Error: Support Terminal unreachable.' 
    });
  } finally {
    loading.value = false;
    await scrollToBottom();
  }
};
</script>

<style scoped>
.chatbot-widget {
  position: fixed;
  bottom: 3rem;
  right: 3rem;
  z-index: 1000;
}

.chat-toggle-btn {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: var(--brand-primary);
  color: #000;
  border: none;
  padding: 1.25rem 2rem;
  border-radius: var(--radius-pill);
  font-size: 1rem;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 0 10px 40px rgba(0, 240, 255, 0.4);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  transition: all 0.3s var(--ease-luxury);
}

.chat-toggle-btn:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 50px rgba(0, 240, 255, 0.6);
  background: white;
}

.chat-window {
  width: 400px;
  height: 600px;
  display: flex;
  flex-direction: column;
  padding: 0;
  overflow: hidden;
}

.chat-header-corp {
  padding: 2.5rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 1px solid var(--border-subtle);
  background: rgba(255, 255, 255, 0.02);
}

.close-btn-corp {
  background: none;
  border: none;
  color: var(--text-dim);
  font-size: 2rem;
  cursor: pointer;
  line-height: 0.5;
}

.chat-messages-corp {
  flex: 1;
  padding: 2.5rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  background: rgba(0,0,0,0.2);
  scrollbar-width: none;
}

.chat-messages-corp::-webkit-scrollbar { display: none; }

.message-corp {
  max-width: 85%;
  padding: 1.25rem 1.75rem;
  border-radius: var(--radius-md);
  font-size: 0.95rem;
  line-height: 1.5;
}

.message-corp.user {
  align-self: flex-end;
  background: var(--brand-primary);
  color: white;
  border-bottom-right-radius: 2px;
}

.message-corp.bot {
  align-self: flex-start;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
  color: var(--text-primary);
  border-bottom-left-radius: 2px;
}

.escalation-warning-corp {
  margin-top: 1rem;
  color: #ffab00;
  font-size: 0.7rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.chat-input-area-corp {
  padding: 2rem 2.5rem 2.5rem;
  background: var(--bg-secondary);
}

.input-action-group {
  display: flex;
  gap: 1rem;
}

.loading-indicator {
  font-style: italic;
  color: var(--text-dim);
}

.font-800 { font-weight: 800; }
</style>
