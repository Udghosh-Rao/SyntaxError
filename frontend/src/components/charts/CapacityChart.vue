<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps<{
  data: Array<{ title: string; registrations: number; capacity: number; fill_rate?: number }>;
}>();

const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

const renderChart = () => {
  if (!chartCanvas.value || !props.data?.length) return;
  if (chartInstance) chartInstance.destroy();

  const labels = props.data.map(d => d.title.length > 18 ? d.title.substring(0, 18) + '…' : d.title);
  const capacities = props.data.map(d => d.capacity);
  const regs = props.data.map(d => d.registrations);

  chartInstance = new Chart(chartCanvas.value, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: 'Capacity',
          data: capacities,
          backgroundColor: 'rgba(255, 255, 255, 0.08)',
          borderColor: 'rgba(255, 255, 255, 0.2)',
          borderWidth: 1,
          borderRadius: 4
        },
        {
          label: 'Registered',
          data: regs,
          backgroundColor: regs.map((r, i) => {
            const rate = capacities[i] > 0 ? (r / capacities[i]) * 100 : 0;
            if (rate > 70) return 'rgba(0, 223, 216, 0.7)';
            if (rate > 30) return 'rgba(255, 171, 0, 0.7)';
            return 'rgba(255, 85, 85, 0.7)';
          }),
          borderRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top', labels: { color: 'rgba(255,255,255,0.6)', font: { size: 11 } } },
        title: { display: true, text: 'Capacity vs Registrations', color: 'rgba(255,255,255,0.5)', font: { size: 12 } }
      },
      scales: {
        x: { ticks: { color: 'rgba(255,255,255,0.5)', font: { size: 10 } }, grid: { color: 'rgba(255,255,255,0.05)' } },
        y: { beginAtZero: true, ticks: { color: 'rgba(255,255,255,0.5)', precision: 0 }, grid: { color: 'rgba(255,255,255,0.05)' } }
      }
    }
  });
};

onMounted(() => renderChart());
watch(() => props.data, renderChart, { deep: true });
</script>

<style scoped>
.chart-container { position: relative; height: 280px; width: 100%; }
</style>
