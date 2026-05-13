<template>
  <teleport to="body">
    <div class="toast-stack">
      <transition-group name="toast" tag="div" class="toast-inner">
        <div
          v-for="t in toasts"
          :key="t.id"
          class="toast"
          :class="`toast--${t.type}`"
          @click="remove(t.id)"
        >
          <span class="toast-icon">
            <svg v-if="t.type === 'success'" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><polyline points="16.5 8.5 10.5 15 7.5 12"/></svg>
            <svg v-else-if="t.type === 'error'" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            <svg v-else-if="t.type === 'warning'" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
            <svg v-else width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
          </span>
          <span class="toast-msg">{{ t.message }}</span>
          <button class="toast-close" @click.stop="remove(t.id)" aria-label="Dismiss">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
          <div class="toast-progress" :style="{ animationDuration: `${t.duration}ms` }" />
        </div>
      </transition-group>
    </div>
  </teleport>
</template>

<script setup lang="ts">
import { useToast } from '../composables/useToast';
const { toasts, remove } = useToast();
</script>

<style scoped>
.toast-stack {
  position: fixed;
  bottom: 1.75rem;
  right: 1.5rem;
  z-index: 9999;
  pointer-events: none;
}
.toast-inner {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  align-items: flex-end;
}
.toast {
  pointer-events: all;
  display: flex;
  align-items: flex-start;
  gap: 0.65rem;
  min-width: 280px;
  max-width: 420px;
  padding: 0.9rem 1rem;
  border-radius: 13px;
  border: 1px solid var(--border-subtle);
  background: var(--bg-panel-solid);
  box-shadow: 0 8px 32px rgba(0,0,0,0.35);
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
[data-theme="light"] .toast { box-shadow: 0 6px 24px rgba(0,0,0,0.12); }

.toast--success { border-color: rgba(34,197,94,0.4); }
.toast--success .toast-icon { color: #22c55e; }
.toast--success .toast-progress { background: #22c55e; }

.toast--error { border-color: rgba(248,113,113,0.4); }
.toast--error .toast-icon { color: #f87171; }
.toast--error .toast-progress { background: #f87171; }

.toast--warning { border-color: rgba(234,179,8,0.4); }
.toast--warning .toast-icon { color: #eab308; }
.toast--warning .toast-progress { background: #eab308; }

.toast--info { border-color: rgba(0,240,255,0.3); }
.toast--info .toast-icon { color: var(--brand-accent); }
.toast--info .toast-progress { background: var(--brand-accent); }

.toast-icon { flex-shrink: 0; margin-top: 1px; }

.toast-msg {
  flex: 1;
  font-size: 0.83rem;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.45;
}

.toast-close {
  background: none; border: none; cursor: pointer;
  color: var(--text-muted); padding: 0; flex-shrink: 0;
  margin-top: 1px; transition: color 0.15s;
}
.toast-close:hover { color: var(--text-primary); }

.toast-progress {
  position: absolute; bottom: 0; left: 0;
  height: 2.5px; width: 100%;
  border-radius: 0 0 13px 13px;
  transform-origin: left;
  animation: shrink linear forwards;
  opacity: 0.65;
}
@keyframes shrink { from { transform: scaleX(1); } to { transform: scaleX(0); } }

.toast-enter-active { transition: all 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
.toast-leave-active { transition: all 0.2s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateX(60px) scale(0.9); }
</style>