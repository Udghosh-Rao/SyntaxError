<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Topbar -->
    <header class="sticky top-0 z-40 border-b border-gray-100 bg-white/90 backdrop-blur-sm">
      <div class="mx-auto max-w-6xl px-6 h-14 flex items-center gap-4">
        <router-link to="/home" class="text-gray-400 hover:text-gray-600 text-sm transition">← Back</router-link>
        <span class="font-bold text-sm text-gray-900">SportsSync</span>
      </div>
    </header>

    <!-- Loading -->
    <div v-if="!event" class="flex justify-center py-24">
      <div class="w-8 h-8 border-2 border-gray-200 border-t-gray-900 rounded-full animate-spin"></div>
    </div>

    <main v-if="event" class="mx-auto max-w-6xl px-6 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Main -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Header card -->
          <div class="bg-white rounded-2xl border border-gray-100 shadow-card p-6">
            <div class="flex items-center gap-2 mb-3">
              <span class="badge badge-blue">{{ event.sport_category }}</span>
              <span v-if="event.price_tier" class="badge" :class="tierBadge">{{ event.price_tier }}</span>
            </div>
            <h1 class="text-2xl font-bold text-gray-900">{{ event.title }}</h1>
          </div>

          <!-- Details -->
          <div class="bg-white rounded-2xl border border-gray-100 shadow-card p-6">
            <h2 class="text-sm font-semibold text-gray-900 mb-4">Event Details</h2>
            <dl class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div v-for="d in details" :key="d.label" class="flex items-start gap-3">
                <span class="text-base mt-0.5">{{ d.icon }}</span>
                <div>
                  <dt class="text-xs text-gray-400">{{ d.label }}</dt>
                  <dd class="text-sm font-medium text-gray-900 mt-0.5">{{ d.value }}</dd>
                </div>
              </div>
            </dl>
          </div>

          <!-- Description -->
          <div class="bg-white rounded-2xl border border-gray-100 shadow-card p-6">
            <h2 class="text-sm font-semibold text-gray-900 mb-3">About This Event</h2>
            <p class="text-sm text-gray-600 leading-relaxed">{{ event.description || 'No description provided.' }}</p>
            <div v-if="event.tags?.length" class="flex flex-wrap gap-2 mt-4">
              <span v-for="tag in event.tags" :key="tag"
                class="px-2.5 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">{{ tag }}</span>
            </div>
          </div>

          <!-- Similar events -->
          <div v-if="similarEvents.length">
            <h2 class="text-sm font-semibold text-gray-900 mb-4">Similar Events</h2>
            <div class="snap-row">
              <EventCard v-for="e in similarEvents" :key="e.id" :event="e" />
            </div>
          </div>
        </div>

        <!-- Registration sidebar -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-2xl border border-gray-100 shadow-card p-6 sticky top-20">
            <div class="text-3xl font-bold text-gray-900 mb-1">₹{{ Number(event.price).toLocaleString('en-IN') }}</div>
            <p class="text-xs text-gray-400 mb-5">per person</p>

            <!-- Fill rate -->
            <div class="mb-5">
              <div class="flex justify-between text-xs text-gray-500 mb-1.5">
                <span>{{ event.seats_sold }}/{{ event.capacity }} registered</span>
                <span>{{ event.fill_rate }}% full</span>
              </div>
              <div class="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                <div class="h-full bg-gray-900 rounded-full transition-all" :style="`width:${event.fill_rate}%`"></div>
              </div>
            </div>

            <div v-if="!isRegistered">
              <button
                v-if="event.seats_remaining > 0"
                @click="handleRegisterAndPay"
                :disabled="paymentLoading"
                class="w-full py-2.5 bg-gray-900 text-white text-sm font-semibold rounded-xl hover:bg-gray-800 disabled:opacity-50 transition shadow-btn"
              >
                {{ paymentLoading ? 'Processing…' : 'Register & Pay' }}
              </button>
              <div v-else class="text-center text-sm text-red-600 bg-red-50 border border-red-100 rounded-xl py-2.5 px-4">
                Fully booked
              </div>
            </div>
            <div v-else class="text-center text-sm text-green-700 bg-green-50 border border-green-100 rounded-xl py-2.5 px-4 font-medium">
              ✓ You're registered
            </div>

            <div v-if="paymentError" class="mt-3 text-xs text-red-600 bg-red-50 border border-red-100 rounded-lg px-3 py-2">{{ paymentError }}</div>
            <div v-if="paymentSuccess" class="mt-3 text-xs text-green-700 bg-green-50 border border-green-100 rounded-lg px-3 py-2">{{ paymentSuccess }}</div>

            <div class="mt-4 pt-4 border-t border-gray-100 text-xs text-gray-400 text-center">
              Secure payments via Razorpay
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useEventsStore } from '@/stores/events'
import EventCard from '@/components/EventCard.vue'
import api from '@/services/api'

const route = useRoute()
const eventsStore = useEventsStore()
const event = ref(null)
const similarEvents = ref([])
const isRegistered = ref(false)
const paymentLoading = ref(false)
const paymentError = ref('')
const paymentSuccess = ref('')

const tierBadge = computed(() => {
  const t = event.value?.price_tier?.toLowerCase()
  if (t === 'premium') return 'badge-green'
  if (t === 'mid') return 'badge-yellow'
  return 'badge-gray'
})

const details = computed(() => event.value ? [
  { icon: '📅', label: 'Date & Time', value: new Date(event.value.event_date).toLocaleString('en-IN', { dateStyle: 'full', timeStyle: 'short' }) },
  { icon: '📍', label: 'City', value: event.value.venue_city },
  { icon: '🏟️', label: 'Venue', value: event.value.venue_address || 'TBA' },
  { icon: '👤', label: 'Organizer', value: event.value.organizer_name || '—' },
  { icon: '🎟️', label: 'Seats Left', value: `${event.value.seats_remaining} of ${event.value.capacity}` },
] : [])

async function handleRegisterAndPay() {
  paymentLoading.value = true; paymentError.value = ''; paymentSuccess.value = ''
  try {
    const res = await api.post('/payments/create-order', { event_id: event.value.id })
    const { order_id, amount, currency, key_id } = res.data
    const options = {
      key: key_id, amount, currency, name: 'SportsSync', description: event.value.title, order_id,
      handler: async (response) => {
        try {
          await api.post('/payments/verify', { razorpay_order_id: response.razorpay_order_id, razorpay_payment_id: response.razorpay_payment_id, razorpay_signature: response.razorpay_signature })
          isRegistered.value = true; paymentSuccess.value = 'Payment successful! Your registration is confirmed.'
        } catch { paymentError.value = 'Payment verification failed. Please contact support.' }
      },
      theme: { color: '#111827' },
    }
    new window.Razorpay(options).open()
  } catch (e) { paymentError.value = e.response?.data?.error || 'Failed to initiate payment.' }
  finally { paymentLoading.value = false }
}

onMounted(async () => {
  const id = route.params.id
  try {
    event.value = await eventsStore.fetchEventById(id)
    similarEvents.value = await eventsStore.fetchSimilarEvents(id)
    const myRegs = await api.get('/registrations/my')
    isRegistered.value = myRegs.data.some(r => r.event_id == id && r.status === 'confirmed')
  } catch (e) { console.error(e) }
})
</script>
