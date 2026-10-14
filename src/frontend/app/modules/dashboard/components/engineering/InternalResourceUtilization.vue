<script setup lang="ts">
const teams = [
  {
    name: 'Frontend',
    rate: 84,
    members: '7 / 10 members',
    icon: 'i-lucide-user',
    iconBg: 'bg-blue-50 text-blue-600',
    barColor: 'bg-blue-500'
  },
  {
    name: 'Backend',
    rate: 76,
    members: '8 / 11 members',
    icon: 'i-lucide-server',
    iconBg: 'bg-emerald-50 text-emerald-600',
    barColor: 'bg-emerald-500'
  },
  {
    name: 'QA',
    rate: 91,
    members: '10 / 11 members',
    icon: 'i-lucide-shield-check',
    iconBg: 'bg-purple-50 text-purple-600',
    barColor: 'bg-purple-500'
  },
  {
    name: 'DevOps',
    rate: 68,
    members: '4 / 6 members',
    icon: 'i-lucide-cloud',
    iconBg: 'bg-amber-50 text-amber-600',
    barColor: 'bg-amber-500'
  }
]
</script>

<template>
  <div class="space-y-2">
    <!-- Header Section -->
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-xs font-bold text-slate-900 tracking-tight">
          Internal Resource Utilization
        </h2>
        <p class="text-[11px] text-slate-400">Utilization rate by internal team</p>
      </div>

      <div
        class="inline-flex items-center gap-1 rounded-md border border-slate-200 bg-white px-2 py-1 text-[11px] font-semibold text-slate-700 cursor-pointer hover:bg-slate-50"
      >
        <span>This Month</span>
        <UIcon name="i-lucide-chevron-down" class="h-3 w-3 text-slate-400" />
      </div>
    </div>

    <!-- 4 Team Cards Grid -->
    <div class="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">
      <div
        v-for="item in teams"
        :key="item.name"
        class="flex flex-col justify-between rounded-xl border border-slate-200/80 bg-white p-3.5 shadow-2xs"
      >
        <div class="flex items-center gap-3">
          <!-- Team Icon -->
          <div
            class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg font-bold"
            :class="item.iconBg"
          >
            <UIcon :name="item.icon" class="h-4.5 w-4.5" />
          </div>

          <!-- Team Name & Rate -->
          <div class="flex-1">
            <p class="text-[11px] font-semibold text-slate-500">
              {{ item.name }}
            </p>
            <p class="text-lg font-bold text-slate-900 leading-tight">{{ item.rate }}%</p>
          </div>
        </div>

        <!-- Progress Bar & Member Count -->
        <div class="mt-2.5 space-y-1">
          <div class="h-1.5 w-full overflow-hidden rounded-full bg-slate-100">
            <div
              class="h-full rounded-full transition-all duration-500"
              :class="item.barColor"
              :style="{ width: `${item.rate}%` }"
            />
          </div>
          <p class="text-[10px] text-slate-400 font-medium">
            {{ item.members }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
