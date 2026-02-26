<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps<{
  data: Array<{ day: string; count: number }>;
}>();

const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

const renderChart = () => {
  if (!chartCanvas.value) return;
  
  if (chartInstance) {
    chartInstance.destroy();
  }

  // Generate continuous 90-day timeline
  const today = new Date();
  const timeline = Array.from({length: 90}, (_, i) => {
    const d = new Date(today);
    d.setDate(d.getDate() - (89 - i));
    return d;
  });

  const dataMap = new Map();
  props.data.forEach(d => {
    dataMap.set(new Date(d.day).toISOString().split('T')[0], d.count);
  });

  const labels = timeline.map(d => d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' }));
  const counts = timeline.map(d => {
    const key = d.toISOString().split('T')[0];
    return dataMap.get(key) || 0;
  });

  chartInstance = new Chart(chartCanvas.value, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Daily Registrations',
        data: counts,
        borderColor: '#00bcd4',
        backgroundColor: 'rgba(0, 188, 212, 0.1)',
        tension: 0.4,
        fill: true
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top', labels: { color: 'rgba(255,255,255,0.7)', font: { size: 11 } } },
        title: { display: true, text: 'Registration Trend (Last 30 Days)', color: 'rgba(255,255,255,0.5)', font: { size: 12 } }
      },
      scales: {
        x: { ticks: { color: 'rgba(255,255,255,0.5)', font: { size: 10 } }, grid: { color: 'rgba(255,255,255,0.05)' } },
        y: { beginAtZero: true, ticks: { precision: 0, color: 'rgba(255,255,255,0.5)' }, grid: { color: 'rgba(255,255,255,0.05)' } }
      }
    }
  });
};

onMounted(() => renderChart());
watch(() => props.data, renderChart, { deep: true });
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 300px;
  width: 100%;
}
</style>
