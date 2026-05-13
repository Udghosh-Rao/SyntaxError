import { ref } from 'vue';

export type ToastType = 'success' | 'error' | 'warning' | 'info';

export interface Toast {
  id: number;
  message: string;
  type: ToastType;
  duration: number;
}

// Shared state — one instance across the whole app
const toasts = ref<Toast[]>([]);
let nextId = 0;

export function useToast() {
  const add = (message: string, type: ToastType = 'info', duration = 4000) => {
    const id = ++nextId;
    toasts.value.push({ id, message, type, duration });
    setTimeout(() => remove(id), duration);
  };

  const remove = (id: number) => {
    toasts.value = toasts.value.filter(t => t.id !== id);
  };

  return {
    toasts,
    remove,
    success: (msg: string, dur?: number) => add(msg, 'success', dur),
    error:   (msg: string, dur?: number) => add(msg, 'error',   dur ?? 5500),
    warning: (msg: string, dur?: number) => add(msg, 'warning', dur),
    info:    (msg: string, dur?: number) => add(msg, 'info',    dur),
  };
}