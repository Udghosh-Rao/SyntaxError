<template>
  <div class="chat-container">
    <div class="chat-header">
      <h2>Event Chat Assistant</h2>
    </div>
    <div class="messages">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['message', message.type]"
      >
        {{ message.text }}
      </div>
    </div>
    <div class="input-area">
      <input
        v-model="inputText"
        type="text"
        placeholder="Ask about the event..."
        @keyup.enter="sendMessage"
      />
      <button @click="sendMessage" class="send-btn">Send</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

interface Message {
  text: string;
  type: 'user' | 'assistant';
}

const inputText = ref('');
const messages = ref<Message[]>([
  {
    text: 'Hello! How can I help you with the event?',
    type: 'assistant',
  },
]);

const sendMessage = () => {
  if (inputText.value.trim()) {
    messages.value.push({
      text: inputText.value,
      type: 'user',
    });

    // Simulate assistant response
    setTimeout(() => {
      messages.value.push({
        text: 'I can help you with event information, registration, and more!',
        type: 'assistant',
      });
    }, 500);

    inputText.value = '';
  }
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 500px;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}

.chat-header {
  background-color: #00bcd4;
  color: white;
  padding: 1rem;
  text-align: center;
}

.chat-header h2 {
  margin: 0;
  font-size: 1.2rem;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background-color: #f5f5f5;
}

.message {
  margin-bottom: 1rem;
  padding: 0.75rem 1rem;
  border-radius: 4px;
  max-width: 80%;
}

.message.user {
  background-color: #00bcd4;
  color: white;
  margin-left: auto;
  text-align: right;
}

.message.assistant {
  background-color: #e0e0e0;
  color: #333;
}

.input-area {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid #ddd;
  background-color: white;
}

.input-area input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.send-btn {
  padding: 0.5rem 1rem;
  background-color: #00bcd4;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.send-btn:hover {
  background-color: #008ba3;
}
</style>
