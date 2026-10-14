<script setup lang="ts">
interface MetricItem {
  label: string
  value: string
  sublabel: string
}

interface Props {
  metrics: MetricItem[]
}

defineProps<Props>()
</script>

<template>
  <div class="space-y-4 rounded-2xl border border-slate-200/80 bg-white p-5 sm:p-6 shadow-2xs">
    <!-- Header -->
    <div class="flex items-center gap-2.5 text-slate-900">
      <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-50 text-blue-600">
        <UIcon name="i-lucide-bar-chart-2" class="h-4.5 w-4.5" />
      </div>
      <h2 class="text-base font-bold tracking-tight">Success Metrics & Impact</h2>
    </div>

    <!-- 4 Metric Cards Grid -->
    <div class="grid grid-cols-2 gap-3 sm:grid-cols-4">
      <div
        v-for="(item, idx) in metrics"
        :key="idx"
        class="flex flex-col justify-between rounded-xl border border-slate-100 bg-slate-50/60 p-4 text-center"
      >
        <div class="flex items-center justify-center gap-1">
          <span class="text-xl sm:text-2xl font-bold tracking-tight text-slate-900">
            {{ item.value }}
          </span>
          <UIcon name="i-lucide-arrow-up" class="h-3.5 w-3.5 text-emerald-600 font-bold" />
        </div>
        <p class="mt-1.5 text-[11px] font-medium text-slate-500 leading-snug">
          {{ item.label }}
        </p>
      </div>
    </div>
  </div>
</template>
