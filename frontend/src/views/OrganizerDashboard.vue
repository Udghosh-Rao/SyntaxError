<template>
  <div class="organizer-dashboard">
    <h1>Organizer Dashboard</h1>
    <div class="dashboard-container">
      <div class="stats-section">
        <div class="stat-card">
          <h3>Total Events</h3>
          <p class="stat-number">{{ organizedEvents.length }}</p>
        </div>
        <div class="stat-card">
          <h3>Total Attendees</h3>
          <p class="stat-number">{{ totalAttendees }}</p>
        </div>
        <div class="stat-card">
          <h3>Total Revenue</h3>
          <p class="stat-number">₹{{ totalRevenue }}</p>
        </div>
      </div>
      <div class="actions-section">
        <button @click="createNewEvent" class="btn btn-primary">+ Create Event</button>
      </div>
      <div class="events-section">
        <h2>My Events</h2>
        <div v-if="organizedEvents.length > 0" class="events-list">
          <div v-for="event in organizedEvents" :key="event.id" class="event-card">
            <h3>{{ event.title }}</h3>
            <p>{{ event.description }}</p>
            <p><strong>Date:</strong> {{ formatDate(event.date) }}</p>
            <p><strong>Attendees:</strong> {{ event.attendees.length }} / {{ event.capacity }}</p>
            <button @click="editEvent(event)" class="btn btn-secondary">Edit</button>
            <button @click="deleteEvent(event.id)" class="btn btn-danger">Delete</button>
          </div>
        </div>
        <div v-else class="no-events">
          <p>You haven't created any events yet</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useEventsStore } from '@/stores/events';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const eventsStore = useEventsStore();
const authStore = useAuthStore();

const organizedEvents = computed(() => {
  return eventsStore.events.filter(e => e.organizer.id === authStore.currentUser?.id);
});

const totalAttendees = computed(() => {
  return organizedEvents.value.reduce((sum, e) => sum + e.attendees.length, 0);
});

const totalRevenue = computed(() => {
  return organizedEvents.value.reduce((sum, e) => sum + (e.registrationFee * e.attendees.length), 0);
});

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString();
};

const createNewEvent = () => {
  router.push({ name: 'CreateEvent' });
};

const editEvent = (event: any) => {
  router.push({ name: 'EditEvent', params: { id: event.id } });
};

const deleteEvent = async (eventId: string) => {
  if (confirm('Are you sure you want to delete this event?')) {
    try {
      await eventsStore.deleteEvent(eventId);
    } catch (error) {
      console.error('Failed to delete event:', error);
    }
  }
};

onMounted(() => {
  if (!authStore.isAuthenticated || authStore.currentUser?.role !== 'organizer') {
    router.push({ name: 'Home' });
  }
});
</script>

<style scoped>
.organizer-dashboard {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  margin: 0.5rem 0 0 0;
}

.actions-section {
  display: flex;
  gap: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover {
  background: #0056b3;
}

.btn-secondary {
  background: #6c757d;
  color: white;
  padding: 0.5rem 1rem;
}

.btn-danger {
  background: #dc3545;
  color: white;
  padding: 0.5rem 1rem;
}

.events-section h2 {
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.events-list {
  display: grid;
  gap: 1.5rem;
}

.event-card {
  background: white;
  border: 1px solid #e0e0e0;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.event-card h3 {
  margin-top: 0;
}

.event-card button {
  margin-right: 0.5rem;
  margin-top: 1rem;
}

.no-events {
  text-align: center;
  padding: 2rem;
  color: #666;
}
</style>
