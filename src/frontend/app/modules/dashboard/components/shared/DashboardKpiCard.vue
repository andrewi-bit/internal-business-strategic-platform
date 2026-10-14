<script setup lang="ts">
import type { DashboardKpi } from '../../types/types'

defineProps<DashboardKpi>()

const trendColors: Record<'up' | 'down' | 'neutral', string> = {
  up: 'bg-emerald-50 text-emerald-700',
  down: 'bg-rose-50 text-rose-700',
  neutral: 'bg-slate-100 text-slate-600'
}

const trendIcons: Record<'up' | 'down' | 'neutral', string> = {
  up: 'i-lucide-arrow-up-right',
  down: 'i-lucide-arrow-down-right',
  neutral: 'i-minus'
}
</script>

<template>
  <article
    class="relative flex min-w-0 items-start gap-3 overflow-hidden rounded-xl border border-slate-200/80 bg-white p-2.5 shadow-xs"
  >
    <div
      class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-blue-50 text-blue-600"
    >
      <UIcon
        :name="icon"
        class="h-4 w-4"
      />
    </div>

    <div class="min-w-0 flex-1">
      <p class="truncate text-[11px] leading-4 font-semibold text-slate-500">
        {{ label }}
      </p>

      <p class="mt-0.5 truncate text-xl leading-7 font-bold text-slate-900">
        {{ value }}
      </p>

      <div class="mt-0.5 flex min-w-0 items-center gap-1.5">
        <span
          class="inline-flex shrink-0 items-center gap-0.5 rounded-md px-1.5 leading-4 text-[10px] font-semibold tabular-nums"
          :class="trendColors[trend]"
        >
          <UIcon
            :name="trendIcons[trend]"
            class="h-3 w-3"
          />
          <span>{{ delta }}</span>
        </span>
        <span class="truncate text-[11px] leading-4 text-slate-500">{{ deltaLabel }}</span>
      </div>
    </div>

    <div
      v-if="progress !== undefined"
      class="absolute inset-x-0 bottom-0 h-1 bg-slate-100"
    >
      <div
        class="h-full bg-blue-600"
        :style="{ width: `${progress}%` }"
      />
    </div>
  </article>
</template>
