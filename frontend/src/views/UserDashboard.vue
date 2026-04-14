<template>
  <div class="user-dashboard-page min-h-screen pt-28 pb-16 px-4 md:px-8">
    <div class="max-w-4xl mx-auto space-y-8">
      
      <div class="dashboard-header mb-8 animate-corp flex justify-between items-end flex-wrap gap-4">
        <div>
          <span class="dash-badge bg-black/50 text-gray-400 border border-gray-800 rounded-full px-3 py-1 text-xs font-bold tracking-widest uppercase mb-3 inline-block">Insights</span>
          <h1 class="text-3xl font-black text-white headline-gradient">Referral Dashboard</h1>
          <p class="text-gray-400 text-sm mt-1">Track your referral impact and earnings.</p>
        </div>
        <div class="code-box bg-[#ccff00]/10 border border-[#ccff00]/30 px-4 py-2 rounded-xl flex items-center gap-4">
          <span class="text-xs uppercase text-[#ccff00] font-bold tracking-widest">Your Code</span>
          <span class="font-mono text-xl font-black text-white">{{ referralCode }}</span>
        </div>
      </div>

      <div v-if="loading" class="text-center text-gray-500 py-10 font-bold tracking-widest uppercase">Loading Insights...</div>
      
      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        <section class="glass-panel p-8 rounded-3xl flex flex-col justify-center items-center text-center">
          <p class="text-sm uppercase tracking-widest text-gray-400 font-bold mb-2">Total Referrals Used</p>
          <div class="text-6xl font-black text-[var(--brand-accent)]">{{ totalReferrals }}</div>
          <p class="text-xs text-gray-500 mt-4 leading-relaxed max-w-xs">Every time a user registers for an event with your code, you earn 5% of the event ticket price directly into your Wallet!</p>
        </section>

        <section class="glass-panel p-8 rounded-3xl">
          <h3 class="text-sm uppercase tracking-widest text-gray-400 font-bold mb-6">Recent Uses</h3>
          <div v-if="referrals.length === 0" class="text-center py-8 text-gray-500 text-sm">
            No one has used your code yet. Share it to start earning!
          </div>
          <ul v-else class="space-y-4 max-h-[300px] overflow-y-auto pr-2 custom-scrollbar">
            <li v-for="ref in referrals" :key="ref.id" class="flex justify-between items-center p-4 bg-black/40 rounded-xl border border-gray-800">
              <div>
                <p class="text-white font-bold text-sm">{{ ref.name }}</p>
                <p class="text-xs text-gray-500">{{ new Date(ref.joined_at).toLocaleDateString() }}</p>
              </div>
              <span class="text-[#ccff00] font-bold text-xs uppercase tracking-wider">+ Bonus</span>
            </li>
          </ul>
        </section>

      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();
const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const loading = ref(true);
const referralCode = ref('');
const totalReferrals = ref(0);
const referrals = ref<any[]>([]);

onMounted(async () => {
  try {
    const res = await axios.get(`${apiBase}/api/auth/my-referrals`, {
      headers: { Authorization: `Bearer ${authStore.token}` }
    });
    referralCode.value = res.data.referral_code;
    totalReferrals.value = res.data.total_referrals;
    referrals.value = res.data.referrals;
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
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

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255,255,255,0.05);
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255,255,255,0.2);
  border-radius: 4px;
}
</style>
