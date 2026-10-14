<script setup lang="ts">
import { ref } from 'vue'

const selectedPeriod = ref('Jan 2026 – Dec 2026')
</script>

<template>
  <div class="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
    <div>
      <h1 class="text-xl font-bold tracking-tight text-slate-900">Engineering Dashboard</h1>
      <p class="text-xs text-slate-500">
        Overview of technical project metrics, portfolio execution status, and internal resource
        utilization
      </p>
    </div>

    <!-- Date Range Filter Pill -->
    <div
      class="inline-flex items-center gap-2 rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700 shadow-2xs transition-colors hover:bg-slate-50 cursor-pointer"
    >
      <UIcon name="i-lucide-calendar" class="h-4 w-4 text-slate-500" />
      <span>{{ selectedPeriod }}</span>
      <UIcon name="i-lucide-chevron-down" class="h-3.5 w-3.5 text-slate-400" />
    </div>
  </div>
</template>
