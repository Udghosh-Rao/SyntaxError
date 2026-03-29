<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps<{ data: Array<{ title: string; revenue: number }> }>();
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
  if (!chartCanvas.value || !props.data?.length) return;
  if (chartInstance) { chartInstance.destroy(); chartInstance = null; }
  const col = c();
  const colors = ['#0070f3','#00dfd8','#ff0080','#7928ca','#ffab00','#36A2EB'];
  const labels = props.data.map(d => d.title.length > 18 ? d.title.substring(0, 18) + '…' : d.title);
  const values = props.data.map(d => d.revenue);
  chartInstance = new Chart(chartCanvas.value, {
    type: 'bar',
    data: { labels, datasets: [{ label: 'Revenue (₹)', data: values, backgroundColor: values.map((_, i) => colors[i % colors.length] + 'B3'), borderColor: values.map((_, i) => colors[i % colors.length]), borderWidth: 1.5, borderRadius: 6 }] },
    options: {
      indexAxis: 'y', responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        title: { display: true, text: 'Revenue per Event', color: col.title, font: { size: 12, weight: '700' } },
      },
      scales: {
        x: { beginAtZero: true, ticks: { color: col.tick, font: { weight: col.tickW }, callback: (v: any) => '₹' + v.toLocaleString() }, grid: { color: col.grid, lineWidth: col.gridW }, border: { color: col.axis, width: col.axisW } },
        y: { ticks: { color: col.tick, font: { size: 11, weight: col.tickW } }, grid: { display: false }, border: { color: col.axis, width: col.axisW } },
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
