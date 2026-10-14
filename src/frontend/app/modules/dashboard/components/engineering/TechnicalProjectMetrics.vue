<script setup lang="ts">
const metrics = [
  {
    title: 'Total Active Projects',
    value: '42',
    change: '+6.3%',
    trend: 'up',
    icon: 'i-lucide-layers',
    iconBg: 'bg-blue-50 text-blue-600'
  },
  {
    title: 'Completed Projects',
    value: '18',
    change: '+12.5%',
    trend: 'up',
    icon: 'i-lucide-check-circle-2',
    iconBg: 'bg-emerald-50 text-emerald-600'
  },
  {
    title: 'Average Project Performance',
    value: '78%',
    change: '+4.2%',
    trend: 'up',
    icon: 'i-lucide-clock',
    iconBg: 'bg-amber-50 text-amber-600'
  },
  {
    title: 'Average ROI',
    value: '24.8%',
    change: '+3.1%',
    trend: 'up',
    icon: 'i-lucide-bar-chart-2',
    iconBg: 'bg-purple-50 text-purple-600'
  }
]
</script>

<template>
  <div class="space-y-2">
    <h2 class="text-xs font-bold text-slate-900 tracking-tight">Technical Project Metrics</h2>

    <div class="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">
      <div
        v-for="item in metrics"
        :key="item.title"
        class="flex items-center gap-3.5 rounded-xl border border-slate-200/80 bg-white p-3.5 shadow-2xs"
      >
        <!-- Icon Container -->
        <div
          class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl font-bold"
          :class="item.iconBg"
        >
          <UIcon :name="item.icon" class="h-5 w-5" />
        </div>

        <!-- Info Value & Trend -->
        <div class="flex-1 min-w-0">
          <p class="text-[11px] font-semibold text-slate-500 truncate">
            {{ item.title }}
          </p>
          <div class="mt-0.5 flex items-baseline gap-2">
            <span class="text-xl font-bold text-slate-900 leading-tight">
              {{ item.value }}
            </span>
            <span class="inline-flex items-center text-[11px] font-semibold text-emerald-600">
              <UIcon name="i-lucide-arrow-up" class="h-3 w-3 mr-0.5" />
              {{ item.change }}
            </span>
            <span class="text-[10px] text-slate-400 hidden xl:inline"> vs last period </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
