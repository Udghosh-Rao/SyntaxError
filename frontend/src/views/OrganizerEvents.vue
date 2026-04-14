<template>
  <div class="organizer-events-page pt-28 pb-16 px-4 md:px-8">
    <div class="max-w-7xl mx-auto space-y-8">
      
      <div class="dashboard-header mb-8 animate-corp flex justify-between items-end flex-wrap gap-4">
        <div>
          <span class="dash-badge bg-black/50 text-gray-400 border border-gray-800 rounded-full px-3 py-1 text-xs font-bold tracking-widest uppercase mb-3 inline-block">Management</span>
          <h1 class="text-3xl font-black text-white headline-gradient">Your Events</h1>
          <p class="text-gray-400 text-sm mt-1">Manage and edit your active events.</p>
        </div>
        <router-link to="/organizer/create" class="save-btn flex items-center gap-2">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          Create Event
        </router-link>
      </div>

      <div v-if="loading" class="text-center text-gray-500 py-10 font-bold tracking-widest uppercase">Loading events...</div>
      <div v-else-if="error" class="bg-red-900/20 text-red-400 p-4 rounded-xl border border-red-900/50">{{ error }}</div>
      
      <section v-else class="glass-panel p-6 rounded-3xl overflow-hidden">
        <div class="table-scroll overflow-x-auto w-full">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="text-xs uppercase tracking-widest text-gray-500 border-b border-gray-800">
                <th class="p-4 font-bold">Event</th>
                <th class="p-4 font-bold">Date</th>
                <th class="p-4 font-bold">City</th>
                <th class="p-4 font-bold">Registrations</th>
                <th class="p-4 font-bold">Capacity</th>
                <th class="p-4 font-bold">Revenue (₹)</th>
                <th class="p-4 font-bold">Status</th>
                <th class="p-4 font-bold">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="event in events" :key="event.event_id" class="border-b border-gray-800/50 hover:bg-gray-800/20 transition-colors">
                <td class="p-4 font-bold text-white">{{ event.title }}</td>
                <td class="p-4 text-gray-400">{{ new Date(event.event_date).toLocaleDateString('en-GB') }}</td>
                <td class="p-4 text-gray-400">{{ event.venue_city }}</td>
                <td class="p-4 text-gray-400">{{ event.registrations }}</td>
                <td class="p-4 text-gray-400">{{ event.capacity }}</td>
                <td class="p-4 text-[var(--brand-accent)] font-black">{{ event.revenue }}</td>
                <td class="p-4">
                  <span class="perf-badge" :class="'perf-badge--' + event.performance_label.toLowerCase()">
                    {{ event.performance_label }}
                  </span>
                </td>
                <td class="p-4">
                  <button @click="router.push('/organizer/edit/' + event.event_id)" 
                          class="bg-[rgba(0,184,204,0.1)] text-[#00b8cc] border border-[rgba(0,184,204,0.3)] px-3 py-1 rounded text-xs font-bold hover:bg-[rgba(0,184,204,0.2)]"
                  >Edit</button>
                </td>
              </tr>
              <tr v-if="events.length === 0">
                <td colspan="8" class="p-8 text-center text-gray-500 font-bold uppercase tracking-widest">No active events found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { organizerApi } from '../services/api';

const router = useRouter();
const loading = ref(true);
const error = ref('');
const events = ref<any[]>([]);

const fetchEvents = async () => {
  loading.value = true;
  error.value = '';
  try {
    const res = await organizerApi.getDashboard();
    events.value = res.data;
  } catch (err) {
    error.value = 'Failed to load events data.';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchEvents();
});
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

.perf-badge {
  display: inline-flex;
  padding: 0.3rem 0.7rem;
  border-radius: 9999px;
  font-size: 0.62rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.perf-badge--high, .perf-badge.high { background: rgba(0,223,216,0.12); color: #00dfd8; }
.perf-badge--medium, .perf-badge.medium { background: rgba(255,171,0,0.12); color: #ffab00; }
.perf-badge--low, .perf-badge.low { background: rgba(255,85,85,0.12); color: #ff5555; }

.save-btn {
  background: var(--brand-accent);
  color: #000;
  font-weight: 800;
  padding: 0.8rem 1.5rem;
  border-radius: 9999px;
  transition: all 0.2s ease;
}
.save-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 243, 255, 0.3);
}
</style>
