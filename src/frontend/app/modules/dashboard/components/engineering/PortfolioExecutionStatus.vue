<script setup lang="ts">
import { ref } from 'vue'

const statusData = [
  { name: 'Completed', count: 17, percentage: '40%', color: '#3b82f6', dotClass: 'bg-blue-500' },
  { name: 'On Going', count: 18, percentage: '43%', color: '#10b981', dotClass: 'bg-emerald-500' },
  { name: 'Planned', count: 5, percentage: '12%', color: '#f59e0b', dotClass: 'bg-amber-500' },
  { name: 'Delayed', count: 2, percentage: '5%', color: '#ef4444', dotClass: 'bg-rose-500' }
]

// Konfigurasi Apache ECharts Donut Chart
const chartOption = ref({
  tooltip: {
    trigger: 'item',
    formatter: '{b}: {c} ({d}%)'
  },
  series: [
    {
      name: 'Status',
      type: 'pie',
      radius: ['60%', '85%'],
      center: ['50%', '50%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 4,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: false
      },
      emphasis: {
        scale: true,
        scaleSize: 5
      },
      data: statusData.map((item) => ({
        name: item.name,
        value: item.count,
        itemStyle: { color: item.color }
      }))
    }
  ]
})
</script>

<template>
  <div class="flex h-full flex-col rounded-xl border border-slate-200/80 bg-white p-4 shadow-2xs">
    <!-- Header Card -->
    <div class="flex items-center justify-between pb-2 border-b border-slate-100">
      <div>
        <h3 class="text-xs font-bold text-slate-900 tracking-tight">Portfolio Execution Status</h3>
        <p class="text-[11px] text-slate-400">Project distribution by current status</p>
      </div>

      <div
        class="inline-flex items-center gap-1 rounded-md border border-slate-200 bg-white px-2 py-1 text-[11px] font-semibold text-slate-700 cursor-pointer hover:bg-slate-50"
      >
        <span>All Projects</span>
        <UIcon name="i-lucide-chevron-down" class="h-3 w-3 text-slate-400" />
      </div>
    </div>

    <!-- Content: Donut Chart + Legend -->
    <div class="mt-2 flex flex-1 items-center justify-between gap-4">
      <!-- Donut Chart Container dengan center text overlay -->
      <div class="relative h-36 w-36 shrink-0 sm:h-40 sm:w-40">
        <VChart :option="chartOption" class="h-full w-full" autoresize />
        <!-- Center Label Overlay -->
        <div
          class="pointer-events-none absolute inset-0 flex flex-col items-center justify-center text-center"
        >
          <span class="text-lg font-extrabold text-slate-900 leading-tight">42</span>
          <span class="text-[10px] font-medium text-slate-400">Projects</span>
        </div>
      </div>

      <!-- Legend List -->
      <div class="flex-1 space-y-2 pr-2">
        <div
          v-for="item in statusData"
          :key="item.name"
          class="flex items-center justify-between text-xs"
        >
          <div class="flex items-center gap-2">
            <span class="h-2 w-2 rounded-full" :class="item.dotClass" />
            <span class="font-medium text-slate-600">{{ item.name }}</span>
          </div>
          <div class="flex items-center gap-3">
            <span class="font-bold text-slate-900">{{ item.count }}</span>
            <span class="w-8 text-right text-slate-400 font-medium">{{ item.percentage }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
