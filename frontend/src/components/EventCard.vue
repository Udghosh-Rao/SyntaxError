<template>
  <router-link :to="`/event/${event.id}`" class="block w-64 flex-shrink-0 group">
    <div class="bg-white rounded-xl border border-gray-100 shadow-card group-hover:shadow-card-hover group-hover:-translate-y-0.5 transition-all overflow-hidden">
      <!-- Top color stripe -->
      <div class="h-1.5 w-full" :style="`background:${sportColor}`"></div>

      <div class="p-4">
        <div class="flex items-start justify-between gap-2 mb-3">
          <span class="badge badge-gray text-xs">{{ event.sport_category }}</span>
          <span class="text-xs font-bold text-gray-900">₹{{ Number(event.price).toLocaleString('en-IN') }}</span>
        </div>

        <h3 class="text-sm font-semibold text-gray-900 leading-snug mb-3 line-clamp-2">{{ event.title }}</h3>

        <div class="space-y-1.5 mb-4">
          <div class="flex items-center gap-1.5 text-xs text-gray-500">
            <span>📅</span> <span>{{ formatDate(event.event_date) }}</span>
          </div>
          <div class="flex items-center gap-1.5 text-xs text-gray-500">
            <span>📍</span> <span>{{ event.venue_city }}</span>
          </div>
        </div>

        <!-- Fill bar -->
        <div class="flex items-center gap-2">
          <div class="flex-1 h-1 bg-gray-100 rounded-full overflow-hidden">
            <div class="h-full rounded-full transition-all" :style="`width:${event.fill_rate || 0}%; background:${sportColor}`"></div>
          </div>
          <span :class="seatsClass" class="text-xs font-medium whitespace-nowrap">{{ event.seats_remaining }} left</span>
        </div>
      </div>
    </div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ event: { type: Object, required: true } })

const SPORT_COLORS = {
  football: '#22c55e', cricket: '#f59e0b', tennis: '#3b82f6',
  basketball: '#ef4444', running: '#8b5cf6', badminton: '#6366f1',
  swimming: '#06b6d4', cycling: '#f97316',
}

const sportColor = computed(() => SPORT_COLORS[props.event.sport_category?.toLowerCase()] || '#6b7280')

const seatsClass = computed(() => {
  const r = props.event.seats_remaining
  if (r <= 0) return 'text-red-500'
  if (r <= 10) return 'text-yellow-600'
  return 'text-gray-400'
})

function formatDate(d) {
  return new Date(d).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })
}
</script>
