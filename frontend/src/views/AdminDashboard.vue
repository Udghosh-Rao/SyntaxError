<template>
  <div class="admin-dashboard">
    <h1>Admin Dashboard</h1>
    <div class="admin-container">
      <div class="controls">
        <input v-model="searchQuery" type="text" placeholder="Search users or events..." class="search-input">
        <select v-model="filterType" class="filter-select">
          <option value="all">All</option>
          <option value="users">Users</option>
          <option value="events">Events</option>
          <option value="payments">Payments</option>
        </select>
      </div>
      <div class="stats-grid">
        <div class="stat-box">
          <h3>Total Users</h3>
          <p class="stat-value">{{ totalUsers }}</p>
        </div>
        <div class="stat-box">
          <h3>Total Events</h3>
          <p class="stat-value">{{ totalEvents }}</p>
        </div>
        <div class="stat-box">
          <h3>Total Revenue</h3>
          <p class="stat-value">₹{{ totalRevenue }}</p>
        </div>
        <div class="stat-box">
          <h3>Pending Approvals</h3>
          <p class="stat-value">{{ pendingApprovals }}</p>
        </div>
      </div>
      <div class="users-section">
        <h2>User Management</h2>
        <table class="admin-table">
          <thead>
            <tr>
              <th>User ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in filteredUsers" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.name }}</td>
              <td>{{ user.email }}</td>
              <td><span class="badge" :class="user.role">{{ user.role }}</span></td>
              <td><span class="badge" :class="user.status">{{ user.status }}</span></td>
              <td>
                <button @click="viewUserDetails(user)" class="btn-small">View</button>
                <button @click="deactivateUser(user.id)" class="btn-small btn-danger">Deactivate</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="payments-section">
        <h2>Payment Transactions</h2>
        <table class="admin-table">
          <thead>
            <tr>
              <th>Transaction ID</th>
              <th>User</th>
              <th>Event</th>
              <th>Amount</th>
              <th>Status</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="payment in payments" :key="payment.id">
              <td>{{ payment.id }}</td>
              <td>{{ payment.userId }}</td>
              <td>{{ payment.eventId }}</td>
              <td>₹{{ payment.amount }}</td>
              <td><span class="badge" :class="payment.status">{{ payment.status }}</span></td>
              <td>{{ formatDate(payment.date) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();
const searchQuery = ref('');
const filterType = ref('all');
const users = ref<any[]>([]);
const payments = ref<any[]>([]);

const totalUsers = computed(() => users.value.length);
const totalEvents = computed(() => 0);
const totalRevenue = computed(() => payments.value.reduce((sum, p) => sum + p.amount, 0));
const pendingApprovals = computed(() => users.value.filter(u => u.status === 'pending').length);

const filteredUsers = computed(() => {
  return users.value.filter(u => 
    u.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    u.email.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString();
};

const viewUserDetails = (user: any) => {
  console.log('View user:', user);
};

const deactivateUser = async (userId: string) => {
  if (confirm('Are you sure you want to deactivate this user?')) {
    try {
      const index = users.value.findIndex(u => u.id === userId);
      if (index > -1) {
        users.value[index].status = 'deactivated';
      }
    } catch (error) {
      console.error('Failed to deactivate user:', error);
    }
  }
};

onMounted(() => {
  if (!authStore.isAuthenticated || authStore.currentUser?.role !== 'admin') {
    router.push({ name: 'Home' });
  }
});
</script>

<style scoped>
.admin-dashboard {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.admin-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.search-input,
.filter-select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.search-input {
  flex: 1;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-box {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  margin: 0.5rem 0 0 0;
}

.admin-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.admin-table th {
  background: #f5f5f5;
  padding: 1rem;
  text-align: left;
  font-weight: bold;
  border-bottom: 2px solid #ddd;
}

.admin-table td {
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: bold;
}

.badge.admin {
  background: #e3f2fd;
  color: #1976d2;
}

.badge.organizer {
  background: #f3e5f5;
  color: #7b1fa2;
}

.badge.user {
  background: #e8f5e9;
  color: #388e3c;
}

.badge.active {
  background: #c8e6c9;
  color: #2e7d32;
}

.badge.pending {
  background: #fff3e0;
  color: #e65100;
}

.badge.completed,
.badge.success {
  background: #c8e6c9;
  color: #2e7d32;
}

.badge.failed,
.badge.cancelled {
  background: #ffcdd2;
  color: #c62828;
}

.btn-small {
  padding: 0.4rem 0.8rem;
  margin-right: 0.5rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
}

.btn-small.btn-danger {
  background: #dc3545;
}

.btn-small:hover {
  opacity: 0.8;
}
</style>
