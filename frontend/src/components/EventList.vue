<template>
  <div class="event-list-container">
    <div class="filters">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search events..."
        class="search-input"
      />
      <select v-model="selectedCategory" class="category-select">
        <option value="">All Categories</option>
        <option value="sports">Sports</option>
        <option value="music">Music</option>
        <option value="tech">Tech</option>
      </select>
    </div>
    <div class="events-grid">
      <div
        v-for="event in filteredEvents"
        :key="event.id"
        class="event-card"
        @click="goToEventDetail(event.id)"
      >
        <img :src="event.image" :alt="event.title" class="event-image" />
        <div class="event-info">
          <h3>{{ event.title }}</h3>
          <p class="date">{{ formatDate(event.date) }}</p>
          <p class="location">📍 {{ event.location }}</p>
          <p class="attendees">{{ event.attendees }} attendees</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const searchQuery = ref('');
const selectedCategory = ref('');

const events = ref([
  {
    id: 1,
    title: 'Football Championship',
    date: '2024-02-15',
    location: 'Stadium A',
    category: 'sports',
    image: 'https://via.placeholder.com/300x200?text=Football',
    attendees: 250,
  },
]);

const filteredEvents = computed(() => {
  return events.value.filter((event) => {
    const matchesSearch = event.title
      .toLowerCase()
      .includes(searchQuery.value.toLowerCase());
    const matchesCategory =
      !selectedCategory.value ||
      event.category === selectedCategory.value;
    return matchesSearch && matchesCategory;
  });
});

const formatDate = (dateString: string) => {
  const options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

const goToEventDetail = (eventId: number) => {
  router.push(`/events/${eventId}`);
};
</script>

<style scoped>
.event-list-container {
  padding: 2rem;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.search-input,
.category-select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.search-input {
  flex: 1;
}

.events-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.event-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.event-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.event-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.event-info {
  padding: 1rem;
}

.event-info h3 {
  margin: 0 0 0.5rem 0;
}

.date,
.location,
.attendees {
  margin: 0.25rem 0;
  font-size: 0.9rem;
  color: #666;
}
</style>
