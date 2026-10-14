<script setup lang="ts">
import DashboardCard from '../shared/DashboardCard.vue'

import type { CategoryMetric } from '../../types/types'

const props = defineProps<{
  categories: CategoryMetric[]
  total: number
}>()

const blueRamp = ['#1D4ED8', '#2563EB', '#3B82F6', '#60A5FA', '#93C5FD']
const fallbackColor = '#CBD5E1'

const colorFor = (category: CategoryMetric) => {
  if (category.label === 'Others') return fallbackColor
  const index = props.categories.filter(item => item.label !== 'Others').indexOf(category)
  return blueRamp[index] ?? fallbackColor
}
</script>

<template>
  <DashboardCard
    title="Top Categories"
    subtitle="By industry"
  >
    <template #actions>
      <span class="text-xs leading-4 font-semibold text-slate-500 tabular-nums">{{ total }} projects</span>
    </template>

    <div class="flex min-h-full flex-col">
      <!-- 100% stacked composition bar -->
      <div class="flex h-2.5 w-full shrink-0 overflow-hidden rounded-full bg-slate-100">
        <div
          v-for="category in categories"
          :key="category.label"
          class="h-full"
          :style="{ width: `${category.share}%`, backgroundColor: colorFor(category) }"
        />
      </div>

      <!-- Legend -->
      <div class="mt-2 grid shrink-0 grid-cols-2 gap-x-2 gap-y-1.5">
        <div
          v-for="category in categories"
          :key="category.label"
          class="flex min-w-0 items-center gap-1.5"
        >
          <span
            class="h-2 w-2 shrink-0 rounded-full"
            :style="{ backgroundColor: colorFor(category) }"
          />
          <span class="truncate text-[11px] leading-4 font-medium text-slate-600">{{ category.label }}</span>
          <span class="ml-auto shrink-0 text-xs leading-4 font-semibold text-slate-900 tabular-nums">
            {{ category.share }}%
          </span>
        </div>
      </div>

      <!-- Insight -->
      <div
        class="mt-auto flex shrink-0 items-center gap-2 border-t border-slate-100 pt-1.5 text-xs leading-4 text-slate-500"
      >
        <UIcon
          name="i-lucide-info"
          class="h-3.5 w-3.5 shrink-0 text-slate-400"
        />
        <span class="truncate">Banking leads volume; Energy leads ROI.</span>
      </div>
    </div>
  </DashboardCard>
</template>
