import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useUserStore = defineStore('user', () => {
  const user = ref(null);
  const isAuthenticated = computed(() => user.value !== null);

  function setUser(userData: any) {
    user.value = userData;
  }

  function setToken(token: string) {
    localStorage.setItem('auth_token', token);
  }

  function clearUser() {
    user.value = null;
    localStorage.removeItem('auth_token');
  }

  return {
    user,
    isAuthenticated,
    setUser,
    setToken,
    clearUser,
  };
});
