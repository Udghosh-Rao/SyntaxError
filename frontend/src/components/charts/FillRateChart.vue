<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps<{
  data: Array<{
    event_id: number;
    title: string;
    organizer_name?: string;
    capacity: number;
    seats_filled: number;
    fill_rate: number;
  }>;
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
});

const renderChart = () => {
  if (!chartCanvas.value || !props.data?.length) return;
  if (chartInstance) { chartInstance.destroy(); chartInstance = null; }

  const sorted = [...props.data].sort((a, b) => b.fill_rate - a.fill_rate);
  const labels = sorted.map(d => d.title.length > 20 ? d.title.substring(0, 20) + '…' : d.title);
  const rates  = sorted.map(d => d.fill_rate);
  const bgColors = rates.map(r => {
    if (r > 70) return 'rgba(0,223,216,0.8)';
    if (r > 30) return 'rgba(255,171,0,0.8)';
    return 'rgba(255,85,85,0.8)';
  });
  const c = colors();

  chartInstance = new Chart(chartCanvas.value, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Fill Rate (%)',
        data: rates,
        backgroundColor: bgColors,
        borderRadius: 4,
        maxBarThickness: 40,
      }],
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        title: {
          display: true,
          text: 'Event Fill Rates',
          color: c.title,
          font: { size: 12, weight: '700' },
        },
      },
      scales: {
        x: {
          min: 0, max: 100,
          ticks: { color: c.tick, font: { weight: c.tickWeight }, callback: (v: any) => v + '%' },
          grid:  { color: c.grid, lineWidth: c.gridWidth },
          border: { color: c.axis, width: c.axisWidth },
        },
        y: {
          ticks: { color: c.tick, font: { size: 11, weight: c.tickWeight } },
          grid:  { display: false },
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
