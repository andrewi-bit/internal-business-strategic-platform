<script setup lang="ts">
import { computed, ref } from 'vue'
import type { PartnerRowAction } from './partnership.types'
import { partners as allPartners, partnershipStats } from './partnership.data'
import { downloadPartnersCsv, usePartnershipList } from './usePartnershipList'
import PartnershipPageHeader from './PartnershipPageHeader.vue'
import PartnershipStats from './PartnershipStats.vue'
import PartnershipFilters from './PartnershipFilters.vue'
import PartnershipMoreFilters from './PartnershipMoreFilters.vue'
import PartnershipTable from './PartnershipTable.vue'
import PartnershipPagination from './PartnershipPagination.vue'

const toast = useToast()

const {
  filters,
  advanced,
  currentPage,
  pageSize,
  selectedIds,
  filteredPartners,
  paginatedPartners,
  allPageSelected,
  somePageSelected,
  selectedCount,
  advancedActiveCount,
  setPage,
  setPageSize,
  resetFilters,
  applyAdvanced,
  toggleRow,
  toggleAllOnPage,
  clearSelection
} = usePartnershipList()

const isMoreFiltersOpen = ref(false)

const updateFilters = (value: typeof filters.value) => {
  filters.value = value
}

const toggleMoreFilters = () => {
  isMoreFiltersOpen.value = !isMoreFiltersOpen.value
}

const handleApplyAdvanced = (value: typeof advanced.value) => {
  applyAdvanced(value)
  isMoreFiltersOpen.value = false
  toast.add({
    title: 'Filters applied',
    description: `${filteredPartners.value.length} partner(s) match the current filters.`,
    color: 'primary'
  })
}

const handleResetAll = () => {
  resetFilters()
}

const handleAddPartner = () => {
  toast.add({
    title: 'Add Partner',
    description: 'The Add Partner form is not available yet in this project.',
    color: 'primary'
  })
}

const handleExport = (scope: 'filtered' | 'all') => {
  const rows = scope === 'filtered' ? filteredPartners.value : allPartners
  downloadPartnersCsv(rows, scope === 'filtered' ? 'partners-filtered' : 'partners-all')
  toast.add({
    title: 'Export ready',
    description: `${rows.length} partner(s) exported to CSV.`,
    color: 'success'
  })
}

const handleRowAction = (payload: { action: PartnerRowAction, partner: (typeof allPartners)[number] }) => {
  const { action, partner } = payload
  if (action === 'view') {
    navigateTo(`/partnership/${partner.id}`)
    return
  }
  const labels: Record<Exclude<PartnerRowAction, 'view'>, string> = {
    edit: 'Edit Partner',
    renew: 'Renew Contract',
    delete: 'Delete Partner'
  }
  toast.add({
    title: labels[action],
    description: `"${partner.name}" — this action is not available yet.`,
    color: action === 'delete' ? 'error' : 'primary'
  })
}

const totalResults = computed(() => filteredPartners.value.length)
</script>

<template>
  <div class="space-y-1 lg:-mx-6 lg:-my-6 lg:px-3">
    <PartnershipPageHeader
      @add-partner="handleAddPartner"
      @export="handleExport"
    />

    <PartnershipStats :stats="partnershipStats" />

    <PartnershipFilters
      :model-value="filters"
      :advanced-active-count="advancedActiveCount"
      @update:model-value="updateFilters"
      @toggle-more="toggleMoreFilters"
      @reset="handleResetAll"
    />

    <PartnershipMoreFilters
      v-if="isMoreFiltersOpen"
      :model-value="advanced"
      @apply="handleApplyAdvanced"
      @close="isMoreFiltersOpen = false"
    />

    <div
      v-if="selectedCount > 0"
      class="flex items-center justify-between rounded-xl border border-blue-200 bg-blue-50 px-4 py-2"
    >
      <p class="text-xs font-semibold text-blue-700">
        {{ selectedCount }} partner(s) selected
      </p>
      <button
        type="button"
        class="text-xs font-semibold text-blue-700 transition-colors hover:text-blue-900 cursor-pointer"
        @click="clearSelection"
      >
        Clear selection
      </button>
    </div>

    <PartnershipTable
      :partners="paginatedPartners"
      :selected-ids="selectedIds"
      :all-page-selected="allPageSelected"
      :some-page-selected="somePageSelected"
      @toggle-row="toggleRow"
      @toggle-all="toggleAllOnPage"
      @action="handleRowAction"
    />

    <PartnershipPagination
      :current-page="currentPage"
      :page-size="pageSize"
      :total-items="totalResults"
      @update:current-page="setPage"
      @update:page-size="setPageSize"
    />
  </div>
</template>
