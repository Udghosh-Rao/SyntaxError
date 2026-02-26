<template>
  <div class="my-registrations animate-corp">
    <header class="hero-v3 py-12">
      <div class="container text-center animate-corp">
        <span class="badge-corp">Your Dashboard</span>
        <h1 class="hero-main-title mt-4">
          My <span class="text-gradient">Registrations</span>
        </h1>
        <p class="hero-description mt-4">
          Track the status of your event commitments.
        </p>
      </div>
    </header>

    <div class="container pb-20">
      <div v-if="loading" class="loading-corp-full">
        <div class="pulse-loader mx-auto mb-6"></div>
        <span class="text-dim">Fetching your registrations...</span>
      </div>

      <div v-else-if="error" class="error-panel-inline">
        {{ error }}
      </div>

      <div v-else-if="registrations.length === 0" class="text-center py-20">
        <h3 class="label-muted mb-4">No Registrations Found</h3>
        <p class="text-dim mb-8">You haven't committed to any missions yet.</p>
        <router-link to="/home" class="btn-corp btn-corp-primary">Browse Events</router-link>
      </div>

      <div v-else class="registrations-list grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <div 
          v-for="reg in registrations" 
          :key="reg.id" 
          class="card-premium p-6 flex flex-col justify-between"
        >
          <div>
            <div class="flex justify-between items-start mb-4">
               <span class="badge-corp-small" :class="reg.status">{{ reg.status }}</span>
               <span class="text-xs font-800 text-dim tracking-widest uppercase">{{ reg.role }}</span>
            </div>
            <h3 class="text-xl font-900 mb-2">{{ reg.event?.title }}</h3>
            <p class="text-dim text-sm mb-4">
              {{ new Date(reg.event?.event_date).toLocaleDateString() }} • {{ reg.event?.venue_city }}
            </p>
            <div v-if="reg.role_details && Object.keys(reg.role_details).length" class="mt-4 p-4 rounded-lg bg-black/20 border border-white/5">
               <div v-for="(val, key) in reg.role_details" :key="key" class="text-xs text-dim mb-1">
                 <strong class="uppercase text-white/70 tracking-wider mr-2">{{ key }}:</strong> {{ val }}
               </div>
            </div>
          </div>
          
          <div class="mt-6 pt-4 border-t border-white/10 flex justify-between items-center">
            <span class="font-600 text-sm">₹{{ reg.event?.price }}</span>
            <router-link :to="`/events/${reg.event_id}`" class="text-brand text-sm font-800 hover:underline">
              View Event
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { registrationApi } from '../services/api';

const registrations = ref<any[]>([]);
const loading = ref(true);
const error = ref('');
let pollInterval: any;

const fetchRegistrations = async (isPolling = false) => {
  if (!isPolling) loading.value = true;
  try {
    const res = await registrationApi.getMy();
    registrations.value = res.data;
  } catch (err) {
    console.error(err);
    if (!isPolling) error.value = 'Failed to load registrations.';
  } finally {
    if (!isPolling) loading.value = false;
  }
};

onMounted(() => {
  fetchRegistrations();
  pollInterval = setInterval(() => {
    fetchRegistrations(true);
  }, 30000);
});

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval);
});
</script>

<style scoped>
.my-registrations {
  min-height: 100vh;
  background: var(--bg-site);
  padding-top: var(--nav-height);
}

.hero-main-title {
  font-size: 3rem;
  font-weight: 900;
  letter-spacing: -0.04em;
}

.badge-corp-small {
  padding: 0.3rem 0.6rem;
  font-size: 0.6rem;
  font-weight: 800;
  border-radius: var(--radius-pill);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.badge-corp-small.confirmed { background: rgba(0, 223, 216, 0.1); color: var(--brand-secondary); }
.badge-corp-small.pending { background: rgba(255, 171, 0, 0.1); color: #ffab00; }
.badge-corp-small.cancelled { background: rgba(255, 85, 85, 0.1); color: #ff5555; }

.loading-corp-full {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 80px 0;
}

.text-brand {
    color: var(--brand-primary);
}
</style>
