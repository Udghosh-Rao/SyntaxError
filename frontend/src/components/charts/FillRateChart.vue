<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps<{
  data: Array<{
    event_id: number;
    title: string;
    organizer_name?: string;
    capacity: number;
    seats_filled: number;
    fill_rate: number;
  }>;
}>();

const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

const renderChart = () => {
  if (!chartCanvas.value || !props.data?.length) return;
  if (chartInstance) chartInstance.destroy();

  const sorted = [...props.data].sort((a, b) => b.fill_rate - a.fill_rate);
  const labels = sorted.map(d => d.title.length > 20 ? d.title.substring(0, 20) + '…' : d.title);
  const rates = sorted.map(d => d.fill_rate);
  const bgColors = rates.map(r => {
    if (r > 70) return 'rgba(0, 223, 216, 0.7)';
    if (r > 30) return 'rgba(255, 171, 0, 0.7)';
    return 'rgba(255, 85, 85, 0.7)';
  });

  chartInstance = new Chart(chartCanvas.value, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Fill Rate (%)',
        data: rates,
        backgroundColor: bgColors,
        borderRadius: 4,
        maxBarThickness: 40
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        title: { display: true, text: 'Event Fill Rates', color: 'rgba(255,255,255,0.5)', font: { size: 12 } }
      },
      scales: {
        x: { min: 0, max: 100, ticks: { color: 'rgba(255,255,255,0.5)', callback: (v: any) => v + '%' }, grid: { color: 'rgba(255,255,255,0.05)' } },
        y: { ticks: { color: 'rgba(255,255,255,0.6)', font: { size: 11 } }, grid: { display: false } }
      }
    }
  });
};

onMounted(() => renderChart());
watch(() => props.data, renderChart, { deep: true });
</script>

<style scoped>
.chart-container { position: relative; height: 300px; width: 100%; }
</style>
