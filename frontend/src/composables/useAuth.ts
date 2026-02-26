import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { userApi } from '@/services/api';

interface User {
  value: string | null;
}

// ApiResponse interface removed

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
      const { data: response } = await userApi.login({
        username,
        password,
      });
      // Backend returns { access_token, role }
      if (response.access_token) {
        user.value = { value: response.role }; // or actual user data if available
        localStorage.setItem('auth_token', response.access_token);
        router.push(response.role === 'admin' ? '/admin' : (response.role === 'organizer' ? '/organizer' : '/home'));
      } else {
        error.value = 'Login failed';
      }
    } catch (err: any) {
      error.value = err.response?.data?.message || err.message || 'An error occurred during login';
    } finally {
      isLoading.value = false;
    }
  };

  const register = async (userData: any) => {
    isLoading.value = true;
    error.value = null;
    try {
      const { data: response } = await userApi.register(userData);
      if (response.access_token) {
        user.value = { value: response.role || 'user' };
        localStorage.setItem('auth_token', response.access_token);
        router.push('/home');
      } else {
        error.value = 'Registration failed';
      }
    } catch (err: any) {
      error.value = err.response?.data?.message || err.message || 'An error occurred during registration';
    } finally {
      isLoading.value = false;
    }
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    user.value = { value: null };
    router.push('/login');
  };

  const initAuth = async () => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      try {
        const { data: response } = await userApi.getProfile();
        if (response) {
          user.value = { value: response.role || 'user' };
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
