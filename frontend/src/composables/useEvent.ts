import { ref, computed } from 'vue';
import { eventApi } from '@/services/api';

interface Event {
  id: string;
  title: string;
  description: string;
  date: string;
  location: string;
  attendees: number;
}

const events = ref<Event[]>([]);
const selectedEvent = ref<Event | null>(null);
const isLoading = ref(false);
const error = ref<string | null>(null);

export const useEvent = () => {
  const fetchEvents = async () => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await eventApi.getEvents();
      if (response.success) {
        events.value = response.data;
      } else {
        error.value = response.error || 'Failed to fetch events';
      }
    } catch (err: any) {
      error.value = err.message || 'An error occurred while fetching events';
    } finally {
      isLoading.value = false;
    }
  };

  const getEventById = async (id: string) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await eventApi.getEventById(id);
      if (response.success) {
        selectedEvent.value = response.data;
      } else {
        error.value = response.error || 'Failed to fetch event';
      }
    } catch (err: any) {
      error.value = err.message || 'An error occurred while fetching the event';
    } finally {
      isLoading.value = false;
    }
  };

  const createEvent = async (eventData: Omit<Event, 'id'>) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await eventApi.createEvent(eventData);
      if (response.success) {
        events.value.push(response.data);
      } else {
        error.value = response.error || 'Failed to create event';
      }
    } catch (err: any) {
      error.value = err.message || 'An error occurred while creating the event';
    } finally {
      isLoading.value = false;
    }
  };

  const updateEvent = async (id: string, eventData: Partial<Event>) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await eventApi.updateEvent(id, eventData);
      if (response.success) {
        const index = events.value.findIndex(e => e.id === id);
        if (index !== -1) {
          events.value[index] = response.data;
        }
      } else {
        error.value = response.error || 'Failed to update event';
      }
    } catch (err: any) {
      error.value = err.message || 'An error occurred while updating the event';
    } finally {
      isLoading.value = false;
    }
  };

  const deleteEvent = async (id: string) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await eventApi.deleteEvent(id);
      if (response.success) {
        events.value = events.value.filter(e => e.id !== id);
      } else {
        error.value = response.error || 'Failed to delete event';
      }
    } catch (err: any) {
      error.value = err.message || 'An error occurred while deleting the event';
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
    updateEvent,
    deleteEvent,
  };
};
