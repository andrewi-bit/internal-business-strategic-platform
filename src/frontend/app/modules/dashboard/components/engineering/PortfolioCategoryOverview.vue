<script setup lang="ts">
import { ref } from 'vue'

const categories = ['Others', 'Energy', 'Healthcare', 'Retail', 'Manufacturing', 'Banking']
const counts = [3, 3, 4, 6, 8, 18]

// Konfigurasi ECharts Horizontal Bar Chart
const chartOption = ref({
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'shadow' }
  },
  grid: {
    top: 5,
    bottom: 5,
    left: 85,
    right: 35
  },
  xAxis: {
    type: 'value',
    show: false
  },
  yAxis: {
    type: 'category',
    data: categories,
    axisLine: { show: false },
    axisTick: { show: false },
    axisLabel: {
      fontSize: 11,
      color: '#64748b',
      fontWeight: 500
    }
  },
  series: [
    {
      name: 'Projects',
      type: 'bar',
      barWidth: 10,
      data: counts,
      showBackground: true,
      backgroundStyle: {
        color: '#f8fafc',
        borderRadius: 4
      },
      itemStyle: {
        color: '#3b82f6',
        borderRadius: [0, 4, 4, 0]
      },
      label: {
        show: true,
        position: 'right',
        fontSize: 11,
        fontWeight: 'bold',
        color: '#1e293b'
      }
    }
  ]
})
</script>

<template>
  <div class="flex h-full flex-col rounded-xl border border-slate-200/80 bg-white p-4 shadow-2xs">
    <!-- Header Card -->
    <div class="flex items-center justify-between pb-2 border-b border-slate-100">
      <div>
        <h3 class="text-xs font-bold text-slate-900 tracking-tight">Portfolio Overview</h3>
        <p class="text-[11px] text-slate-400">Project distribution by category</p>
      </div>

      <div
        class="inline-flex items-center gap-1 rounded-md border border-slate-200 bg-white px-2 py-1 text-[11px] font-semibold text-slate-700 cursor-pointer hover:bg-slate-50"
      >
        <span>By Project Count</span>
        <UIcon name="i-lucide-chevron-down" class="h-3 w-3 text-slate-400" />
      </div>
    </div>

    <!-- Chart Container -->
    <div class="mt-2 flex-1 min-h-[140px] w-full">
      <VChart :option="chartOption" class="h-full w-full" autoresize />
    </div>
  </div>
</template>
