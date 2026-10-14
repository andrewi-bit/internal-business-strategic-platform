export type PartnerStatus = 'Active' | 'Under Review' | 'Draft' | 'Expired' | 'Terminated'
export type ContractStatus = 'Active' | 'Expiring Soon' | 'Expired'
export type PartnerCategory =
  | 'Technology Partner'
  | 'Channel Partner'
  | 'Service Partner'
  | 'Marketing Partner'
export type ContactType = 'Primary' | 'Technical' | 'Commercial'

export interface KeyContact {
  id: string
  name: string
  initials: string
  position: string
  email: string
  phone: string
  type: ContactType
}

export interface CollaborationProject {
  id: string
  name: string
  code: string
  contribution: string
  status: 'In Progress' | 'Completed' | 'Pending'
  startDate: string
  endDate: string
}

export interface PartnerEvaluation {
  overallScore: number
  ratingLabel: string
  evaluationDate: string
  evaluator: string
  recommendation: string
  nextEvaluation: string
  remarks: string
}

export interface PartnerDetailItem {
  id: string
  code: string
  name: string
  legalName: string
  logo: string
  status: PartnerStatus
  partnershipSince: string
  category: PartnerCategory
  tags: string[]
  contract: {
    status: ContractStatus
    validUntil: string
    remainingTime: string
  }
  companyOverview: {
    website: string
    headquarters: string
    industry: string
    businessFocus: string
    keyMarkets: string[]
    description: string
  }
  keyExpertise: {
    name: string
    icon: string
  }[]
  keyContacts: KeyContact[]
  quickInfo: {
    partnerType: string
    hasActiveProject: boolean
    activeProjectsCount: number
    lastEvaluation: string
    nextEvaluation: string
  }
  recentCollaborations: CollaborationProject[]
  latestEvaluation: PartnerEvaluation
}
