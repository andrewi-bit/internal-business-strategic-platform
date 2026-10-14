import { computed } from 'vue'
import type { DashboardDateRange } from '../modules/dashboard/types/types'
import { dashboardDateRanges, performanceTrend } from '../modules/dashboard/data/executive.data'

export function useDashboardRange() {
  const selectedRange = useState<DashboardDateRange>('dashboard-date-range', () => '12m')

  const selectedRangeLabel = computed(
    () => dashboardDateRanges.find(range => range.value === selectedRange.value)?.label ?? ''
  )

  const rangeMenuItems = computed(() =>
    dashboardDateRanges.map(range => ({
      label: range.label,
      checked: selectedRange.value === range.value,
      onSelect: () => {
        selectedRange.value = range.value
      }
    }))
  )

  const visibleTrend = computed(() => {
    const months = dashboardDateRanges.find(range => range.value === selectedRange.value)?.months ?? 12
    return performanceTrend.slice(-months)
  })

  return { selectedRange, selectedRangeLabel, rangeMenuItems, visibleTrend }
}
