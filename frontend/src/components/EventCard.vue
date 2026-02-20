<template>
  <div class="event-card">
    <div class="card-image">
      <img :src="event.image" :alt="event.title" class="event-image" />
      <div class="card-badge">{{ event.sport }}</div>
    </div>
    
    <div class="card-content">
      <h3 class="event-title">{{ event.title }}</h3>
      
      <div class="event-info">
        <div class="info-item">
          <span class="icon">📅</span>
          <span>{{ formatDate(event.date) }}</span>
        </div>
        <div class="info-item">
          <span class="icon">📍</span>
          <span>{{ event.location }}</span>
        </div>
        <div class="info-item">
          <span class="icon">👥</span>
          <span>{{ event.registrations }} registered</span>
        </div>
      </div>
      
      <p class="event-description">{{ event.description }}</p>
      
      <div class="card-footer">
        <div class="price-info">
          <span class="label">Entry Fee:</span>
          <span class="price">${{ event.entryFee }}</span>
        </div>
        <router-link :to="`/events/${event.id}`" class="btn-details">
          View Details
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Event {
  id: string;
  title: string;
  description: string;
  date: string;
  location: string;
  sport: string;
  image: string;
  entryFee: number;
  registrations: number;
}

defineProps<{
  event: Event;
}>();

const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  });
};
</script>

<style scoped>
.event-card {
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
  transition: all 0.3s ease;
  background: white;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.event-card:hover {
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  transform: translateY(-4px);
}

.card-image {
  position: relative;
  height: 200px;
  overflow: hidden;
  background: #f0f0f0;
}

.event-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: #3b82f6;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 600;
}

.card-content {
  padding: 1.5rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.event-title {
  font-size: 1.25rem;
  font-weight: bold;
  margin: 0 0 1rem 0;
  color: #1f2937;
}

.event-info {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.icon {
  font-size: 1rem;
}

.event-description {
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.5;
  margin: 0 0 1rem 0;
  flex: 1;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #f0f0f0;
  padding-top: 1rem;
  margin-top: auto;
}

.price-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.label {
  font-size: 0.75rem;
  color: #9ca3af;
  text-transform: uppercase;
}

.price {
  font-size: 1.5rem;
  font-weight: bold;
  color: #3b82f6;
}

.btn-details {
  background: #3b82f6;
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 0.375rem;
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 600;
  transition: background 0.3s;
}

.btn-details:hover {
  background: #2563eb;
}
</style>
