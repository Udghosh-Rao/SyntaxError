<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps<{
  data: Array<{ title: string; revenue: number }>;
}>();

const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

const renderChart = () => {
  if (!chartCanvas.value || !props.data?.length) return;
  if (chartInstance) chartInstance.destroy();

  const labels = props.data.map(d => d.title.length > 18 ? d.title.substring(0, 18) + '…' : d.title);
  const values = props.data.map(d => d.revenue);
  const colors = ['#0070f3', '#00dfd8', '#ff0080', '#7928ca', '#ffab00', '#36A2EB'];

  chartInstance = new Chart(chartCanvas.value, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Revenue (₹)',
        data: values,
        backgroundColor: values.map((_, i) => colors[i % colors.length] + 'B3'),
        borderColor: values.map((_, i) => colors[i % colors.length]),
        borderWidth: 1,
        borderRadius: 6
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        title: { display: true, text: 'Revenue per Event', color: 'rgba(255,255,255,0.5)', font: { size: 12 } }
      },
      scales: {
        x: { beginAtZero: true, ticks: { color: 'rgba(255,255,255,0.5)', callback: (v: any) => '₹' + v.toLocaleString() }, grid: { color: 'rgba(255,255,255,0.05)' } },
        y: { ticks: { color: 'rgba(255,255,255,0.6)', font: { size: 11 } }, grid: { display: false } }
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
