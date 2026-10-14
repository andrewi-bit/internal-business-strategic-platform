<script setup lang="ts">
import type { ProjectStatus } from '../../types/types'

interface Props {
  status: ProjectStatus
  client: string
  period: string
  projectValue: string
  location: string
  teamSize: string
  lastUpdated: string
}

defineProps<Props>()
</script>

<template>
  <div class="space-y-4 rounded-2xl border border-slate-200/80 bg-white p-5 shadow-2xs">
    <!-- Header Card -->
    <div class="flex items-center justify-between border-b border-slate-100 pb-3">
      <h3 class="text-sm font-bold text-slate-900">Project Status</h3>
      <span
        class="inline-flex items-center gap-1.5 rounded-full border border-emerald-200 bg-emerald-50 px-2.5 py-0.5 text-xs font-semibold text-emerald-700"
      >
        <span class="h-1.5 w-1.5 rounded-full bg-emerald-500" />
        <span>{{ status }}</span>
      </span>
    </div>

    <!-- Metadata Rows -->
    <div class="space-y-3 text-xs">
      <div class="flex items-start justify-between gap-2">
        <div class="flex items-center gap-2 text-slate-400 font-medium">
          <UIcon name="i-lucide-user" class="h-4 w-4 shrink-0 text-slate-400" />
          <span>Client</span>
        </div>
        <span class="font-semibold text-slate-800 text-right">{{ client }}</span>
      </div>

      <div class="flex items-start justify-between gap-2">
        <div class="flex items-center gap-2 text-slate-400 font-medium">
          <UIcon name="i-lucide-calendar" class="h-4 w-4 shrink-0 text-slate-400" />
          <span>Project Period</span>
        </div>
        <span class="font-semibold text-slate-800 text-right">{{ period }}</span>
      </div>

      <div class="flex items-start justify-between gap-2">
        <div class="flex items-center gap-2 text-slate-400 font-medium">
          <UIcon name="i-lucide-circle-dollar-sign" class="h-4 w-4 shrink-0 text-slate-400" />
          <span>Project Value</span>
        </div>
        <span class="font-semibold text-slate-800 text-right">{{ projectValue }}</span>
      </div>

      <div class="flex items-start justify-between gap-2">
        <div class="flex items-center gap-2 text-slate-400 font-medium">
          <UIcon name="i-lucide-map-pin" class="h-4 w-4 shrink-0 text-slate-400" />
          <span>Location</span>
        </div>
        <span class="font-semibold text-slate-800 text-right">{{ location }}</span>
      </div>

      <div class="flex items-start justify-between gap-2">
        <div class="flex items-center gap-2 text-slate-400 font-medium">
          <UIcon name="i-lucide-users" class="h-4 w-4 shrink-0 text-slate-400" />
          <span>Team Size</span>
        </div>
        <span class="font-semibold text-slate-800 text-right">{{ teamSize }}</span>
      </div>

      <div class="flex items-start justify-between gap-2">
        <div class="flex items-center gap-2 text-slate-400 font-medium">
          <UIcon name="i-lucide-clock" class="h-4 w-4 shrink-0 text-slate-400" />
          <span>Last Updated</span>
        </div>
        <span class="font-semibold text-slate-800 text-right">{{ lastUpdated }}</span>
      </div>
    </div>
  </div>
</template>
