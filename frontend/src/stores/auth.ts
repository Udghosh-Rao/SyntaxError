import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('auth_token'));
  const userId = ref<string | null>(localStorage.getItem('user_id'));
  const role = ref<string | null>(localStorage.getItem('user_role'));
  const user = ref<any>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // Computed
  const isAuthenticated = computed(() => !!token.value);
  const isAdmin = computed(() => role.value === 'admin');
  const isOrganizer = computed(() => role.value === 'organizer');

  // Methods
  const register = async (userData: any) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await axios.post(`${API_URL}/register`, userData);
      token.value = response.data.accessToken;
      userId.value = response.data.userId;
      localStorage.setItem('auth_token', response.data.accessToken);
      localStorage.setItem('user_id', response.data.userId);
      axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.accessToken}`;
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Registration failed';
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const login = async (email: string, password: string) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await axios.post(`${API_URL}/login`, { email, password });
      token.value = response.data.accessToken;
      userId.value = response.data.userId;
      role.value = response.data.role;
      localStorage.setItem('auth_token', response.data.accessToken);
      localStorage.setItem('user_id', response.data.userId);
      localStorage.setItem('user_role', response.data.role);
      axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.accessToken}`;
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Login failed';
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const logout = () => {
    token.value = null;
    userId.value = null;
    role.value = null;
    user.value = null;
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_role');
    delete axios.defaults.headers.common['Authorization'];
  };

  const initializeAuth = () => {
    const storedToken = localStorage.getItem('auth_token');
    if (storedToken) {
      token.value = storedToken;
      userId.value = localStorage.getItem('user_id');
      role.value = localStorage.getItem('user_role');
      axios.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`;
    }
  };

  return {
    token,
    userId,
    role,
    user,
    isLoading,
    error,
    isAuthenticated,
    isAdmin,
    isOrganizer,
    register,
    login,
    logout,
    initializeAuth,
  };
});
