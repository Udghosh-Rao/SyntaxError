<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps<{ data: Array<{ category: string; registrations: number }> }>();
const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

const isLight = () => document.documentElement.getAttribute('data-theme') === 'light';

const c = () => ({
  tick:  isLight() ? 'rgba(15,23,42,0.85)'   : 'rgba(255,255,255,0.7)',
  grid:  isLight() ? 'rgba(100,116,139,0.2)'  : 'rgba(255,255,255,0.08)',
  gridW: 1.5,
  axis:  isLight() ? 'rgba(15,23,42,0.5)'     : 'rgba(255,255,255,0.3)',
  axisW: 2.5,
  title: isLight() ? 'rgba(15,23,42,0.75)'    : 'rgba(255,255,255,0.55)',
  tickW: '700' as const,
});

const renderChart = () => {
  if (!chartCanvas.value) return;
  if (chartInstance) { chartInstance.destroy(); chartInstance = null; }
  const col = c();
  chartInstance = new Chart(chartCanvas.value, {
    type: 'bar',
    data: {
      labels: props.data.map(d => d.category),
      datasets: [{ label: 'Registrations', data: props.data.map(d => d.registrations), backgroundColor: ['#FF6384','#36A2EB','#FFCE56','#4BC0C0','#9966FF','#FF9F40'], borderWidth: 0, borderRadius: 6 }],
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        title: { display: true, text: 'Registrations by Sport Category', color: col.title, font: { size: 12, weight: '700' } },
      },
      scales: {
        x: { ticks: { color: col.tick, font: { size: 10, weight: col.tickW } }, grid: { color: col.grid, lineWidth: col.gridW }, border: { color: col.axis, width: col.axisW } },
        y: { beginAtZero: true, ticks: { precision: 0, color: col.tick, font: { weight: col.tickW } }, grid: { color: col.grid, lineWidth: col.gridW }, border: { color: col.axis, width: col.axisW } },
      },
    },
  });
};

const observer = new MutationObserver(renderChart);
onMounted(() => { renderChart(); observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] }); });
onUnmounted(() => { observer.disconnect(); chartInstance?.destroy(); });
watch(() => props.data, renderChart, { deep: true });
</script>

<style scoped>
.chart-container { position: relative; height: 300px; width: 100%; }
</style>
