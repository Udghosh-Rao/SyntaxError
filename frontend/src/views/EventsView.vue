<template>
  <div class="events-view">
    <h1>All Events</h1>
    <EventList />
  </div>
</template>

<script setup lang="ts">
import EventList from '../components/EventList.vue';
</script>

<style scoped>
.events-view {
  padding: 2rem;
}

.events-view h1 {
  margin-bottom: 2rem;
  color: #333;
}
</style>
