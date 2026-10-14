<script setup lang="ts">
import DashboardCard from '../shared/DashboardCard.vue'

import type { ConversionTrendPoint } from '../../types/commercial.types'

const props = defineProps<{
  points: ConversionTrendPoint[]
  target: number
}>()

type ConversionRange = '3m' | '6m' | '12m'

const rangeOptions: { label: string, value: ConversionRange, months: number }[] = [
  { label: 'This Quarter', value: '3m', months: 3 },
  { label: 'Last 6 Months', value: '6m', months: 6 },
  { label: 'Last 12 Months', value: '12m', months: 12 }
]

const selectedRange = ref<ConversionRange>('12m')

const selectedRangeLabel = computed(
  () => rangeOptions.find(range => range.value === selectedRange.value)?.label ?? ''
)

const visiblePoints = computed(() => {
  const months = rangeOptions.find(range => range.value === selectedRange.value)?.months ?? 12
  return props.points.slice(-months)
})

const rangeMenuItems = computed(() =>
  rangeOptions.map(range => ({
    label: range.label,
    checked: selectedRange.value === range.value,
    onSelect: () => {
      selectedRange.value = range.value
    }
  }))
)

const option = computed<ECOption>(() => ({
  tooltip: {
    trigger: 'axis',
    backgroundColor: '#0F172A',
    borderWidth: 0,
    padding: [8, 12],
    textStyle: { color: '#fff', fontSize: 12 },
    axisPointer: {
      type: 'line',
      lineStyle: { color: '#CBD5E1', type: 'dashed' }
    },
    formatter: '{b}<br/>Conversion: {c}%'
  },
  grid: {
    top: 24,
    right: 8,
    bottom: 0,
    left: 0,
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: visiblePoints.value.map(point => point.month),
    axisLine: { lineStyle: { color: '#E2E8F0' } },
    axisTick: { show: false },
    axisLabel: { color: '#94A3B8', fontSize: 11, margin: 8 }
  },
  yAxis: {
    type: 'value',
    min: 0,
    max: 30,
    interval: 10,
    splitLine: { lineStyle: { color: '#F1F5F9' } },
    axisLine: { show: false },
    axisTick: { show: false },
    axisLabel: { color: '#94A3B8', fontSize: 11, formatter: '{value}%' }
  },
  series: [
    {
      name: 'Conversion Rate',
      type: 'line',
      data: visiblePoints.value.map(point => point.rate),
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      lineStyle: { width: 2.5, color: '#2563EB' },
      itemStyle: { color: '#2563EB', borderColor: '#fff', borderWidth: 2 },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(37, 99, 235, 0.18)' },
            { offset: 1, color: 'rgba(37, 99, 235, 0)' }
          ]
        }
      },
      markLine: {
        silent: true,
        symbol: 'none',
        lineStyle: { color: '#94A3B8', type: 'dashed', width: 1 },
        label: {
          show: true,
          position: 'insideEndTop',
          color: '#64748B',
          fontSize: 10,
          fontWeight: 600,
          formatter: 'Target {c}%'
        },
        data: [{ yAxis: props.target }]
      },
      animationDuration: 600
    }
  ]
}))
</script>

<template>
  <DashboardCard
    title="Conversion Rate Trend"
    subtitle="Won deals as a share of total prospects over time"
    :padded="false"
  >
    <template #actions>
      <UDropdownMenu
        :items="rangeMenuItems"
        :content="{ align: 'end' }"
      >
        <button
          type="button"
          class="inline-flex items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-2.5 py-1 text-[11px] font-semibold text-slate-700 shadow-xs transition-colors hover:bg-slate-50 cursor-pointer"
        >
          <UIcon
            name="i-lucide-calendar-days"
            class="h-3.5 w-3.5 text-slate-400"
          />
          <span>{{ selectedRangeLabel }}</span>
          <UIcon
            name="i-lucide-chevron-down"
            class="h-3.5 w-3.5 text-slate-400"
          />
        </button>
      </UDropdownMenu>
    </template>

    <div class="h-72 min-w-0 px-3 pt-2 pb-2 lg:h-[130px]">
      <VChart
        :option="option"
        autoresize
      />
    </div>
  </DashboardCard>
</template>
