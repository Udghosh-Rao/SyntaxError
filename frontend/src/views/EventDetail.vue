<template>
  <div class="event-detail">
    <button @click="goBack" class="back-btn">← Back</button>
    <div v-if="event" class="detail-container">
      <h1>{{ event.title }}</h1>
      <img :src="event.image" :alt="event.title" class="event-image">
      <div class="detail-info">
        <p><strong>Date:</strong> {{ formatDate(event.date) }}</p>
        <p><strong>Location:</strong> {{ event.location }}</p>
        <p><strong>Organizer:</strong> {{ event.organizer.name }}</p>
        <p><strong>Description:</strong> {{ event.description }}</p>
        <p><strong>Attendees:</strong> {{ event.attendees.length }} / {{ event.capacity }}</p>
      </div>
      <button v-if="!isAttending" @click="registerForEvent" class="register-btn">Register</button>
      <button v-else @click="unregister" class="unregister-btn">Unregister</button>
      <EventDetail :event="event" />
    </div>
    <div v-else class="loading">Loading event details...</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useEventsStore } from '@/stores/events';
import { useAuthStore } from '@/stores/auth';
import EventDetail from '@/components/EventDetail.vue';

const route = useRoute();
const router = useRouter();
const eventsStore = useEventsStore();
const authStore = useAuthStore();

const eventId = route.params.id as string;
const event = ref<any>(null);
const isAttending = computed(() => {
  if (!event.value) return false;
  return event.value.attendees.some((a: any) => a.id === authStore.currentUser?.id);
});

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString();
};

const goBack = () => router.back();

const registerForEvent = async () => {
  try {
    await eventsStore.registerForEvent(eventId);
    await loadEventDetails();
  } catch (error) {
    console.error('Registration failed:', error);
  }
};

const unregister = async () => {
  try {
    await eventsStore.unregisterFromEvent(eventId);
    await loadEventDetails();
  } catch (error) {
    console.error('Unregister failed:', error);
  }
};

const loadEventDetails = async () => {
  event.value = eventsStore.getEventById(eventId);
};

onMounted(() => {
  loadEventDetails();
});
</script>

<style scoped>
.event-detail {
  padding: 2rem;
}

.back-btn {
  padding: 0.5rem 1rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 1rem;
}

.detail-container {
  max-width: 800px;
  margin: 0 auto;
}

.event-image {
  width: 100%;
  height: 400px;
  object-fit: cover;
  border-radius: 8px;
  margin: 1rem 0;
}

.detail-info {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
}

.register-btn,
.unregister-btn {
  padding: 0.75rem 1.5rem;
  margin-right: 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.register-btn {
  background: #28a745;
  color: white;
}

.unregister-btn {
  background: #dc3545;
  color: white;
}

.loading {
  text-align: center;
  padding: 2rem;
}
</style>
