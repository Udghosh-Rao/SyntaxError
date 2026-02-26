import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || '/api';

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
      events.value = response.data.events || response.data;
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
      selectedEvent.value = response.data.event || response.data;
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to fetch event';
    } finally {
      isLoading.value = false;
    }
  };

  const createEvent = async (eventData: any) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await axios.post(`${API_URL}/events`, eventData);
      events.value.push(response.data);
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Failed to create event';
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const deleteEvent = async (id: string) => {
    isLoading.value = true;
    error.value = null;
    try {
      await axios.delete(`${API_URL}/events/${id}`);
      events.value = events.value.filter(e => e.id !== id);
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Failed to delete event';
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const registerForEvent = async (eventId: string | number) => {
    isLoading.value = true;
    error.value = null;
    try {
      await axios.post(`${API_URL}/registrations`, { event_id: Number(eventId) });
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Failed to register';
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const unregisterFromEvent = async (eventId: string | number) => {
    isLoading.value = true;
    error.value = null;
    try {
      await axios.delete(`${API_URL}/registrations/event/${eventId}`);
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Failed to cancel registration';
      throw err;
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
    createEvent,
    deleteEvent,
    registerForEvent,
    unregisterFromEvent,
  };
});
