<script setup lang="ts">
import DashboardCard from '../shared/DashboardCard.vue'

import type { TrendPoint } from '../../types/types'

const props = defineProps<{
  points: TrendPoint[]
}>()

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
    }
  },
  legend: {
    top: 0,
    right: 0,
    icon: 'circle',
    itemWidth: 8,
    itemHeight: 8,
    itemGap: 18,
    textStyle: { color: '#475569', fontSize: 12, fontWeight: 500 }
  },
  grid: {
    top: 30,
    right: 8,
    bottom: 0,
    left: 0,
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: props.points.map(point => point.month),
    axisLine: { lineStyle: { color: '#E2E8F0' } },
    axisTick: { show: false },
    axisLabel: { color: '#94A3B8', fontSize: 11, margin: 8 }
  },
  yAxis: [
    {
      type: 'value',
      min: 0,
      max: 160,
      interval: 40,
      splitLine: { lineStyle: { color: '#F1F5F9' } },
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { color: '#94A3B8', fontSize: 11 }
    },
    {
      type: 'value',
      min: 0,
      max: 30,
      interval: 10,
      position: 'right',
      splitLine: { show: false },
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { color: '#94A3B8', fontSize: 11 }
    }
  ],
  series: [
    {
      name: 'Projects',
      type: 'line',
      yAxisIndex: 0,
      data: props.points.map(point => point.projects),
      smooth: true,
      symbol: 'none',
      lineStyle: { width: 2, color: '#94A3B8', type: 'dashed' },
      itemStyle: { color: '#94A3B8' },
      z: 3
    },
    {
      name: 'Revenue',
      type: 'line',
      yAxisIndex: 1,
      data: props.points.map(point => point.revenue),
      smooth: true,
      symbol: 'none',
      lineStyle: { width: 2.5, color: '#2563EB' },
      itemStyle: { color: '#2563EB' },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(37, 99, 235, 0.16)' },
            { offset: 1, color: 'rgba(37, 99, 235, 0)' }
          ]
        }
      },
      z: 2
    },
    {
      name: 'ROI',
      type: 'line',
      yAxisIndex: 1,
      data: props.points.map(point => point.roi),
      smooth: true,
      symbol: 'none',
      lineStyle: { width: 2, color: '#16A34A' },
      itemStyle: { color: '#16A34A' },
      z: 3
    }
  ],
  animationDuration: 600
}))
</script>

<template>
  <DashboardCard
    title="Business Performance Trend"
    subtitle="Revenue (Rp B), ROI (%), and active project volume"
    :padded="false"
  >
    <div class="h-80 min-w-0 px-3 pt-2 pb-2 lg:h-[140px]">
      <VChart
        :option="option"
        autoresize
      />
    </div>
  </DashboardCard>
</template>
