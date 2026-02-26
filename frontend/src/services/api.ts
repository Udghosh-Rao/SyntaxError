import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Response interceptor to handle 401 Unauthorized
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
      window.dispatchEvent(new Event('auth-expired'));
    }
    return Promise.reject(error);
  }
);

export const userApi = {
  login: (data: any) => api.post('/auth/login', data),
  register: (data: any) => api.post('/auth/register', data),
  getProfile: () => api.get('/auth/me'),
  updateProfile: (data: any) => api.put('/auth/me', data),
  getAllUsers: () => api.get('/users'),
  getUserById: (id: string) => api.get(`/users/${id}`),
  updateUser: (id: string, data: any) => api.put(`/users/${id}`, data),
  deleteUser: (id: string) => api.delete(`/users/${id}`),
  assignRole: (id: string, role: string) => api.post(`/users/${id}/role`, { role }),
};

export const eventApi = {
  getAll: (params?: any) => api.get('/events', { params }),
  getById: (id: string) => api.get(`/events/${id}`),
  create: (data: any) => api.post('/events', data),
  update: (id: string, data: any) => api.put(`/events/${id}`, data),
  delete: (id: string) => api.delete(`/events/${id}`),
  register: (id: string | number) => api.post(`/events/${id}/register`),
};

export const registrationApi = {
  getMy: () => api.get('/registrations/my'),
  create: (data: { event_id: number | string; role: string; role_details: any }) =>
    api.post('/registrations', data),
  cancel: (id: number | string) => api.put(`/registrations/${id}/cancel`),
};

export const paymentApi = {
  createOrder: (data: { event_id: number | string }) =>
    api.post('/payments/create-order', data),
};

export const adminApi = {
  getDashboard: () => api.get('/admin/dashboard'),
  getMonthlyTrend: () => api.get('/admin/monthly-trend'),
  getCityDistribution: () => api.get('/admin/city-distribution'),
  getFillRate: () => api.get('/admin/fill-rate'),
  getOrganizerPerformance: () => api.get('/admin/organizer-performance'),
  getPopularSport: () => api.get('/admin/popular-sport'),
};

export const organizerApi = {
  getDashboard: () => api.get('/organizer/dashboard'),
  getCategoryInsight: () => api.get('/organizer/category-insight'),
  toggleFeature: (id: string | number) => api.post(`/organizer/events/${id}/feature`, {}),
  getTrend: (id: string | number) => api.get(`/organizer/trend/${id}`),
};

export default api;
