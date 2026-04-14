import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '@/services/api';

const API_URL = '/events';

export const useEventsStore = defineStore('events', () => {
  const events = ref<any[]>([]);
  const selectedEvent = ref<any>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  const fetchEvents = async (filters?: any) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await api.get(API_URL, { params: filters });
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
      const response = await api.get(`${API_URL}/${id}`);
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
      const response = await api.post(API_URL, eventData);
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
      await api.delete(`${API_URL}/${id}`);
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
      await api.post('/registrations', { event_id: Number(eventId) });
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
      await api.delete(`/registrations/event/${eventId}`);
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