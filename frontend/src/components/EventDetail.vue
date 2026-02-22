<template>
  <div class="event-detail-container">
    <router-link to="/events" class="back-link">← Back to Events</router-link>
    <div v-if="event" class="event-details">
      <img :src="event.image" :alt="event.title" class="event-image" />
      <div class="event-body">
        <h1>{{ event.title }}</h1>
        <div class="event-meta">
          <span class="meta-item">📅 {{ formatDate(event.date) }}</span>
          <span class="meta-item">📍 {{ event.location }}</span>
          <span class="meta-item">👥 {{ event.attendees }} attendees</span>
        </div>
        <p class="description">{{ event.description }}</p>
        <div class="actions">
          <button @click="registerEvent" class="btn btn-primary">Register Event</button>
          <button @click="shareEvent" class="btn btn-secondary">Share Event</button>
        </div>
      </div>
    </div>
    <div v-else>
      <p>Event not found</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const event = ref<any>(null);

// Redundant interface removed

onMounted(() => {
  // Simulate fetching event details
  const eventId = route.params.id;
  event.value = {
    id: eventId,
    title: 'Football Championship',
    date: '2024-02-15',
    location: 'Stadium A',
    image: 'https://via.placeholder.com/600x400?text=Football',
    description: 'Join us for the annual football championship. This is a major event with teams from all across the region competing for the title.',
    attendees: 250,
  };
});

const formatDate = (dateString: string) => {
  const options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

const registerEvent = () => {
  alert('You have registered for the event!');
};

const shareEvent = () => {
  alert('Share event link copied!');
};
</script>

<style scoped>
.event-detail-container {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.back-link {
  color: #00bcd4;
  text-decoration: none;
  font-weight: 500;
  margin-bottom: 2rem;
  display: inline-block;
}

.back-link:hover {
  text-decoration: underline;
}

.event-image {
  width: 100%;
  height: 400px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.event-body h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.event-meta {
  display: flex;
  gap: 2rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.meta-item {
  font-size: 1.1rem;
  color: #666;
}

.description {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #333;
  margin-bottom: 2rem;
}

.actions {
  display: flex;
  gap: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #00bcd4;
  color: white;
}

.btn-primary:hover {
  background-color: #008ba3;
}

.btn-secondary {
  background-color: #f0f0f0;
  color: #333;
}

.btn-secondary:hover {
  background-color: #e0e0e0;
}
</style>
