<template>
  <div class="profile-page min-h-screen pt-28 pb-16 px-4 md:px-8">
    <div class="max-w-3xl mx-auto space-y-8">
      
      <!-- Header Section -->
      <section class="glass-panel p-8 rounded-3xl flex flex-col items-center gap-4 text-center">
        <h1 class="text-3xl font-black tracking-tight headline-gradient">Your Profile</h1>
        <p class="text-gray-400 text-sm">Manage your personal details and avatar.</p>
        
        <div class="relative group mt-4">
          <div class="avatar-circle overflow-hidden w-32 h-32 rounded-full border-4 border-[var(--brand-accent)] bg-gray-800 flex items-center justify-center cursor-pointer relative"
               @click="$refs.avatarInput.click()">
            <img v-if="userObj.avatar_url" :src="apiBase + userObj.avatar_url" alt="Avatar" class="w-full h-full object-cover" />
            <span v-else class="text-4xl font-black text-white">{{ userObj?.name?.[0]?.toUpperCase() || 'U' }}</span>
            <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity flex-col gap-1">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line>
              </svg>
              <span class="text-xs text-white font-bold">Upload</span>
            </div>
          </div>
          <input type="file" ref="avatarInput" class="hidden" accept="image/*" @change="handleAvatarUpload" />
        </div>
      </section>

      <!-- Edit Form -->
      <section class="glass-panel p-8 rounded-3xl space-y-6">
        <h2 class="text-xl font-bold text-white mb-6">Personal Details</h2>
        
        <form @submit.prevent="saveProfile" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="form-group">
              <label class="block text-sm font-semibold text-gray-300 mb-2">Name</label>
              <input v-model="formData.name" type="text" class="custom-input w-full" required />
            </div>
            <div class="form-group">
              <label class="block text-sm font-semibold text-gray-300 mb-2">City</label>
              <input v-model="formData.city" type="text" class="custom-input w-full" required />
            </div>
          </div>
          
          <!-- Read only details -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 opacity-70">
            <div class="form-group">
              <label class="block text-sm font-semibold text-gray-300 mb-2">Email Address</label>
              <input v-model="userObj.email" type="email" class="custom-input w-full" disabled />
            </div>
            <div class="form-group">
              <label class="block text-sm font-semibold text-gray-300 mb-2">Referral Code</label>
              <input v-model="userObj.referral_code" type="text" class="custom-input w-full" disabled />
            </div>
          </div>

          <div class="pt-4 flex justify-end">
            <button type="submit" class="save-btn" :disabled="isSaving">
              <span v-if="isSaving">Saving...</span>
              <span v-else>Save Changes</span>
            </button>
          </div>
        </form>
      </section>
      
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();
const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:5000';
const userObj = ref({
  name: '',
  city: '',
  email: '',
  referral_code: '',
  avatar_url: ''
});

const formData = ref({
  name: '',
  city: ''
});

const isSaving = ref(false);
const avatarInput = ref<HTMLInputElement | null>(null);

onMounted(async () => {
  await authStore.fetchProfile();
  if (authStore.userObj) {
    userObj.value = { ...authStore.userObj };
    formData.value.name = authStore.userObj.name || '';
    formData.value.city = authStore.userObj.city || '';
  }
});

const handleAvatarUpload = async (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0];
  if (!file) return;

  const data = new FormData();
  data.append('avatar', file);

  try {
    const res = await fetch(`${apiBase}/api/auth/me/avatar`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      },
      body: data
    });
    if (res.ok) {
      const updatedUser = await res.json();
      authStore.userObj = updatedUser;
      userObj.value = { ...updatedUser };
      alert('Avatar uploaded successfully!');
    } else {
      const err = await res.json();
      alert(`Upload failed: ${err.message}`);
    }
  } catch (error) {
    console.error(error);
    alert('An error occurred during upload.');
  }
};

const saveProfile = async () => {
  isSaving.value = true;
  try {
    const res = await fetch(`${apiBase}/api/auth/me`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authStore.token}`
      },
      body: JSON.stringify(formData.value)
    });
    
    if (res.ok) {
      const updatedUser = await res.json();
      authStore.userObj = updatedUser;
      alert('Profile updated successfully!');
    } else {
      alert('Failed to update profile.');
    }
  } catch (error) {
    console.error(error);
  } finally {
    isSaving.value = false;
  }
};
</script>

<style scoped>
.glass-panel {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
}
[data-theme="light"] .glass-panel {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
}

.headline-gradient {
  background: linear-gradient(135deg, #fff 0%, #a1a1aa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
[data-theme="light"] .headline-gradient {
  background: linear-gradient(135deg, #000 0%, #4b5563 100%);
}

.custom-input {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
  padding: 0.8rem 1.2rem;
  border-radius: 12px;
  outline: none;
  transition: all 0.2s ease;
}
.custom-input:focus {
  border-color: var(--brand-accent);
  box-shadow: 0 0 0 2px rgba(0, 243, 255, 0.15);
}
[data-theme="light"] .custom-input {
  background: #f8fafc;
  border-color: #e2e8f0;
  color: #000;
}

.save-btn {
  background: var(--brand-accent);
  color: #000;
  font-weight: 800;
  padding: 0.8rem 2rem;
  border-radius: 999px;
  transition: all 0.2s ease;
}
.save-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 243, 255, 0.3);
}
.save-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>
