import axios from 'axios';
import type { Event, User, EventRegistration, ApiResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Event APIs
export const eventApi = {
  getAll: async (): Promise<ApiResponse<Event[]>> => {
    const response = await apiClient.get('/events');
    return response.data;
  },

  getById: async (id: number): Promise<ApiResponse<Event>> => {
    const response = await apiClient.get(`/events/${id}`);
    return response.data;
  },

  create: async (event: Partial<Event>): Promise<ApiResponse<Event>> => {
    const response = await apiClient.post('/events', event);
    return response.data;
  },

  update: async (id: number, event: Partial<Event>): Promise<ApiResponse<Event>> => {
    const response = await apiClient.put(`/events/${id}`, event);
    return response.data;
  },

  delete: async (id: number): Promise<ApiResponse<void>> => {
    const response = await apiClient.delete(`/events/${id}`);
    return response.data;
  },
};

// User APIs
export const userApi = {
  login: async (email: string, password: string): Promise<ApiResponse<{ token: string; user: User }>> => {
    const response = await apiClient.post('/auth/login', { email, password });
    return response.data;
  },

  register: async (email: string, name: string, password: string): Promise<ApiResponse<User>> => {
    const response = await apiClient.post('/auth/register', { email, name, password });
    return response.data;
  },

  getProfile: async (): Promise<ApiResponse<User>> => {
    const response = await apiClient.get('/auth/profile');
    return response.data;
  },
};

// Registration APIs
export const registrationApi = {
  register: async (eventId: number): Promise<ApiResponse<EventRegistration>> => {
    const response = await apiClient.post(`/events/${eventId}/register`);
    return response.data;
  },

  getRegistrations: async (): Promise<ApiResponse<EventRegistration[]>> => {
    const response = await apiClient.get('/registrations');
    return response.data;
  },

  cancel: async (registrationId: number): Promise<ApiResponse<void>> => {
    const response = await apiClient.delete(`/registrations/${registrationId}`);
    return response.data;
  },
};

export default apiClient;
