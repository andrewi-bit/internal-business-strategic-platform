<script setup lang="ts">
import DashboardCard from '../shared/DashboardCard.vue'

import type { PipelineStage } from '../../types/types'

const props = defineProps<{
  stages: PipelineStage[]
  openValue: string
}>()

const option = computed<ECOption>(() => ({
  tooltip: {
    trigger: 'item',
    backgroundColor: '#0F172A',
    borderWidth: 0,
    padding: [8, 12],
    textStyle: { color: '#fff', fontSize: 12 },
    formatter: '{b}<br/>{c} opportunities'
  },
  series: [
    {
      type: 'funnel',
      left: '4%',
      right: '4%',
      top: 4,
      bottom: 4,
      sort: 'none',
      gap: 4,
      minSize: '24%',
      label: {
        show: false
      },
      labelLine: { show: false },
      itemStyle: { borderWidth: 0 },
      data: props.stages.map(stage => ({
        name: stage.label,
        value: stage.opportunities,
        itemStyle: { color: stage.color }
      })),
      animationDuration: 600
    }
  ]
}))
</script>

<template>
  <DashboardCard
    title="Revenue Pipeline"
    subtitle="By stage"
  >
    <template #actions>
      <span
        class="inline-flex items-center rounded-full bg-blue-50 px-2.5 py-1 text-[11px] font-semibold text-blue-700 tabular-nums"
      >
        {{ openValue }} open
      </span>
    </template>

    <div class="flex min-w-0 flex-col gap-3 sm:flex-row sm:items-stretch">
      <div class="h-40 min-w-0 shrink-0 sm:h-52 sm:w-[38%] lg:h-[100px]">
        <VChart
          :option="option"
          autoresize
        />
      </div>

      <div class="flex min-w-0 flex-1 flex-col justify-center">
        <div
          v-for="stage in stages"
          :key="stage.label"
          class="flex items-center gap-2 py-0.5"
        >
          <span
            class="h-1.5 w-1.5 shrink-0 rounded-full"
            :style="{ backgroundColor: stage.color }"
          />
          <span class="min-w-0 truncate text-xs leading-4 font-medium text-slate-600">{{ stage.label }}</span>

          <span class="ml-auto shrink-0 text-[11px] leading-4 text-slate-400 tabular-nums">
            {{ stage.opportunities }}
          </span>
          <span
            class="shrink-0 text-xs leading-4 font-semibold tabular-nums"
            :class="stage.open ? 'text-slate-900' : 'text-emerald-600'"
          >
            {{ stage.value }}
          </span>
        </div>
      </div>
    </div>
  </DashboardCard>
</template>
