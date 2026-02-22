<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps<{
  data: Array<{ category: string; registrations: number }>;
}>();

const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

const renderChart = () => {
  if (!chartCanvas.value || !props.data?.length) return;
  if (chartInstance) chartInstance.destroy();

  const labels = props.data.map(d => d.category);
  const values = props.data.map(d => d.registrations);
  const colors = ['#0070f3', '#00dfd8', '#ff0080', '#7928ca', '#ffab00', '#36A2EB', '#FF6384', '#4BC0C0'];

  chartInstance = new Chart(chartCanvas.value, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: colors.slice(0, labels.length),
        borderWidth: 0,
        hoverOffset: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '60%',
      plugins: {
        legend: { position: 'right', labels: { color: 'rgba(255,255,255,0.7)', font: { size: 11 }, padding: 12 } },
        title: { display: true, text: 'Sport Category Distribution', color: 'rgba(255,255,255,0.5)', font: { size: 12 } }
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
