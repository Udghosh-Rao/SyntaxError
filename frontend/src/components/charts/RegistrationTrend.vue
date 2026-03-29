<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps<{ data: Array<{ day: string; count: number }> }>();
const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

const isLight = () => document.documentElement.getAttribute('data-theme') === 'light';

const c = () => ({
  tick:      isLight() ? 'rgba(15,23,42,0.85)'    : 'rgba(255,255,255,0.7)',
  grid:      isLight() ? 'rgba(100,116,139,0.2)'   : 'rgba(255,255,255,0.08)',
  gridW:     1.5,
  axis:      isLight() ? 'rgba(15,23,42,0.5)'      : 'rgba(255,255,255,0.3)',
  axisW:     2.5,
  title:     isLight() ? 'rgba(15,23,42,0.75)'     : 'rgba(255,255,255,0.55)',
  legend:    isLight() ? 'rgba(15,23,42,0.85)'     : 'rgba(255,255,255,0.7)',
  tickW:     '700' as const,
});

const renderChart = () => {
  if (!chartCanvas.value) return;
  if (chartInstance) { chartInstance.destroy(); chartInstance = null; }

  const today = new Date();
  const timeline = Array.from({ length: 90 }, (_, i) => {
    const d = new Date(today); d.setDate(d.getDate() - (89 - i)); return d;
  });
  const dataMap = new Map(props.data.map(d => [new Date(d.day).toISOString().split('T')[0], d.count]));
  const labels = timeline.map(d => d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' }));
  const counts = timeline.map(d => dataMap.get(d.toISOString().split('T')[0]) ?? 0);
  const col = c();

  chartInstance = new Chart(chartCanvas.value, {
    type: 'line',
    data: { labels, datasets: [{ label: 'Daily Registrations', data: counts, borderColor: '#00bcd4', backgroundColor: 'rgba(0,188,212,0.12)', tension: 0.4, fill: true, borderWidth: 2.5, pointRadius: 0 }] },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top', labels: { color: col.legend, font: { size: 11, weight: col.tickW } } },
        title:  { display: true, text: 'Registration Trend (Last 90 Days)', color: col.title, font: { size: 12, weight: '700' } },
      },
      scales: {
        x: { ticks: { color: col.tick, font: { size: 10, weight: col.tickW }, maxTicksLimit: 10 }, grid: { color: col.grid, lineWidth: col.gridW }, border: { color: col.axis, width: col.axisW } },
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
