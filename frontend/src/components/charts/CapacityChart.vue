<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps<{ data: Array<{ title: string; registrations: number; capacity: number }> }>();
const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

const isLight = () => document.documentElement.getAttribute('data-theme') === 'light';

const c = () => ({
  tick:      isLight() ? 'rgba(15,23,42,0.85)'   : 'rgba(255,255,255,0.7)',
  grid:      isLight() ? 'rgba(100,116,139,0.2)'  : 'rgba(255,255,255,0.08)',
  gridW:     1.5,
  axis:      isLight() ? 'rgba(15,23,42,0.5)'     : 'rgba(255,255,255,0.3)',
  axisW:     2.5,
  title:     isLight() ? 'rgba(15,23,42,0.75)'    : 'rgba(255,255,255,0.55)',
  legend:    isLight() ? 'rgba(15,23,42,0.85)'    : 'rgba(255,255,255,0.65)',
  capBg:     isLight() ? 'rgba(100,116,139,0.15)' : 'rgba(255,255,255,0.08)',
  capBorder: isLight() ? 'rgba(100,116,139,0.5)'  : 'rgba(255,255,255,0.2)',
  tickW:     '700' as const,
});

const renderChart = () => {
  if (!chartCanvas.value || !props.data?.length) return;
  if (chartInstance) { chartInstance.destroy(); chartInstance = null; }
  const col = c();
  const labels = props.data.map(d => d.title.length > 18 ? d.title.substring(0, 18) + '…' : d.title);
  const caps = props.data.map(d => d.capacity);
  const regs = props.data.map(d => d.registrations);
  chartInstance = new Chart(chartCanvas.value, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        { label: 'Capacity', data: caps, backgroundColor: col.capBg, borderColor: col.capBorder, borderWidth: 1.5, borderRadius: 4 },
        { label: 'Registered', data: regs, backgroundColor: regs.map((r, i) => { const rate = caps[i] > 0 ? (r / caps[i]) * 100 : 0; return rate > 70 ? 'rgba(0,223,216,0.8)' : rate > 30 ? 'rgba(255,171,0,0.8)' : 'rgba(255,85,85,0.8)'; }), borderRadius: 4 },
      ],
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { position: 'top', labels: { color: col.legend, font: { size: 11, weight: col.tickW } } },
        title: { display: true, text: 'Capacity vs Registrations', color: col.title, font: { size: 12, weight: '700' } },
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
.chart-container { position: relative; height: 280px; width: 100%; }
</style>
