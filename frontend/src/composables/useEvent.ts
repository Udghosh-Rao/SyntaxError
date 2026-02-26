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
      const { data: response } = await eventApi.getAll();
      if (response) {
        events.value = response;
      } else {
        error.value = 'Failed to fetch events';
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
      const { data: response } = await eventApi.getById(id);
      if (response) {
        selectedEvent.value = response;
      } else {
        error.value = 'Failed to fetch event';
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
      const { data: response } = await eventApi.create(eventData);
      if (response) {
        events.value.push(response);
      } else {
        error.value = 'Failed to create event';
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
      const { data: response } = await eventApi.update(id, eventData);
      if (response) {
        const index = events.value.findIndex(e => e.id === id);
        if (index !== -1) {
          events.value[index] = response;
        }
      } else {
        error.value = 'Failed to update event';
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
      const { data: response } = await eventApi.delete(id);
      if (response) {
        events.value = events.value.filter(e => e.id !== id);
      } else {
        error.value = 'Failed to delete event';
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
