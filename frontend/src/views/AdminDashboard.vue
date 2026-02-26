<template>
  <div class="min-h-screen bg-black text-white relative flex flex-col selection:bg-[#ccff00] selection:text-black">
    <!-- Cinematic Background Ambient Glow -->
    <div class="fixed inset-0 z-0 pointer-events-none">
      <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,rgba(112,0,255,0.15)_0%,transparent_50%)]"></div>
      <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom_left,rgba(0,243,255,0.1)_0%,transparent_50%)]"></div>
    </div>

    <div class="relative z-10 pt-32 pb-24 flex-1">
      <div class="container mx-auto px-6 max-w-7xl">
        
        <!-- Dashboard Header -->
        <div class="flex flex-col md:flex-row justify-between items-start md:items-end mb-16 gap-8">
          <div>
            <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-white/10 bg-white/5 backdrop-blur-2xl shadow-xl mb-6">
              <span class="text-xs font-black tracking-[0.2em] text-[#7000ff] uppercase">Platform Intelligence</span>
            </div>
            <h1 class="text-5xl md:text-7xl font-black text-white tracking-tighter leading-[0.95] mb-4 drop-shadow-2xl">
              Command <br/>
              <span class="text-transparent bg-clip-text bg-gradient-to-r from-white to-white/50">Overview.</span>
            </h1>
            <p class="text-lg text-white/50 font-medium max-w-xl leading-relaxed">
              High-level telemetry of platform operatives and architectural efficiency.
            </p>
          </div>
          
          <button @click="fetchData" :disabled="loading" class="bg-white/5 border border-white/10 hover:bg-white/10 hover:border-white/20 text-white font-bold px-8 py-4 rounded-full transition-all duration-300 backdrop-blur-xl flex items-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" :class="{'animate-spin': loading}"><path d="M23 4v6h-6"></path><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path></svg>
            Re-Sync Platform
          </button>
        </div>

        <!-- State Handling -->
        <div v-if="loading" class="py-24 flex flex-col items-center justify-center">
          <div class="w-12 h-12 border-4 border-white/10 border-t-[#7000ff] rounded-full animate-spin mb-6"></div>
          <span class="text-white/60 font-bold tracking-widest uppercase text-sm">Fetching Intelligence...</span>
        </div>
        
        <div v-else-if="error" class="bg-red-500/10 border border-red-500/20 rounded-3xl p-8 mb-12 backdrop-blur-xl flex items-center gap-4 text-red-400">
          <span class="text-2xl">⚠️</span>
          <span class="font-medium font-lg">{{ error }}</span>
        </div>
        
        <div v-else class="flex flex-col gap-8">
          <!-- Top-level Platform Stats -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div class="bg-white/5 border border-white/10 rounded-3xl p-8 backdrop-blur-2xl hover:bg-white/10 hover:border-[#7000ff]/30 transition-all duration-500 group relative overflow-hidden flex flex-col">
              <div class="absolute inset-0 bg-gradient-to-br from-[#7000ff]/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <span class="text-[0.65rem] font-black tracking-[0.2em] text-[#7000ff] uppercase mb-4 relative z-10">Total Operatives</span>
              <span class="text-5xl font-black text-white tracking-tighter relative z-10">{{ overview.total_users }}</span>
            </div>
            
            <div class="bg-white/5 border border-white/10 rounded-3xl p-8 backdrop-blur-2xl hover:bg-white/10 hover:border-[#00f3ff]/30 transition-all duration-500 group relative overflow-hidden flex flex-col">
              <div class="absolute inset-0 bg-gradient-to-br from-[#00f3ff]/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <span class="text-[0.65rem] font-black tracking-[0.2em] text-[#00f3ff] uppercase mb-4 relative z-10">Active Deployments</span>
              <span class="text-5xl font-black text-white tracking-tighter relative z-10">{{ overview.total_events }}</span>
            </div>
            
            <div class="bg-white/5 border border-white/10 rounded-3xl p-8 backdrop-blur-2xl hover:bg-white/10 hover:border-[#ff0055]/30 transition-all duration-500 group relative overflow-hidden flex flex-col">
              <div class="absolute inset-0 bg-gradient-to-br from-[#ff0055]/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <span class="text-[0.65rem] font-black tracking-[0.2em] text-[#ff0055] uppercase mb-4 relative z-10">Total Commitments</span>
              <span class="text-5xl font-black text-white tracking-tighter relative z-10">{{ overview.total_registrations }}</span>
            </div>
            
            <div class="bg-white/5 border border-white/10 rounded-3xl p-8 backdrop-blur-2xl hover:bg-white/10 hover:border-white/30 transition-all duration-500 group relative overflow-hidden flex flex-col">
              <div class="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <span class="text-[0.65rem] font-black tracking-[0.2em] text-white/60 uppercase mb-4 relative z-10">Aggregate Yield</span>
              <span class="text-4xl font-black text-white tracking-tighter relative z-10 mt-1">₹{{ overview.total_revenue?.toLocaleString() }}</span>
            </div>
          </div>

          <!-- Charts Row 1 -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Temporal Growth -->
            <div class="bg-white/5 border border-white/10 rounded-3xl p-8 backdrop-blur-2xl col-span-1 lg:col-span-2 flex flex-col">
              <h2 class="text-xs font-black tracking-[0.15em] text-white/50 uppercase mb-8">Temporal Growth Trend</h2>
              <div class="flex-1 w-full min-h-[300px]"><MonthlyTrendChart :data="monthlyTrend" /></div>
            </div>
            
            <!-- Sport Category -->
            <div class="bg-white/5 border border-white/10 rounded-3xl p-8 backdrop-blur-2xl flex flex-col">
              <h2 class="text-xs font-black tracking-[0.15em] text-white/50 uppercase mb-8">Sport Category</h2>
              <div class="flex-1 w-full min-h-[300px]"><SportDonutChart :data="popularSports" /></div>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Bio-Region Distribution -->
            <div class="bg-white/5 border border-white/10 rounded-3xl p-8 backdrop-blur-2xl flex flex-col">
              <h2 class="text-xs font-black tracking-[0.15em] text-white/50 uppercase mb-8">Bio-Region Distribution</h2>
              <div class="flex-1 w-full min-h-[300px]"><CityDistributionChart :data="cityData" /></div>
            </div>

            <!-- Event Fill Rates -->
            <div class="bg-white/5 border border-white/10 rounded-3xl p-8 backdrop-blur-2xl flex flex-col">
               <h2 class="text-xs font-black tracking-[0.15em] text-white/50 uppercase mb-8">Event Fill Rates</h2>
               <div class="flex-1 w-full min-h-[300px]"><FillRateChart :data="fillRates" /></div>
            </div>
          </div>

          <!-- Organizer Comparison Chart -->
          <div class="bg-white/5 border border-white/10 rounded-3xl p-8 backdrop-blur-2xl flex flex-col">
            <h2 class="text-xs font-black tracking-[0.15em] text-white/50 uppercase mb-8">Organizer Performance</h2>
            <div class="w-full min-h-[400px]"><OrganizerComparisonChart :data="topOrganizers" /></div>
          </div>

          <!-- Organizer Leaderboard Table -->
          <div class="bg-white/5 border border-white/10 rounded-3xl p-8 backdrop-blur-2xl overflow-hidden">
            <h2 class="text-xs font-black tracking-[0.15em] text-white/50 uppercase mb-8">Elite Architect Performance</h2>
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse">
                <thead>
                  <tr class="border-b border-white/10">
                    <th class="py-4 px-6 text-[0.65rem] font-black tracking-[0.1em] text-white/40 uppercase">Rank</th>
                    <th class="py-4 px-6 text-[0.65rem] font-black tracking-[0.1em] text-white/40 uppercase">Architect Name</th>
                    <th class="py-4 px-6 text-[0.65rem] font-black tracking-[0.1em] text-white/40 uppercase">Deployments</th>
                    <th class="py-4 px-6 text-[0.65rem] font-black tracking-[0.1em] text-white/40 uppercase">Commitments</th>
                    <th class="py-4 px-6 text-[0.65rem] font-black tracking-[0.1em] text-white/40 uppercase">Total Yield (₹)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(org, i) in topOrganizers" :key="org.organizer_id" class="border-b border-white/5 hover:bg-white/5 transition-colors">
                    <td class="py-5 px-6 font-bold text-white/40">#{{ i + 1 }}</td>
                    <td class="py-5 px-6 font-bold text-white">{{ org.organizer_name }}</td>
                    <td class="py-5 px-6 font-medium text-white/70">{{ org.total_events }}</td>
                    <td class="py-5 px-6 font-medium text-white/70">{{ org.total_registrations }}</td>
                    <td class="py-5 px-6 font-black text-[#00f3ff] tracking-tighter">₹{{ org.total_revenue.toLocaleString() }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { adminApi } from '../services/api';
import MonthlyTrendChart from '../components/charts/MonthlyTrendChart.vue';
import CityDistributionChart from '../components/charts/CityDistributionChart.vue';
import FillRateChart from '../components/charts/FillRateChart.vue';
import OrganizerComparisonChart from '../components/charts/OrganizerComparisonChart.vue';
import SportDonutChart from '../components/charts/SportDonutChart.vue';

const loading = ref(true);
const error = ref('');

// Data Refs
const overview = ref<any>({});
const monthlyTrend = ref<any[]>([]);
const cityData = ref<any[]>([]);
const fillRates = ref<any[]>([]);
const topOrganizers = ref<any[]>([]);
const popularSports = ref<any[]>([]);

const fetchData = async () => {
  loading.value = true;
  error.value = '';
  try {
    const [statsRes, trendRes, cityRes, fillRes, orgRes, popularRes] = await Promise.all([
      adminApi.getDashboard(),
      adminApi.getMonthlyTrend(),
      adminApi.getCityDistribution(),
      adminApi.getFillRate(),
      adminApi.getOrganizerPerformance(),
      adminApi.getPopularSport(),
    ]);

    overview.value = statsRes.data;
    monthlyTrend.value = trendRes.data;
    cityData.value = cityRes.data;
    fillRates.value = fillRes.data;
    topOrganizers.value = orgRes.data;
    popularSports.value = popularRes.data;

  } catch (err: any) {
    error.value = 'Failed to load admin analytics. ' + (err.response?.data?.message || '');
  } finally {
    loading.value = false;
  }
};

onMounted(() => fetchData());
</script>
