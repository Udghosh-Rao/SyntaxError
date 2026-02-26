<template>
  <div class="recommendation-row" v-if="events.length > 0">
    <div class="header">
      <h2>{{ title }}</h2>
      <div v-if="authStore.isAuthenticated && authStore.isUser" class="personalization-badge">
        ✨ Personalized for You
      </div>
      <div v-else class="personalization-badge public">
        🔥 Trending Now
      </div>
    </div>
    
    <div class="scroll-container">
      <div class="events-track">
        <EventCard 
          v-for="event in events.slice(0, limit)" 
          :key="event.id" 
          :event="event" 
          class="compact-card"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import EventCard from './EventCard.vue';
import { useAuthStore } from '../stores/auth';

const props = defineProps({
  title: {
    type: String,
    default: 'Recommended Events'
  },
  limit: {
    type: Number,
    default: 5
  },
  eventId: {
    type: [String, Number],
    default: null
  }
});

const authStore = useAuthStore();
const events = ref<any[]>([]);

onMounted(async () => {
  try {
    const config = authStore.token 
      ? { headers: { Authorization: `Bearer ${authStore.token}` } } 
      : {};
      
    let url = '/api/events';
    if (props.eventId) {
      url = `/api/events/${props.eventId}/similar`;
    }

    const res = await axios.get(url, config);
    events.value = res.data;
  } catch (e) {
    console.error("Failed to load recommendations", e);
  }
});
</script>

<style scoped>
.recommendation-row {
  margin: 0;
  padding: 1rem 0;
  background: transparent;
  border-radius: 0;
  box-shadow: none;
  border: none;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header h2 {
  font-size: 0.8rem;
  color: rgba(255,255,255,0.5);
  text-transform: uppercase;
  letter-spacing: 0.2em;
  font-weight: 800;
  margin-bottom: 0;
}

.personalization-badge {
  background: rgba(204, 255, 0, 0.1);
  color: #ccff00;
  padding: 0.35rem 0.85rem;
  border-radius: var(--radius-pill);
  font-size: 0.7rem;
  font-weight: 800;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border: 1px solid rgba(204, 255, 0, 0.2);
  box-shadow: 0 0 10px rgba(204, 255, 0, 0.1);
}

.personalization-badge.public {
  background: rgba(0, 243, 255, 0.1);
  color: #00f3ff;
  border: 1px solid rgba(0, 243, 255, 0.2);
  box-shadow: 0 0 10px rgba(0, 243, 255, 0.1);
}

.scroll-container {
  overflow-x: auto;
  padding: 1rem 0;
  /* Hide scrollbar */
  scrollbar-width: none;
}

.scroll-container::-webkit-scrollbar {
  display: none;
}

.events-track {
  display: flex;
  gap: 2rem;
  width: max-content;
}

.compact-card {
  width: 320px;
  min-width: 320px;
}
</style>
