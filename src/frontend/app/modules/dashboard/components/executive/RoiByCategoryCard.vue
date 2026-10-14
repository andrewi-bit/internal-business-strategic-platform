<script setup lang="ts">
import DashboardCard from '../shared/DashboardCard.vue'

import type { CategoryMetric } from '../../types/types'

const props = defineProps<{
  categories: CategoryMetric[]
  average: number
}>()

const option = computed<ECOption>(() => ({
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'shadow' },
    backgroundColor: '#0F172A',
    borderWidth: 0,
    padding: [8, 12],
    textStyle: { color: '#fff', fontSize: 12 },
    formatter: '{b}<br/>ROI: {c}%'
  },
  grid: {
    top: 8,
    right: 44,
    bottom: 0,
    left: 0,
    containLabel: true
  },
  xAxis: {
    type: 'value',
    min: 0,
    max: 36,
    interval: 12,
    splitLine: { lineStyle: { color: '#F1F5F9' } },
    axisLine: { show: false },
    axisTick: { show: false },
    axisLabel: { color: '#94A3B8', fontSize: 11, formatter: '{value}%' }
  },
  yAxis: {
    type: 'category',
    inverse: true,
    data: props.categories.map(category => category.label),
    axisLine: { show: false },
    axisTick: { show: false },
    axisLabel: { color: '#475569', fontSize: 12, fontWeight: 500, margin: 12 }
  },
  series: [
    {
      name: 'ROI',
      type: 'bar',
      barWidth: 12,
      data: props.categories.map(category => category.roi),
      itemStyle: {
        borderRadius: [0, 6, 6, 0],
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 1,
          y2: 0,
          colorStops: [
            { offset: 0, color: '#60A5FA' },
            { offset: 1, color: '#2563EB' }
          ]
        }
      },
      label: {
        show: true,
        position: 'right',
        color: '#0F172A',
        fontSize: 11,
        fontWeight: 600,
        formatter: '{c}%'
      },
      markLine: {
        silent: true,
        symbol: 'none',
        lineStyle: { color: '#94A3B8', type: 'dashed', width: 1 },
        label: {
          show: true,
          position: 'end',
          color: '#64748B',
          fontSize: 10,
          fontWeight: 600,
          formatter: 'Avg {c}%'
        },
        data: [{ xAxis: props.average }]
      },
      animationDuration: 600
    }
  ]
}))
</script>

<template>
  <DashboardCard
    title="ROI by Category"
    subtitle="Average return by vertical"
  >
    <div class="h-[23rem] min-w-0 lg:h-[100px]">
      <VChart
        :option="option"
        autoresize
      />
    </div>
  </DashboardCard>
</template>
