import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { userApi } from '@/services/api';

interface User {
  value: string | null;
}

interface ApiResponse {
  success: boolean;
  data?: any;
}

const user = ref<User>({
  value: null,
});

const isAuthenticated = computed(() => !!user.value?.value);
const isLoading = ref(false);
const error = ref<string | null>(null);

export const useAuth = () => {
  const router = useRouter();

  const login = async (username: string, password: string) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await userApi.login({
        username,
        password,
      });
      if (response.success) {
        user.value = response.data;
        localStorage.setItem('auth_token', response.data.token);
        router.push('/dashboard');
      } else {
        error.value = response.error || 'Login failed';
      }
    } catch (err: any) {
      error.value = err.message || 'An error occurred during login';
    } finally {
      isLoading.value = false;
    }
  };

  const register = async (userData: any) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await userApi.register(userData);
      if (response.success) {
        user.value = response.data;
        localStorage.setItem('auth_token', response.data.token);
        router.push('/dashboard');
      } else {
        error.value = response.error || 'Registration failed';
      }
    } catch (err: any) {
      error.value = err.message || 'An error occurred during registration';
    } finally {
      isLoading.value = false;
    }
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    user.value = null;
    router.push('/login');
  };

  const initAuth = async () => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      try {
        const response = await userApi.getProfile();
        if (response.success && response.data) {
          user.value = response.data;
        } else {
          logout();
        }
      } catch (err) {
        logout();
      }
    }
  };

  return {
    user: computed(() => user.value),
    isAuthenticated,
    isLoading: computed(() => isLoading.value),
    error: computed(() => error.value),
    login,
    register,
    logout,
    initAuth,
  };
};
