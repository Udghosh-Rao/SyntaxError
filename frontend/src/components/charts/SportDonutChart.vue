<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps<{
  data: Array<{ category: string; registrations: number }>;
}>();

const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

const isLight = () => document.documentElement.getAttribute('data-theme') === 'light';

const colors = () => ({
  legend:      isLight() ? 'rgba(15,23,42,0.9)'  : 'rgba(255,255,255,0.8)',
  legendWeight:'bold' as const,
  title:       isLight() ? 'rgba(15,23,42,0.8)'  : 'rgba(255,255,255,0.6)',
  segBorder:   isLight() ? '#f1f5f9'              : 'rgba(0,0,0,0.35)',
  segBorderW:  isLight() ? 3                      : 1,
});

const renderChart = () => {
  if (!chartCanvas.value || !props.data?.length) return;
  if (chartInstance) { chartInstance.destroy(); chartInstance = null; }

  const labels  = props.data.map((d: any) => d.sport_category || d.category);
  const values  = props.data.map((d: any) => d.registration_count ?? d.registrations);
  const palette = ['#0070f3','#00dfd8','#ff0080','#7928ca','#ffab00','#36A2EB','#FF6384','#4BC0C0'];
  const c = colors();

  chartInstance = new Chart(chartCanvas.value, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: palette.slice(0, labels.length),
        borderWidth: c.segBorderW,
        borderColor: c.segBorder,
        hoverOffset: 8,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '60%',
      plugins: {
        legend: {
          position: 'right',
          labels: { color: c.legend, font: { size: 11, weight: c.legendWeight }, padding: 12 },
        },
        title: {
          display: true,
          text: 'Sport Category Distribution',
          color: c.title,
          font: { size: 12, weight: 'bold' },
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
.chart-container { position: relative; height: 280px; width: 100%; }
</style>
