import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { userApi } from '@/services/api';

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('auth_token'));
  const role = ref<string | null>(localStorage.getItem('user_role'));
  const userId = ref<string | null>(localStorage.getItem('user_id'));
  const userObj = ref<any>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // Computed
  const isAuthenticated = computed(() => !!token.value);
  const isAdmin = computed(() => role.value === 'admin');
  const isOrganizer = computed(() => role.value === 'organizer' || role.value === 'founder');
  const isUser = computed(() => role.value === 'user');
  const isFounder = computed(() => role.value === 'founder');

  // Methods
  const register = async (userData: any) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await userApi.register(userData);
      token.value = response.data.access_token;

      // role defaults to 'user' in backend if not explicitly organizer
      const newRole = userData.role || 'user';
      role.value = newRole;
      userId.value = response.data.user_id;

      localStorage.setItem('auth_token', response.data.access_token);
      localStorage.setItem('user_role', newRole);
      if (response.data.user_id) {
        localStorage.setItem('user_id', response.data.user_id);
      }

      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Registration failed';
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const login = async (email: string, password: string) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await userApi.login({ email, password });
      token.value = response.data.access_token;
      role.value = response.data.role;

      localStorage.setItem('auth_token', response.data.access_token);
      localStorage.setItem('user_role', response.data.role);

      // Fetch profile data after login
      await fetchProfile();

      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Login failed';
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const fetchProfile = async () => {
    try {
      const res = await userApi.getProfile();
      userObj.value = res.data;
      userId.value = res.data.id;
      localStorage.setItem('user_id', res.data.id);
    } catch (err) {
      console.error("Failed to fetch profile", err);
    }
  };

  const logout = () => {
    token.value = null;
    userId.value = null;
    role.value = null;
    userObj.value = null;
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_role');
  };

  const initializeAuth = () => {
    const storedToken = localStorage.getItem('auth_token');
    if (storedToken) {
      token.value = storedToken;
      userId.value = localStorage.getItem('user_id');
      role.value = localStorage.getItem('user_role');
    }
  };

  return {
    token,
    userId,
    role,
    userObj,
    isLoading,
    error,
    isAuthenticated,
    isAdmin,
    isOrganizer,
    isUser,
    isFounder,
    register,
    login,
    fetchProfile,
    logout,
    initializeAuth,
  };
});
