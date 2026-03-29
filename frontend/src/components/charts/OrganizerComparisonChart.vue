<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps<{
  data: Array<{ organizer_name: string; total_revenue: number; total_registrations: number; total_events: number }>;
}>();

const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

const isLight = () => document.documentElement.getAttribute('data-theme') === 'light';

const colors = () => ({
  tick:       isLight() ? 'rgba(15,23,42,0.9)'     : 'rgba(255,255,255,0.75)',
  tickWeight: '700' as const,
  grid:       isLight() ? 'rgba(100,116,139,0.25)'  : 'rgba(255,255,255,0.1)',
  gridWidth:  1.5,
  axis:       isLight() ? 'rgba(15,23,42,0.55)'     : 'rgba(255,255,255,0.35)',
  axisWidth:  2.5,
  title:      isLight() ? 'rgba(15,23,42,0.8)'      : 'rgba(255,255,255,0.6)',
  legend:     isLight() ? 'rgba(15,23,42,0.9)'      : 'rgba(255,255,255,0.8)',
  axisLabel:  isLight() ? 'rgba(15,23,42,0.7)'      : 'rgba(255,255,255,0.5)',
});

const renderChart = () => {
  if (!chartCanvas.value || !props.data?.length) return;
  if (chartInstance) { chartInstance.destroy(); chartInstance = null; }

  const labels  = props.data.map(d => d.organizer_name);
  const revenue = props.data.map(d => d.total_revenue);
  const regs    = props.data.map(d => d.total_registrations);
  const c = colors();

  chartInstance = new Chart(chartCanvas.value, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: 'Revenue (₹)',
          data: revenue,
          backgroundColor: 'rgba(0,112,243,0.75)',
          borderColor: '#0070f3',
          borderWidth: 1.5,
          yAxisID: 'y',
        },
        {
          label: 'Registrations',
          data: regs,
          backgroundColor: 'rgba(0,223,216,0.75)',
          borderColor: '#00dfd8',
          borderWidth: 1.5,
          yAxisID: 'y1',
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
          labels: { color: c.legend, font: { size: 11, weight: c.tickWeight } },
        },
        title: {
          display: true,
          text: 'Organizer Performance Comparison',
          color: c.title,
          font: { size: 12, weight: '700' },
        },
      },
      scales: {
        x: {
          ticks:  { color: c.tick, font: { size: 10, weight: c.tickWeight } },
          grid:   { color: c.grid, lineWidth: c.gridWidth },
          border: { color: c.axis, width: c.axisWidth },
        },
        y: {
          type: 'linear', position: 'left',
          ticks:  { color: c.tick, font: { weight: c.tickWeight } },
          grid:   { color: c.grid, lineWidth: c.gridWidth },
          border: { color: c.axis, width: c.axisWidth },
          title:  { display: true, text: 'Revenue (₹)', color: c.axisLabel, font: { weight: '600' } },
        },
        y1: {
          type: 'linear', position: 'right',
          ticks:  { color: c.tick, font: { weight: c.tickWeight } },
          grid:   { drawOnChartArea: false },
          border: { color: c.axis, width: c.axisWidth },
          title:  { display: true, text: 'Registrations', color: c.axisLabel, font: { weight: '600' } },
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
