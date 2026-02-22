<template>
  <div class="user-profile">
    <div class="profile-header">
      <div class="avatar-section">
        <img :src="user.avatar" :alt="user.name" class="avatar" />
        <div class="profile-info">
          <h2 class="user-name">{{ user.name }}</h2>
          <p class="user-email">{{ user.email }}</p>
          <p class="user-bio">{{ user.bio }}</p>
          <div class="profile-stats">
            <div class="stat">
              <span class="stat-value">{{ user.eventsAttended }}</span>
              <span class="stat-label">Events Attended</span>
            </div>
            <div class="stat">
              <span class="stat-value">{{ user.eventsOrganized }}</span>
              <span class="stat-label">Events Organized</span>
            </div>
            <div class="stat">
              <span class="stat-value">{{ user.followers }}</span>
              <span class="stat-label">Followers</span>
            </div>
          </div>
        </div>
      </div>
      <button v-if="isOwnProfile" class="btn-edit" @click="editMode = !editMode">
        {{ editMode ? 'Cancel' : 'Edit Profile' }}
      </button>
      <button v-else class="btn-follow">Follow</button>
    </div>

    <div class="profile-tabs">
      <div class="tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab" 
          :class="['tab', { active: activeTab === tab }]"
          @click="activeTab = tab"
        >
          {{ tab }}
        </button>
      </div>
    </div>

    <div class="tab-content">
      <div v-if="activeTab === 'About'" class="about-section">
        <div class="about-item">
          <h4>Bio</h4>
          <p>{{ user.bio }}</p>
        </div>
        <div class="about-item">
          <h4>Location</h4>
          <p>{{ user.location }}</p>
        </div>
        <div class="about-item">
          <h4>Joined</h4>
          <p>{{ formatDate(user.joinedDate) }}</p>
        </div>
      </div>

      <div v-if="activeTab === 'Events'" class="events-section">
        <div class="event-list">
          <div v-for="event in user.events" :key="event.id" class="event-item">
            <h4>{{ event.title }}</h4>
            <p>{{ event.date }}</p>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'Badges'" class="badges-section">
        <div class="badge-grid">
          <div v-for="badge in user.badges" :key="badge.id" class="badge">
            <span class="badge-icon">{{ badge.icon }}</span>
            <span class="badge-name">{{ badge.name }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

interface User {
  id: string;
  name: string;
  email: string;
  avatar: string;
  bio: string;
  location: string;
  joinedDate: string;
  eventsAttended: number;
  eventsOrganized: number;
  followers: number;
  events: any[];
  badges: any[];
}

const props = defineProps<{
  user: User;
  isOwnProfile: boolean;
}>();

const editMode = ref(false);
const activeTab = ref('About');
const tabs = ['About', 'Events', 'Badges'];

const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
};
</script>

<style scoped>
.user-profile {
  background: white;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.profile-header {
  padding: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.avatar-section {
  display: flex;
  gap: 2rem;
  flex: 1;
}

.avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 4px solid white;
  object-fit: cover;
}

.profile-info {
  flex: 1;
}

.user-name {
  font-size: 2rem;
  margin: 0 0 0.5rem 0;
  font-weight: bold;
}

.user-email {
  margin: 0 0 0.5rem 0;
  opacity: 0.9;
}

.user-bio {
  margin: 0 0 1.5rem 0;
  font-size: 0.95rem;
}

.profile-stats {
  display: flex;
  gap: 2rem;
}

.stat {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
}

.stat-label {
  font-size: 0.875rem;
  opacity: 0.9;
}

.btn-edit,
.btn-follow {
  padding: 0.5rem 1.5rem;
  border-radius: 0.375rem;
  border: 2px solid white;
  color: white;
  background: transparent;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-edit:hover,
.btn-follow:hover {
  background: white;
  color: #667eea;
}

.profile-tabs {
  border-bottom: 1px solid #e5e7eb;
  padding: 0 2rem;
}

.tabs {
  display: flex;
  gap: 0;
}

.tab {
  padding: 1rem 1.5rem;
  border: none;
  background: none;
  font-weight: 500;
  cursor: pointer;
  color: #6b7280;
  border-bottom: 3px solid transparent;
  transition: all 0.3s;
}

.tab:hover {
  color: #1f2937;
}

.tab.active {
  color: #667eea;
  border-bottom-color: #667eea;
}

.tab-content {
  padding: 2rem;
}

.about-section,
.events-section,
.badges-section {
  animation: fadeIn 0.3s ease;
}

.about-item {
  margin-bottom: 1.5rem;
}

.about-item h4 {
  color: #1f2937;
  margin: 0 0 0.5rem 0;
}

.about-item p {
  color: #6b7280;
  margin: 0;
}

.event-list {
  display: grid;
  gap: 1rem;
}

.event-item {
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
}

.event-item h4 {
  margin: 0 0 0.5rem 0;
  color: #1f2937;
}

.event-item p {
  margin: 0;
  color: #6b7280;
  font-size: 0.875rem;
}

.badge-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 1rem;
}

.badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.375rem;
  text-align: center;
  transition: all 0.3s;
}

.badge:hover {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.badge-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.badge-name {
  font-size: 0.875rem;
  font-weight: 500;
  color: #1f2937;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>
