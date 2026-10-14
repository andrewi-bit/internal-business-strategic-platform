<script setup lang="ts">
import DashboardCard from '../shared/DashboardCard.vue'

import type { StatusSlice } from '../../types/types'

const props = defineProps<{
  slices: StatusSlice[]
}>()

const total = computed(() => props.slices.reduce((sum, slice) => sum + slice.value, 0))

const getShare = (value: number) => (total.value > 0 ? ((value / total.value) * 100).toFixed(1) : '0.0')

const option = computed<ECOption>(() => ({
  tooltip: {
    trigger: 'item',
    backgroundColor: '#0F172A',
    borderWidth: 0,
    padding: [8, 12],
    textStyle: { color: '#fff', fontSize: 12 },
    formatter: '{b}<br/>{c} projects · {d}%'
  },
  series: [
    {
      type: 'pie',
      radius: ['70%', '92%'],
      center: ['50%', '50%'],
      avoidLabelOverlap: true,
      padAngle: 2,
      label: { show: false },
      labelLine: { show: false },
      itemStyle: { borderColor: '#fff', borderWidth: 2 },
      data: props.slices.map(slice => ({
        name: slice.label,
        value: slice.value,
        itemStyle: { color: slice.color }
      })),
      animationDuration: 600
    }
  ]
}))
</script>

<template>
  <DashboardCard
    title="Portfolio Status"
    subtitle="Across the lifecycle"
    :padded="false"
  >
    <div class="flex flex-col gap-4 p-4 lg:flex-row lg:items-center lg:gap-4">
      <!-- Donut Chart + Center Score -->
      <div class="relative mx-auto h-48 w-full min-w-0 max-w-56 shrink-0 lg:h-[100px] lg:w-[100px] lg:max-w-none">
        <VChart
          :option="option"
          autoresize
        />
        <div
          class="pointer-events-none absolute inset-0 flex flex-col items-center justify-center"
        >
          <span class="text-3xl leading-8 font-bold tracking-tight text-slate-900 tabular-nums">
            {{ total }}
          </span>
          <span class="text-[11px] leading-4 font-medium text-slate-500">Total Projects</span>
        </div>
      </div>

      <!-- Legend List -->
      <div class="min-w-0 flex-1 space-y-2">
        <div
          v-for="slice in slices"
          :key="slice.label"
          class="flex items-center justify-between gap-2"
        >
          <div class="flex min-w-0 items-center gap-2">
            <span
              class="h-2.5 w-2.5 shrink-0 rounded-full"
              :style="{ backgroundColor: slice.color }"
            />
            <span class="truncate text-xs leading-4 font-medium text-slate-600">{{ slice.label }}</span>
          </div>

          <div class="flex shrink-0 items-baseline gap-2 tabular-nums">
            <span class="text-xs leading-4 font-semibold text-slate-900">{{ slice.value }}</span>
            <span class="w-10 text-right text-[11px] leading-4 text-slate-400">{{ getShare(slice.value) }}%</span>
          </div>
        </div>
      </div>
    </div>
  </DashboardCard>
</template>
