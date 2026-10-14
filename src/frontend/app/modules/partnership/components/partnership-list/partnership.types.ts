export type PartnershipCategory
  = | 'Technology Partner'
    | 'Channel Partner'
    | 'Service Partner'
    | 'Marketing Partner'

export type PartnershipStatus = 'Draft' | 'Under Review' | 'Active' | 'Expired' | 'Terminated'

export type ContractStatus = 'Active' | 'Pending' | 'Expired' | 'Terminated'

export type PartnerType
  = | 'Strategic Partner'
    | 'Implementation Partner'
    | 'Consulting Partner'
    | 'Reseller'
    | 'Technology Provider'
    | 'Other'

export interface Partner {
  id: string
  name: string
  logo?: string
  category: PartnershipCategory
  industry: string
  expertise: string
  location: string
  status: PartnershipStatus
  contractStatus: ContractStatus
  contractEndDate: string
  lastUpdated: string
  partnerType: PartnerType
  hasActiveProject: boolean
}

export interface FilterOption {
  label: string
  value: string
}

export type StatTone = 'blue' | 'emerald' | 'amber' | 'orange' | 'rose'

export interface PartnershipStat {
  key: string
  label: string
  value: number
  icon: string
  tone: StatTone
  hint?: string
}

export interface PartnershipFilterState {
  search: string
  categories: string[]
  statuses: string[]
  contractStatuses: string[]
  industries: string[]
  expertises: string[]
  locations: string[]
}

export type ContractEndPreset = 'any' | '30' | '90' | '180' | 'custom'
export type LastUpdatedPreset = 'any' | '7' | '30' | '90' | 'custom'

export interface PartnershipAdvancedFilters {
  contractEndPreset: ContractEndPreset
  contractEndStart: string
  contractEndEnd: string
  lastUpdatedPreset: LastUpdatedPreset
  lastUpdatedStart: string
  lastUpdatedEnd: string
  partnerTypes: string[]
  activeProjectWith: boolean
  activeProjectWithout: boolean
}

export type PartnerRowAction = 'view' | 'edit' | 'renew' | 'delete'
