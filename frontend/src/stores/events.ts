import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

export const useEventsStore = defineStore('events', () => {
  const events = ref<any[]>([]);
  const selectedEvent = ref<any>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  const fetchEvents = async (filters?: any) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await axios.get(`${API_URL}/events`, { params: filters });
      events.value = response.data;
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to fetch events';
    } finally {
      isLoading.value = false;
    }
  };

  const getEventById = async (id: string) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await axios.get(`${API_URL}/events/${id}`);
      selectedEvent.value = response.data;
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to fetch event';
    } finally {
      isLoading.value = false;
    }
  };

  return {
    events: computed(() => events.value),
    selectedEvent: computed(() => selectedEvent.value),
    isLoading: computed(() => isLoading.value),
    error: computed(() => error.value),
    fetchEvents,
    getEventById,
  };
});
