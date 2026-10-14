import type { UserRole } from '../modules/dashboard/types/types'

export const dashboardRoleOptions: { label: string, value: UserRole }[] = [
  { label: 'Executive', value: 'executive' },
  { label: 'Commercial', value: 'commercial' },
  { label: 'Engineering', value: 'engineering' }
]

export function useDashboardRole() {
  const activeRole = useState<UserRole>('dashboard-active-role', () => 'executive')

  return { activeRole, dashboardRoleOptions }
}
