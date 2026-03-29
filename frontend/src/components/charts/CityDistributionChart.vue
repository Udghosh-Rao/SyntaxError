<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps<{
  data: Array<{ city: string; user_count: number }>;
}>();

const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

const isLight = () => document.documentElement.getAttribute('data-theme') === 'light';

const colors = () => ({
  legend:      isLight() ? 'rgba(15,23,42,0.9)'  : 'rgba(255,255,255,0.8)',
  legendWeight:'700' as const,
  title:       isLight() ? 'rgba(15,23,42,0.8)'  : 'rgba(255,255,255,0.6)',
  segBorder:   isLight() ? '#f1f5f9'              : 'rgba(0,0,0,0.4)',
  segBorderW:  isLight() ? 3                      : 1,
});

const renderChart = () => {
  if (!chartCanvas.value) return;
  if (chartInstance) { chartInstance.destroy(); chartInstance = null; }

  const labels = props.data.map(d => d.city);
  const counts = props.data.map(d => d.user_count);
  const c = colors();

  chartInstance = new Chart(chartCanvas.value, {
    type: 'pie',
    data: {
      labels,
      datasets: [{
        data: counts,
        backgroundColor: ['#FF6384','#36A2EB','#FFCE56','#4BC0C0','#9966FF','#FF9F40'],
        borderWidth: c.segBorderW,
        borderColor: c.segBorder,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          labels: { color: c.legend, font: { size: 11, weight: c.legendWeight }, padding: 12 },
        },
        title: {
          display: true,
          text: 'User City Distribution',
          color: c.title,
          font: { size: 12, weight: '700' },
        },
      },
    },
  });
};

const observer = new MutationObserver(renderChart);

onMounted(() => {
  renderChart();
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
});

onUnmounted(() => { observer.disconnect(); chartInstance?.destroy(); });
watch(() => props.data, renderChart, { deep: true });
</script>

<style scoped>
.chart-container { position: relative; height: 300px; width: 100%; }
</style>
