<script setup lang="ts">
import type { ViewMode } from '../../types/types'

interface Props {
  totalCount: number
  currentView: ViewMode
  sortBy: string
}

defineProps<Props>()

const emit = defineEmits<{
  (e: 'update:currentView', mode: ViewMode): void
  (e: 'update:sortBy', sort: string): void
}>()

const sortOptions = [
  { label: 'Latest Updated', value: 'latest' },
  { label: 'Oldest Updated', value: 'oldest' },
  { label: 'Project Name (A-Z)', value: 'name_asc' },
  { label: 'Project Name (Z-A)', value: 'name_desc' }
]
</script>

<template>
  <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
    <!-- Total Counter -->
    <div class="text-sm font-bold text-slate-900">{{ totalCount }} Projects</div>

    <!-- Controls: Grid/Table Toggle & Sort By -->
    <div class="flex items-center gap-3">
      <!-- Grid / Table View Switcher -->
      <div class="inline-flex items-center rounded-lg border border-slate-200 bg-slate-50 p-0.5">
        <button
          type="button"
          class="inline-flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-xs font-semibold transition-all cursor-pointer"
          :class="[
            currentView === 'grid'
              ? 'bg-[#0B132B] text-white shadow-xs'
              : 'text-slate-600 hover:text-slate-900'
          ]"
          @click="emit('update:currentView', 'grid')"
        >
          <UIcon name="i-lucide-layout-grid" class="h-3.5 w-3.5" />
          <span>Grid</span>
        </button>

        <button
          type="button"
          class="inline-flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-xs font-semibold transition-all cursor-pointer"
          :class="[
            currentView === 'table'
              ? 'bg-[#0B132B] text-white shadow-xs'
              : 'text-slate-600 hover:text-slate-900'
          ]"
          @click="emit('update:currentView', 'table')"
        >
          <UIcon name="i-lucide-table-2" class="h-3.5 w-3.5" />
          <span>Table</span>
        </button>
      </div>

      <!-- Sort By Dropdown -->
      <div class="flex items-center gap-2">
        <span class="hidden text-xs text-slate-500 sm:inline">Sort by</span>
        <select
          :value="sortBy"
          class="h-8.5 rounded-lg border border-slate-200 bg-white px-3 text-xs font-medium text-slate-700 transition-colors focus:border-blue-500 focus:outline-none cursor-pointer"
          @change="emit('update:sortBy', ($event.target as HTMLSelectElement).value)"
        >
          <option v-for="opt in sortOptions" :key="opt.value" :value="opt.value">
            {{ opt.label }}
          </option>
        </select>
      </div>
    </div>
  </div>
</template>
