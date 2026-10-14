<script setup lang="ts">
import { ref } from 'vue'
import type { PortfolioFilterState } from '../../types/types'

const filters = ref<PortfolioFilterState>({
  search: '',
  industry: '',
  technology: '',
  year: '',
  status: ''
})

const emit = defineEmits<{
  (e: 'filter-change', filters: PortfolioFilterState): void
  (e: 'reset'): void
}>()

// Opsi filter dummy
const industryOptions = [
  { label: 'All Industries', value: '' },
  { label: 'Banking', value: 'Banking' },
  { label: 'Manufacturing', value: 'Manufacturing' },
  { label: 'Retail', value: 'Retail' },
  { label: 'Healthcare', value: 'Healthcare' },
  { label: 'Logistics', value: 'Logistics' },
  { label: 'Government', value: 'Government' },
  { label: 'Energy', value: 'Energy' }
]

const technologyOptions = [
  { label: 'All Technologies', value: '' },
  { label: 'Web', value: 'Web' },
  { label: 'Mobile', value: 'Mobile' },
  { label: 'IoT', value: 'IoT' },
  { label: 'Cloud', value: 'Cloud' },
  { label: 'Analytics', value: 'Analytics' },
  { label: 'Fintech', value: 'Fintech' }
]

const yearOptions = [
  { label: 'All Years', value: '' },
  { label: '2026', value: '2026' },
  { label: '2025', value: '2025' },
  { label: '2024', value: '2024' },
  { label: '2023', value: '2023' }
]

const statusOptions = [
  { label: 'All Statuses', value: '' },
  { label: 'Completed', value: 'Completed' },
  { label: 'Active', value: 'Active' },
  { label: 'On Going', value: 'On Going' },
  { label: 'Planned', value: 'Planned' },
  { label: 'Cancelled', value: 'Cancelled' }
]

const handleSearch = () => {
  emit('filter-change', { ...filters.value })
}

const handleReset = () => {
  filters.value = {
    search: '',
    industry: '',
    technology: '',
    year: '',
    status: ''
  }
  emit('reset')
}
</script>

<template>
  <div class="flex flex-wrap items-center gap-3">
    <!-- Search Input -->
    <div class="relative min-w-[260px] flex-1">
      <div
        class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400"
      >
        <UIcon name="i-lucide-search" class="h-4 w-4" />
      </div>
      <input
        v-model="filters.search"
        type="text"
        placeholder="Search project name, client, or keyword..."
        class="w-full rounded-lg border border-slate-200 bg-white py-2 pr-4 pl-9 text-sm text-slate-800 placeholder-slate-400 transition-colors focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        @input="handleSearch"
      />
    </div>

    <!-- Filter Dropdowns -->
    <div class="flex flex-wrap items-center gap-2.5">
      <!-- Industry Select -->
      <select
        v-model="filters.industry"
        class="h-9.5 rounded-lg border border-slate-200 bg-white px-3 text-xs font-medium text-slate-700 transition-colors focus:border-blue-500 focus:outline-none cursor-pointer"
        @change="handleSearch"
      >
        <option value="" disabled hidden>Industry</option>
        <option v-for="opt in industryOptions" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>

      <!-- Technology Select -->
      <select
        v-model="filters.technology"
        class="h-9.5 rounded-lg border border-slate-200 bg-white px-3 text-xs font-medium text-slate-700 transition-colors focus:border-blue-500 focus:outline-none cursor-pointer"
        @change="handleSearch"
      >
        <option value="" disabled hidden>Technology</option>
        <option v-for="opt in technologyOptions" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>

      <!-- Year Select -->
      <select
        v-model="filters.year"
        class="h-9.5 rounded-lg border border-slate-200 bg-white px-3 text-xs font-medium text-slate-700 transition-colors focus:border-blue-500 focus:outline-none cursor-pointer"
        @change="handleSearch"
      >
        <option value="" disabled hidden>Year</option>
        <option v-for="opt in yearOptions" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>

      <!-- Status Select -->
      <select
        v-model="filters.status"
        class="h-9.5 rounded-lg border border-slate-200 bg-white px-3 text-xs font-medium text-slate-700 transition-colors focus:border-blue-500 focus:outline-none cursor-pointer"
        @change="handleSearch"
      >
        <option value="" disabled hidden>Status</option>
        <option v-for="opt in statusOptions" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>

      <!-- Reset Button -->
      <button
        type="button"
        class="inline-flex h-9.5 items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-3 text-xs font-medium text-slate-700 transition-colors hover:bg-slate-50 active:bg-slate-100 cursor-pointer"
        @click="handleReset"
      >
        <UIcon name="i-lucide-rotate-ccw" class="h-3.5 w-3.5 text-slate-500" />
        <span>Reset</span>
      </button>
    </div>
  </div>
</template>
