import type { DashboardKpi } from '../types/types'
import type {
  CommercialPipelineStage,
  ConversionTrendPoint,
  FeaturedPartnership,
  PartnershipStatusSlice
} from '../types/commercial.types'

export const commercialKpis: DashboardKpi[] = [
  {
    label: 'Revenue Pipeline',
    value: 'Rp 18.4B',
    delta: '+12.5%',
    deltaLabel: 'vs last quarter',
    trend: 'up',
    icon: 'i-lucide-wallet',
    progress: 78
  },
  {
    label: 'Active Prospects',
    value: '166',
    delta: '+18',
    deltaLabel: 'vs last quarter',
    trend: 'up',
    icon: 'i-lucide-users-round',
    progress: 62
  },
  {
    label: 'Conversion Rate',
    value: '24.5%',
    delta: '+3.2 pts',
    deltaLabel: 'vs last quarter',
    trend: 'up',
    icon: 'i-lucide-target',
    progress: 24
  }
]

export const salesPipeline: CommercialPipelineStage[] = [
  { label: 'Lead', opportunities: 72, value: 'Rp 7.0B', open: true, color: '#BFDBFE' },
  { label: 'Qualified', opportunities: 46, value: 'Rp 5.6B', open: true, color: '#93C5FD' },
  { label: 'Proposal', opportunities: 30, value: 'Rp 3.8B', open: true, color: '#60A5FA' },
  { label: 'Negotiation', opportunities: 18, value: 'Rp 2.0B', open: true, color: '#2563EB' },
  { label: 'Won', opportunities: 54, value: 'Rp 6.4B', open: false, color: '#16A34A' }
]

export const openSalesValue = 'Rp 18.4B'

export const partnershipStatus: PartnershipStatusSlice[] = [
  { label: 'New', value: 48, color: '#93C5FD' },
  { label: 'In Progress', value: 32, color: '#60A5FA' },
  { label: 'Negotiation', value: 18, color: '#2563EB' },
  { label: 'Won', value: 24, color: '#16A34A' },
  { label: 'Lost', value: 12, color: '#F43F5E' }
]

export const conversionTrend: ConversionTrendPoint[] = [
  { month: 'Jan', rate: 17.8 },
  { month: 'Feb', rate: 18.6 },
  { month: 'Mar', rate: 19.2 },
  { month: 'Apr', rate: 20.1 },
  { month: 'May', rate: 20.8 },
  { month: 'Jun', rate: 21.4 },
  { month: 'Jul', rate: 22.0 },
  { month: 'Aug', rate: 22.6 },
  { month: 'Sep', rate: 23.1 },
  { month: 'Oct', rate: 23.8 },
  { month: 'Nov', rate: 24.2 },
  { month: 'Dec', rate: 24.5 }
]

export const conversionTarget = 25

export const featuredPartnerships: FeaturedPartnership[] = [
  {
    id: 'p1',
    name: 'Fintech Integration Suite',
    client: 'Nusantara Finance',
    category: 'Banking',
    status: 'Negotiation',
    value: 'Rp 4.2B',
    progress: 65,
    image:
      'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=400&auto=format&fit=crop'
  },
  {
    id: 'p2',
    name: 'Supply Chain Analytics',
    client: 'PT Manufaktur Indonesia',
    category: 'Manufacturing',
    status: 'Proposal',
    value: 'Rp 3.1B',
    progress: 40,
    image:
      'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?q=80&w=400&auto=format&fit=crop'
  },
  {
    id: 'p3',
    name: 'Telemedicine Platform',
    client: 'MediCare Hospital',
    category: 'Healthcare',
    status: 'Won',
    value: 'Rp 5.6B',
    progress: 100,
    image:
      'https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?q=80&w=400&auto=format&fit=crop'
  },
  {
    id: 'p4',
    name: 'Smart Grid Partnership',
    client: 'Green Energy Corp',
    category: 'Energy',
    status: 'Qualified',
    value: 'Rp 2.8B',
    progress: 25,
    image:
      'https://images.unsplash.com/photo-1466611653911-95081537e5b7?q=80&w=400&auto=format&fit=crop'
  }
]
