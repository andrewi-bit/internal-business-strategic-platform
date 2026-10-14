export type CommercialStatus = 'Lead' | 'Qualified' | 'Proposal' | 'Negotiation' | 'Won' | 'Lost' | 'New' | 'In Progress'

export interface CommercialPipelineStage {
  label: string
  opportunities: number
  value: string
  open: boolean
  color: string
}

export interface PartnershipStatusSlice {
  label: 'New' | 'In Progress' | 'Negotiation' | 'Won' | 'Lost'
  value: number
  color: string
}

export interface ConversionTrendPoint {
  month: string
  rate: number
}

export interface FeaturedPartnership {
  id: string
  name: string
  client: string
  category: string
  status: CommercialStatus
  value: string
  progress: number
  image: string
}
