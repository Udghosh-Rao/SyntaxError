<template>
  <div class="table-container">
    <h3>Event Fill Rates</h3>
    <table class="data-table">
      <thead>
        <tr>
          <th>Event ID</th>
          <th>Title</th>
          <th>Organizer</th>
          <th>Capacity</th>
          <th>Filled</th>
          <th>Fill Rate</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in sortedData" :key="item.event_id">
          <td>#{{ item.event_id }}</td>
          <td>{{ item.title }}</td>
          <td>{{ item.organizer_name }}</td>
          <td>{{ item.capacity }}</td>
          <td>{{ item.seats_filled }}</td>
          <td>
            <div class="progress-bar-container">
              <div 
                class="progress-fill" 
                :class="getPerformanceClass(item.fill_rate)"
                :style="{ width: item.fill_rate + '%' }"
              ></div>
              <span class="progress-text">{{ item.fill_rate }}%</span>
            </div>
          </td>
        </tr>
        <tr v-if="data.length === 0">
          <td colspan="6" class="text-center">No active events found.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  data: Array<{
    event_id: number;
    title: string;
    organizer_name: string;
    capacity: number;
    seats_filled: number;
    seats_remaining: number;
    fill_rate: number;
  }>;
}>();

// Sort by fill_rate descending
const sortedData = computed(() => {
  return [...props.data].sort((a, b) => b.fill_rate - a.fill_rate);
});

// Use the explicit thresholds from Spec 3.3 for styling
const getPerformanceClass = (rate: number) => {
  if (rate < 30) return 'perf-low';       // <30%
  else if (rate <= 70) return 'perf-medium';// 30-70%
  else return 'perf-high';                // >70%
};
</script>

<style scoped>
.table-container {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  margin-top: 1rem;
}

h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #333;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th, .data-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
  color: #333;
}

.data-table th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #555;
}

.progress-bar-container {
  width: 100%;
  height: 24px;
  background-color: #e9ecef;
  border-radius: 12px;
  overflow: hidden;
  position: relative;
}

.progress-fill {
  height: 100%;
  transition: width 0.5s ease;
}

.progress-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 0.8rem;
  font-weight: bold;
  color: #333;
}

.perf-low { background-color: #dc3545; }    /* Red */
.perf-medium { background-color: #ffc107; } /* Yellow */
.perf-high { background-color: #28a745; }   /* Green */

.text-center { text-align: center; color: #888; }
</style>
