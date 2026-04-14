<template>
  <div class="chat-widget">

    <!-- Floating icon button -->
    <button
      v-if="!isOpen"
      class="chat-fab"
      @click="isOpen = true"
      aria-label="Open support chat"
      title="Support"
    >
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
        stroke="currentColor" stroke-width="2.5"
        stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
      </svg>
    </button>

    <!-- Chat window -->
    <div v-else class="chat-window">

      <!-- Header -->
      <div class="chat-header">
        <div class="chat-header-left">
          <div class="chat-avatar">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2.5"
              stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
          </div>
          <div>
            <p class="chat-name">LiveSports Support</p>
            <p class="chat-status">
              <span class="status-dot"></span> Online
            </p>
          </div>
        </div>
        <div class="chat-header-actions">
          <button class="chat-icon-btn" @click="clearChat" title="Clear conversation" aria-label="Clear chat">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2.5"
              stroke-linecap="round" stroke-linejoin="round">
              <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
              <path d="M10 11v6"/><path d="M14 11v6"/>
            </svg>
          </button>
          <button class="chat-close" @click="isOpen = false" aria-label="Close">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2.5"
              stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Messages -->
      <div class="chat-messages" ref="messagesContainer">
        <div
          v-for="(msg, i) in messages"
          :key="i"
          class="msg-row"
          :class="msg.role === 'user' ? 'msg-row--user' : 'msg-row--bot'"
        >
          <div class="msg-bubble" :class="msg.role === 'user' ? 'msg-bubble--user' : 'msg-bubble--bot'">
            {{ msg.content }}
          </div>
          <p v-if="msg.escalated" class="escalation-note">
            ⚠ Transferred to a human agent
          </p>
        </div>

        <!-- Typing indicator -->
        <div v-if="loading" class="msg-row msg-row--bot">
          <div class="msg-bubble msg-bubble--bot typing-bubble">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
          </div>
        </div>
      </div>

      <!-- Quick suggestions (shown only at start) -->
      <div v-if="messages.length === 1" class="chat-suggestions">
        <button
          v-for="s in suggestions"
          :key="s"
          class="suggestion-chip"
          @click="sendSuggestion(s)"
        >{{ s }}</button>
      </div>

      <!-- Input -->
      <div class="chat-input-row">
        <input
          v-model="inputMsg"
          type="text"
          class="chat-input"
          placeholder="Ask something…"
          :disabled="loading"
          @keyup.enter="sendMessage"
        />
        <button
          class="chat-send"
          :disabled="!inputMsg.trim() || loading"
          @click="sendMessage"
          aria-label="Send"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2.5"
            stroke-linecap="round" stroke-linejoin="round">
            <line x1="22" y1="2" x2="11" y2="13"/>
            <polygon points="22 2 15 22 11 13 2 9 22 2"/>
          </svg>
        </button>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();
const isOpen    = ref(false);
const loading   = ref(false);
const inputMsg  = ref('');
const messagesContainer = ref<HTMLElement | null>(null);

// Unique session ID per browser tab so each tab has its own conversation history
const sessionId = `session_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`;

type Message = { role: 'user' | 'bot'; content: string; escalated?: boolean };

const messages = ref<Message[]>([
  { role: 'bot', content: 'Hi! I\'m the LiveSports assistant. How can I help you today?' },
]);

const suggestions = [
  'How do I register for an event?',
  'What payment methods are accepted?',
  'Show me upcoming events',
  'How do I cancel my registration?',
];

const scrollToBottom = async () => {
  await nextTick();
  if (messagesContainer.value)
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
};

const sendMessage = async () => {
  const txt = inputMsg.value.trim();
  if (!txt || loading.value) return;
  messages.value.push({ role: 'user', content: txt });
  inputMsg.value = '';
  loading.value  = true;
  await scrollToBottom();

  try {
    const headers: any = { 'Content-Type': 'application/json' };
    if (authStore.token) headers.Authorization = `Bearer ${authStore.token}`;

    const res = await axios.post(
      '/api/chatbot',
      { message: txt, session_id: sessionId },
      { headers }
    );
    messages.value.push({
      role: 'bot',
      content: res.data.response,
      escalated: res.data.escalated,
    });
  } catch {
    messages.value.push({
      role: 'bot',
      content: 'Sorry, something went wrong. Please try again.',
    });
  } finally {
    loading.value = false;
    await scrollToBottom();
  }
};

const sendSuggestion = (text: string) => {
  inputMsg.value = text;
  sendMessage();
};

const clearChat = () => {
  messages.value = [
    { role: 'bot', content: 'Hi! I\'m the LiveSports assistant. How can I help you today?' },
  ];
};
</script>

