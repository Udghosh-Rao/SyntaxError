import { ref, computed } from 'vue';
import { userApi } from '@/services/api';

interface User {
  id: string;
  username: string;
  email: string;
  firstName: string;
  lastName: string;
  avatar?: string;
  role: 'admin' | 'user';
  createdAt: string;
}

const users = ref<User[]>([]);
const selectedUser = ref<User | null>(null);
const isLoading = ref(false);
const error = ref<string | null>(null);

export const useUser = () => {
  const fetchUsers = async () => {
    isLoading.value = true;
    error.value = null;
    try {
      const { data: response } = await userApi.getAllUsers();
      if (response) {
        users.value = response;
      } else {
        error.value = 'Failed to fetch users';
      }
    } catch (err: any) {
      error.value = err.message || 'An error occurred while fetching users';
    } finally {
      isLoading.value = false;
    }
  };

  const getUserById = async (id: string) => {
    isLoading.value = true;
    error.value = null;
    try {
      const { data: response } = await userApi.getUserById(id);
      if (response) {
        selectedUser.value = response;
      } else {
        error.value = 'Failed to fetch user';
      }
    } catch (err: any) {
      error.value = err.message || 'An error occurred while fetching the user';
    } finally {
      isLoading.value = false;
    }
  };

  const updateUser = async (id: string, userData: Partial<User>) => {
    isLoading.value = true;
    error.value = null;
    try {
      const { data: response } = await userApi.updateUser(id, userData);
      if (response) {
        const index = users.value.findIndex(u => u.id === id);
        if (index !== -1) {
          users.value[index] = response;
        }
        if (selectedUser.value?.id === id) {
          selectedUser.value = response;
        }
      } else {
        error.value = 'Failed to update user';
      }
    } catch (err: any) {
      error.value = err.message || 'An error occurred while updating the user';
    } finally {
      isLoading.value = false;
    }
  };

  const deleteUser = async (id: string) => {
    isLoading.value = true;
    error.value = null;
    try {
      const { data: response } = await userApi.deleteUser(id);
      if (response) {
        users.value = users.value.filter(u => u.id !== id);
        if (selectedUser.value?.id === id) {
          selectedUser.value = null;
        }
      } else {
        error.value = 'Failed to delete user';
      }
    } catch (err: any) {
      error.value = err.message || 'An error occurred while deleting the user';
    } finally {
      isLoading.value = false;
    }
  };

  const assignRole = async (id: string, role: 'admin' | 'user') => {
    isLoading.value = true;
    error.value = null;
    try {
      const { data: response } = await userApi.assignRole(id, role);
      if (response) {
        const index = users.value.findIndex(u => u.id === id);
        if (index !== -1) {
          users.value[index].role = role;
        }
        if (selectedUser.value?.id === id) {
          selectedUser.value.role = role;
        }
      } else {
        error.value = 'Failed to assign role';
      }
    } catch (err: any) {
      error.value = err.message || 'An error occurred while assigning the role';
    } finally {
      isLoading.value = false;
    }
  };

  return {
    users: computed(() => users.value),
    selectedUser: computed(() => selectedUser.value),
    isLoading: computed(() => isLoading.value),
    error: computed(() => error.value),
    fetchUsers,
    getUserById,
    updateUser,
    deleteUser,
    assignRole,
  };
};
