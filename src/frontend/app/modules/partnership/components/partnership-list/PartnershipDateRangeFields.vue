<script setup lang="ts">
interface Props {
  start: string
  end: string
  error?: string
}

const props = withDefaults(defineProps<Props>(), {
  error: ''
})

const emit = defineEmits<{
  (e: 'update:start' | 'update:end', value: string): void
}>()

const fieldClass = (invalid: boolean) =>
  invalid
    ? 'border-rose-300 focus:border-rose-500'
    : 'border-slate-200 focus:border-blue-500'
</script>

<template>
  <div class="mt-2">
    <div class="grid grid-cols-2 gap-2.5">
      <div class="flex flex-col gap-1">
        <label class="text-[11px] font-semibold text-slate-500">Start date</label>
        <input
          :value="props.start"
          type="date"
          :max="props.end || undefined"
          class="h-8.5 rounded-lg border bg-white px-2.5 text-xs text-slate-700 focus:outline-none"
          :class="fieldClass(Boolean(props.error))"
          @input="emit('update:start', ($event.target as HTMLInputElement).value)"
        >
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-[11px] font-semibold text-slate-500">End date</label>
        <input
          :value="props.end"
          type="date"
          :min="props.start || undefined"
          class="h-8.5 rounded-lg border bg-white px-2.5 text-xs text-slate-700 focus:outline-none"
          :class="fieldClass(Boolean(props.error))"
          @input="emit('update:end', ($event.target as HTMLInputElement).value)"
        >
      </div>
    </div>
    <p
      v-if="props.error"
      class="mt-1.5 flex items-center gap-1 text-[11px] font-medium text-rose-600"
    >
      <UIcon
        name="i-lucide-circle-alert"
        class="h-3.5 w-3.5"
      />
      {{ props.error }}
    </p>
  </div>
</template>