<style scoped>
/* ── Widget container ── */
.chat-widget {
  position: fixed;
  bottom: 1.75rem;
  right: 1.75rem;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

/* ── FAB button ── */
.chat-fab {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: none;
  background: var(--brand-accent);
  color: #000;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 20px color-mix(in srgb, var(--brand-accent) 35%, transparent);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.chat-fab:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 28px color-mix(in srgb, var(--brand-accent) 50%, transparent);
}

/* ── Chat window ── */
.chat-window {
  width: 340px;
  max-height: 520px;
  display: flex;
  flex-direction: column;
  background: var(--bg-panel-solid);
  border: 1px solid var(--border-subtle);
  border-radius: 18px;
  overflow: hidden;
  box-shadow: 0 8px 40px rgba(0,0,0,0.2);
}

[data-theme="light"] .chat-window {
  background: #ffffff;
  border-color: #cbd5e1;
  box-shadow: 0 8px 40px rgba(0,0,0,0.12);
}

/* ── Header ── */
.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.1rem;
  border-bottom: 1px solid var(--border-subtle);
  flex-shrink: 0;
}

.chat-header-left {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.chat-header-actions {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.chat-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--brand-accent);
  color: #000;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.chat-name {
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.2;
}

.chat-status {
  font-size: 0.68rem;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 0.3rem;
  line-height: 1.2;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #22c55e;
  flex-shrink: 0;
}

.chat-icon-btn,
.chat-close {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-muted);
  padding: 0.25rem;
  display: flex;
  align-items: center;
  border-radius: 6px;
  transition: background 0.15s ease, color 0.15s ease;
}

.chat-icon-btn:hover,
.chat-close:hover {
  background: var(--bg-panel-light);
  color: var(--text-primary);
}

/* ── Messages ── */
.chat-messages {
  flex: 1;
  padding: 1rem 1.1rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  scrollbar-width: none;
  min-height: 0;
}

.chat-messages::-webkit-scrollbar { display: none; }

.msg-row { display: flex; flex-direction: column; }
.msg-row--user { align-items: flex-end; }
.msg-row--bot  { align-items: flex-start; }

.msg-bubble {
  max-width: 82%;
  padding: 0.6rem 0.9rem;
  border-radius: 14px;
  font-size: 0.85rem;
  line-height: 1.55;
}

.msg-bubble--user {
  background: var(--brand-accent);
  color: #000;
  border-bottom-right-radius: 4px;
}

.msg-bubble--bot {
  background: var(--bg-panel-light);
  border: 1px solid var(--border-subtle);
  color: var(--text-primary);
  border-bottom-left-radius: 4px;
}

[data-theme="light"] .msg-bubble--bot {
  background: #f1f5f9;
  border-color: #e2e8f0;
}

/* Typing indicator */
.typing-bubble {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 0.65rem 0.9rem;
}

.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--text-muted);
  animation: bounce 1.2s ease infinite;
}

.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 80%, 100% { transform: translateY(0); }
  40%           { transform: translateY(-5px); }
}

.escalation-note {
  font-size: 0.68rem;
  color: #f59e0b;
  margin-top: 0.35rem;
  font-weight: 600;
}

/* ── Quick suggestions ── */
.chat-suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  padding: 0 1rem 0.75rem;
  flex-shrink: 0;
}

.suggestion-chip {
  padding: 0.3rem 0.75rem;
  border-radius: 9999px;
  border: 1px solid var(--border-subtle);
  background: var(--bg-panel-light);
  color: var(--text-dim);
  font-size: 0.72rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s ease, border-color 0.15s ease, color 0.15s ease;
  white-space: nowrap;
  font-family: inherit;
}

.suggestion-chip:hover {
  background: var(--brand-accent);
  border-color: var(--brand-accent);
  color: #000;
}

[data-theme="light"] .suggestion-chip {
  background: #f1f5f9;
  border-color: #cbd5e1;
  color: #475569;
}

[data-theme="light"] .suggestion-chip:hover {
  background: var(--brand-accent);
  border-color: var(--brand-accent);
  color: #000;
}

/* ── Input row ── */
.chat-input-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-top: 1px solid var(--border-subtle);
  flex-shrink: 0;
}

.chat-input {
  flex: 1;
  background: var(--bg-panel-light);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  padding: 0.55rem 0.85rem;
  font-size: 0.85rem;
  font-family: inherit;
  color: var(--text-primary);
  outline: none;
  transition: border-color 0.15s ease;
}

.chat-input::placeholder { color: var(--text-muted); }
.chat-input:focus { border-color: var(--brand-accent); }

[data-theme="light"] .chat-input {
  background: #f8fafc;
  border-color: #e2e8f0;
}

.chat-send {
  width: 34px;
  height: 34px;
  border-radius: 9px;
  border: none;
  background: var(--brand-accent);
  color: #000;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: opacity 0.15s ease, transform 0.15s ease;
}

.chat-send:hover:not(:disabled) {
  opacity: 0.88;
  transform: scale(1.05);
}

.chat-send:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>