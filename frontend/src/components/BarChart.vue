<template>
  <Bar :data="data" :options="options" />
</template>

<script setup>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js'
ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend)

defineProps({ data: Object })

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: '#fff',
      titleColor: '#111827',
      bodyColor: '#6b7280',
      borderColor: '#e5e7eb',
      borderWidth: 1,
      padding: 10,
    },
  },
  scales: {
    x: {
      ticks: { color: '#9ca3af', font: { size: 11, family: 'Inter' } },
      grid: { display: false },
      border: { display: false },
    },
    y: {
      ticks: { color: '#9ca3af', font: { size: 11, family: 'Inter' } },
      grid: { color: '#f3f4f6', lineWidth: 1 },
      border: { display: false },
    },
  },
}
</script>
