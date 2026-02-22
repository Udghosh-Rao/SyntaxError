<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps<{
  data: Array<{ organizer_name: string; total_revenue: number; total_registrations: number; total_events: number }>;
}>();

const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

const renderChart = () => {
  if (!chartCanvas.value || !props.data?.length) return;
  if (chartInstance) chartInstance.destroy();

  const labels = props.data.map(d => d.organizer_name);
  const revenue = props.data.map(d => d.total_revenue);
  const regs = props.data.map(d => d.total_registrations);

  chartInstance = new Chart(chartCanvas.value, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: 'Revenue (₹)',
          data: revenue,
          backgroundColor: 'rgba(0, 112, 243, 0.7)',
          borderColor: '#0070f3',
          borderWidth: 1,
          yAxisID: 'y'
        },
        {
          label: 'Registrations',
          data: regs,
          backgroundColor: 'rgba(0, 223, 216, 0.7)',
          borderColor: '#00dfd8',
          borderWidth: 1,
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top', labels: { color: 'rgba(255,255,255,0.7)', font: { size: 11 } } },
        title: { display: true, text: 'Organizer Performance Comparison', color: 'rgba(255,255,255,0.5)', font: { size: 12 } }
      },
      scales: {
        x: { ticks: { color: 'rgba(255,255,255,0.5)', font: { size: 10 } }, grid: { color: 'rgba(255,255,255,0.05)' } },
        y: { type: 'linear', position: 'left', ticks: { color: 'rgba(255,255,255,0.5)' }, grid: { color: 'rgba(255,255,255,0.05)' }, title: { display: true, text: 'Revenue (₹)', color: 'rgba(255,255,255,0.4)' } },
        y1: { type: 'linear', position: 'right', ticks: { color: 'rgba(255,255,255,0.5)' }, grid: { drawOnChartArea: false }, title: { display: true, text: 'Registrations', color: 'rgba(255,255,255,0.4)' } }
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
