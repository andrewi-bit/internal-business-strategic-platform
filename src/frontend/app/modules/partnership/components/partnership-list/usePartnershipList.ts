import { computed, ref, watch } from 'vue'
import type {
  ContractEndPreset,
  LastUpdatedPreset,
  Partner,
  PartnershipAdvancedFilters,
  PartnershipFilterState
} from './partnership.types'
import {
  createAdvancedFilters,
  createPartnershipFilters,
  partners as allPartners
} from './partnership.data'

const toDateString = (date: Date) => date.toISOString().slice(0, 10)

const addDays = (base: Date, days: number) => {
  const date = new Date(base)
  date.setUTCDate(date.getUTCDate() + days)
  return toDateString(date)
}

export function usePartnershipList() {
  const filters = ref<PartnershipFilterState>(createPartnershipFilters())
  const advanced = ref<PartnershipAdvancedFilters>(createAdvancedFilters())
  const currentPage = ref(1)
  const pageSize = ref(10)
  const selectedIds = ref<string[]>([])

  const matchesSearch = (partner: Partner, keyword: string) => {
    const haystack = [
      partner.name,
      partner.id,
      partner.category,
      partner.industry,
      partner.expertise,
      partner.location,
      partner.status,
      partner.contractStatus,
      partner.partnerType
    ]
      .join(' ')
      .toLowerCase()
    return haystack.includes(keyword)
  }

  const matchesContractEnd = (partner: Partner, now: Date) => {
    const preset: ContractEndPreset = advanced.value.contractEndPreset
    if (preset === 'any') return true
    if (preset === 'custom') {
      const { contractEndStart, contractEndEnd } = advanced.value
      if (contractEndStart && partner.contractEndDate < contractEndStart) return false
      if (contractEndEnd && partner.contractEndDate > contractEndEnd) return false
      return true
    }
    const days = Number(preset)
    return partner.contractEndDate >= toDateString(now) && partner.contractEndDate <= addDays(now, days)
  }

  const matchesLastUpdated = (partner: Partner, now: Date) => {
    const preset: LastUpdatedPreset = advanced.value.lastUpdatedPreset
    if (preset === 'any') return true
    const updatedOn = partner.lastUpdated.slice(0, 10)
    if (preset === 'custom') {
      const { lastUpdatedStart, lastUpdatedEnd } = advanced.value
      if (lastUpdatedStart && updatedOn < lastUpdatedStart) return false
      if (lastUpdatedEnd && updatedOn > lastUpdatedEnd) return false
      return true
    }
    const days = Number(preset)
    return updatedOn >= addDays(now, -days)
  }

  const filteredPartners = computed(() => {
    const keyword = filters.value.search.trim().toLowerCase()
    const now = new Date()

    return allPartners.filter((partner) => {
      if (keyword && !matchesSearch(partner, keyword)) return false

      const { categories, statuses, contractStatuses, industries, expertises, locations } = filters.value
      if (categories.length && !categories.includes(partner.category)) return false
      if (statuses.length && !statuses.includes(partner.status)) return false
      if (contractStatuses.length && !contractStatuses.includes(partner.contractStatus)) return false
      if (industries.length && !industries.includes(partner.industry)) return false
      if (expertises.length && !expertises.includes(partner.expertise)) return false
      if (locations.length && !locations.includes(partner.location)) return false

      const { partnerTypes, activeProjectWith, activeProjectWithout } = advanced.value
      if (partnerTypes.length && !partnerTypes.includes(partner.partnerType)) return false
      if (activeProjectWith !== activeProjectWithout) {
        if (activeProjectWith && !partner.hasActiveProject) return false
        if (activeProjectWithout && partner.hasActiveProject) return false
      }

      if (!matchesContractEnd(partner, now)) return false
      if (!matchesLastUpdated(partner, now)) return false

      return true
    })
  })

  const totalPages = computed(() => Math.max(1, Math.ceil(filteredPartners.value.length / pageSize.value)))

  const paginatedPartners = computed(() => {
    const start = (currentPage.value - 1) * pageSize.value
    return filteredPartners.value.slice(start, start + pageSize.value)
  })

  const pageIds = computed(() => paginatedPartners.value.map(partner => partner.id))

  const allPageSelected = computed(
    () => pageIds.value.length > 0 && pageIds.value.every(id => selectedIds.value.includes(id))
  )

  const somePageSelected = computed(
    () => pageIds.value.some(id => selectedIds.value.includes(id)) && !allPageSelected.value
  )

  const selectedCount = computed(() => selectedIds.value.length)

  const advancedActiveCount = computed(() => {
    let count = 0
    if (advanced.value.contractEndPreset !== 'any') count += 1
    if (advanced.value.lastUpdatedPreset !== 'any') count += 1
    if (advanced.value.partnerTypes.length > 0) count += 1
    if (advanced.value.activeProjectWith !== advanced.value.activeProjectWithout) count += 1
    return count
  })

  watch([totalPages, pageSize], () => {
    if (currentPage.value > totalPages.value) currentPage.value = totalPages.value
    if (currentPage.value < 1) currentPage.value = 1
  })

  const setPage = (page: number) => {
    currentPage.value = page
  }

  const setPageSize = (size: number) => {
    pageSize.value = size
    currentPage.value = 1
  }

  const resetFilters = () => {
    filters.value = createPartnershipFilters()
    currentPage.value = 1
  }

  const applyAdvanced = (value: PartnershipAdvancedFilters) => {
    advanced.value = { ...value, partnerTypes: [...value.partnerTypes] }
    currentPage.value = 1
  }

  const resetAdvanced = () => {
    advanced.value = createAdvancedFilters()
    currentPage.value = 1
  }

  const toggleRow = (id: string) => {
    selectedIds.value = selectedIds.value.includes(id)
      ? selectedIds.value.filter(item => item !== id)
      : [...selectedIds.value, id]
  }

  const toggleAllOnPage = () => {
    if (allPageSelected.value) {
      selectedIds.value = selectedIds.value.filter(id => !pageIds.value.includes(id))
    } else {
      selectedIds.value = [...new Set([...selectedIds.value, ...pageIds.value])]
    }
  }

  const clearSelection = () => {
    selectedIds.value = []
  }

  return {
    filters,
    advanced,
    currentPage,
    pageSize,
    selectedIds,
    filteredPartners,
    paginatedPartners,
    totalPages,
    pageIds,
    allPageSelected,
    somePageSelected,
    selectedCount,
    advancedActiveCount,
    setPage,
    setPageSize,
    resetFilters,
    applyAdvanced,
    resetAdvanced,
    toggleRow,
    toggleAllOnPage,
    clearSelection
  }
}

export function downloadPartnersCsv(rows: Partner[], filename = 'partners') {
  const headers = [
    'Partner ID',
    'Partner Name',
    'Partnership Category',
    'Industry',
    'Expertise',
    'Location',
    'Partnership Status',
    'Contract Status',
    'Contract End Date',
    'Last Updated',
    'Partner Type',
    'Active Project'
  ]

  const escape = (value: string) => `"${value.replace(/"/g, '""')}"`

  const lines = rows.map(partner =>
    [
      partner.id,
      partner.name,
      partner.category,
      partner.industry,
      partner.expertise,
      partner.location,
      partner.status,
      partner.contractStatus,
      partner.contractEndDate,
      partner.lastUpdated,
      partner.partnerType,
      partner.hasActiveProject ? 'Yes' : 'No'
    ]
      .map(value => escape(String(value)))
      .join(',')
  )

  const csv = [headers.map(escape).join(','), ...lines].join('\r\n')
  const blob = new Blob([`\uFEFF${csv}`], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `${filename}-${toDateString(new Date())}.csv`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}
