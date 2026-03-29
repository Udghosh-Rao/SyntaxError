<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps<{
  data: Array<{ year: number; month: number; count: number }>;
}>();

const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

const isLight = () => document.documentElement.getAttribute('data-theme') === 'light';

const colors = () => ({
  tick:        isLight() ? 'rgba(15,23,42,0.9)'    : 'rgba(255,255,255,0.75)',
  tickSize:    11,
  tickWeight:  '700' as const,
  grid:        isLight() ? 'rgba(100,116,139,0.25)' : 'rgba(255,255,255,0.1)',
  gridWidth:   1.5,
  axis:        isLight() ? 'rgba(15,23,42,0.55)'    : 'rgba(255,255,255,0.35)',
  axisWidth:   2.5,
  title:       isLight() ? 'rgba(15,23,42,0.8)'     : 'rgba(255,255,255,0.6)',
});

const renderChart = () => {
  if (!chartCanvas.value) return;
  if (chartInstance) { chartInstance.destroy(); chartInstance = null; }

  const monthNames = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const labels = props.data.map(d => `${monthNames[d.month - 1]} ${d.year}`);
  const counts = props.data.map(d => d.count);
  const c = colors();

  chartInstance = new Chart(chartCanvas.value, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Monthly Registrations',
        data: counts,
        borderColor: '#9C27B0',
        backgroundColor: 'rgba(156,39,176,0.12)',
        tension: 0.4,
        fill: true,
        pointBackgroundColor: '#9C27B0',
        borderWidth: 2.5,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        title: {
          display: true,
          text: 'Platform Monthly Registration Trend',
          color: c.title,
          font: { size: 12, weight: '700' },
        },
      },
      scales: {
        x: {
          ticks: { color: c.tick, font: { size: c.tickSize, weight: c.tickWeight } },
          grid:  { color: c.grid, lineWidth: c.gridWidth },
          border: { color: c.axis, width: c.axisWidth },
        },
        y: {
          beginAtZero: true,
          ticks: { precision: 0, color: c.tick, font: { size: c.tickSize, weight: c.tickWeight } },
          grid:  { color: c.grid, lineWidth: c.gridWidth },
          border: { color: c.axis, width: c.axisWidth },
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
