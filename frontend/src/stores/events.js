import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'

export const useEventsStore = defineStore('events', () => {
  const events = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function fetchEvents() {
    loading.value = true
    error.value = null
    try {
      const res = await api.get('/events')
      events.value = res.data
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function fetchEventById(id) {
    const res = await api.get(`/events/${id}`)
    return res.data
  }

  async function fetchSimilarEvents(id) {
    const res = await api.get(`/events/${id}/similar`)
    return res.data
  }

  async function createEvent(payload) {
    const res = await api.post('/events', payload)
    return res.data
  }

  async function updateEvent(id, payload) {
    const res = await api.put(`/events/${id}`, payload)
    return res.data
  }

  async function deleteEvent(id) {
    const res = await api.delete(`/events/${id}`)
    return res.data
  }

  return {
    events, loading, error,
    fetchEvents, fetchEventById, fetchSimilarEvents,
    createEvent, updateEvent, deleteEvent,
  }
})
