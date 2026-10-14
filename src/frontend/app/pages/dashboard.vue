<script setup lang="ts">
import ExecutiveDashboard from '../modules/dashboard/components/executive/ExecutiveDashboardView.vue'
import CommercialDashboard from '../modules/dashboard/components/commercial/CommercialDashboardView.vue'
import EngineeringDashboard from '../modules/dashboard/components/engineering/EngineeringDashboardView.vue'

const { activeRole, dashboardRoleOptions } = useDashboardRole()
const { selectedRangeLabel, rangeMenuItems } = useDashboardRange()
</script>

<template>
  <div class="flex flex-col gap-2">
    <!-- Page Header + Role Switcher -->
    <div class="flex shrink-0 items-center justify-between gap-3">
      <div class="min-w-0 flex-1">
        <div
          v-if="activeRole === 'executive'"
          class="flex min-w-0 items-baseline gap-2"
        >
          <h1 class="shrink-0 text-xl leading-7 font-bold tracking-tight text-slate-900">
            Executive Dashboard
          </h1>
          <p class="min-w-0 truncate text-xs leading-4 text-slate-500">
            Performance, portfolio, and pipeline at a glance.
          </p>
        </div>
      </div>

      <div class="flex shrink-0 items-center gap-2">
        <div class="inline-flex rounded-lg bg-slate-100 p-0.5">
          <button
            v-for="role in dashboardRoleOptions"
            :key="role.value"
            type="button"
            class="rounded-md px-2.5 py-1 text-[11px] leading-4 font-semibold transition-colors cursor-pointer"
            :class="[
              activeRole === role.value
                ? 'bg-white text-slate-900 shadow-xs'
                : 'text-slate-500 hover:text-slate-700'
            ]"
            @click="activeRole = role.value"
          >
            {{ role.label }}
          </button>
        </div>

        <UDropdownMenu
          v-if="activeRole === 'executive'"
          :items="rangeMenuItems"
          :content="{ align: 'end' }"
        >
          <button
            type="button"
            class="inline-flex h-8 items-center gap-2 rounded-lg border border-slate-200 bg-white px-3 text-sm font-medium text-slate-700 shadow-xs transition-colors hover:bg-slate-50 cursor-pointer"
          >
            <UIcon
              name="i-lucide-calendar-days"
              class="h-4 w-4 text-slate-400"
            />
            <span>{{ selectedRangeLabel }}</span>
            <UIcon
              name="i-lucide-chevron-down"
              class="h-4 w-4 text-slate-400"
            />
          </button>
        </UDropdownMenu>
      </div>
    </div>

    <ExecutiveDashboard v-if="activeRole === 'executive'" />
    <CommercialDashboard v-else-if="activeRole === 'commercial'" />
    <EngineeringDashboard v-else-if="activeRole === 'engineering'" />
  </div>
</template>
