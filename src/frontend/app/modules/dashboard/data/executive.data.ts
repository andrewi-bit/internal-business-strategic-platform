import type {
  CategoryMetric,
  DashboardDateRange,
  DashboardKpi,
  FeaturedProject,
  PipelineStage,
  StatusSlice,
  TrendPoint
} from '../types/types'

export const dashboardDateRanges: { label: string, value: DashboardDateRange, months: number }[] = [
  { label: 'This Quarter', value: '3m', months: 3 },
  { label: 'Last 6 Months', value: '6m', months: 6 },
  { label: 'Last 12 Months', value: '12m', months: 12 }
]

export const executiveKpis: DashboardKpi[] = [
  {
    label: 'Active Projects',
    value: '128',
    delta: '+12',
    deltaLabel: 'vs last quarter',
    trend: 'up',
    icon: 'i-lucide-folder-kanban'
  },
  {
    label: 'Average ROI',
    value: '24.8%',
    delta: '+2.4 pts',
    deltaLabel: 'vs last quarter',
    trend: 'up',
    icon: 'i-lucide-trending-up'
  },
  {
    label: 'Revenue Pipeline',
    value: 'Rp 12.8B',
    delta: '+8.2%',
    deltaLabel: 'vs last quarter',
    trend: 'up',
    icon: 'i-lucide-wallet'
  },
  {
    label: 'Portfolio Health',
    value: '87%',
    delta: '+4 pts',
    deltaLabel: 'vs last quarter',
    trend: 'up',
    icon: 'i-lucide-heart-pulse',
    progress: 87
  }
]

export const performanceTrend: TrendPoint[] = [
  { month: 'Jan', revenue: 8.4, roi: 19.2, projects: 96 },
  { month: 'Feb', revenue: 9.1, roi: 20.1, projects: 99 },
  { month: 'Mar', revenue: 8.7, roi: 19.6, projects: 101 },
  { month: 'Apr', revenue: 10.2, roi: 21.4, projects: 104 },
  { month: 'May', revenue: 11.4, roi: 22.0, projects: 108 },
  { month: 'Jun', revenue: 10.9, roi: 21.6, projects: 110 },
  { month: 'Jul', revenue: 12.1, roi: 22.8, projects: 113 },
  { month: 'Aug', revenue: 12.6, roi: 23.4, projects: 116 },
  { month: 'Sep', revenue: 11.8, roi: 23.0, projects: 119 },
  { month: 'Oct', revenue: 13.4, roi: 24.1, projects: 122 },
  { month: 'Nov', revenue: 14.2, roi: 24.4, projects: 125 },
  { month: 'Dec', revenue: 15.1, roi: 24.8, projects: 128 }
]

export const portfolioStatus: StatusSlice[] = [
  { label: 'Active', value: 128, color: '#2563EB' },
  { label: 'Completed', value: 96, color: '#16A34A' },
  { label: 'On Going', value: 46, color: '#F59E0B' },
  { label: 'Planned', value: 30, color: '#94A3B8' }
]

export const topCategories: CategoryMetric[] = [
  { label: 'Banking', projects: 32, share: 25.0, roi: 29.0 },
  { label: 'Manufacturing', projects: 24, share: 18.8, roi: 22.5 },
  { label: 'Healthcare', projects: 19, share: 14.8, roi: 27.0 },
  { label: 'Retail', projects: 17, share: 13.3, roi: 20.0 },
  { label: 'Energy', projects: 14, share: 10.9, roi: 31.5 },
  { label: 'Others', projects: 22, share: 17.2, roi: 18.5 }
]

export const revenuePipeline: PipelineStage[] = [
  { label: 'Prospect', opportunities: 148, value: 'Rp 4.6B', open: true, color: '#BFDBFE' },
  { label: 'Qualified', opportunities: 92, value: 'Rp 3.8B', open: true, color: '#93C5FD' },
  { label: 'Proposal', opportunities: 54, value: 'Rp 2.7B', open: true, color: '#60A5FA' },
  { label: 'Negotiation', opportunities: 31, value: 'Rp 1.7B', open: true, color: '#2563EB' },
  { label: 'Won', opportunities: 18, value: 'Rp 5.2B', open: false, color: '#16A34A' }
]

export const openPipelineValue = 'Rp 12.8B'
export const averageRoi = 24.8
export const activeProjectsTotal = 128

export const featuredProjects: FeaturedProject[] = [
  {
    id: 'f1',
    title: 'Digital Banking Transformation',
    client: 'ABC Bank',
    description: 'End-to-end digital banking platform for improved customer experience.',
    industry: 'Banking',
    technologies: ['Web', 'Fintech'],
    status: 'Completed',
    image:
      'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=600&auto=format&fit=crop',
    updatedAt: '2 days ago',
    roi: '34.2%',
    duration: '14 months'
  },
  {
    id: 'f2',
    title: 'Smart Manufacturing Platform',
    client: 'PT. Manufaktur Indonesia',
    description: 'IoT-based manufacturing monitoring and predictive maintenance platform.',
    industry: 'Manufacturing',
    technologies: ['IoT', 'Analytics'],
    status: 'Active',
    image:
      'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?q=80&w=600&auto=format&fit=crop',
    updatedAt: '5 days ago',
    roi: '26.5%',
    duration: '10 months'
  },
  {
    id: 'f3',
    title: 'Healthcare Management System',
    client: 'MediCare Hospital',
    description: 'Patient management and resource allocation system for healthcare providers.',
    industry: 'Healthcare',
    technologies: ['IoT', 'Mobile', 'SaaS'],
    status: 'Completed',
    image:
      'https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?q=80&w=600&auto=format&fit=crop',
    updatedAt: '2 weeks ago',
    roi: '28.7%',
    duration: '18 months'
  },
  {
    id: 'f4',
    title: 'Renewable Energy Dashboard',
    client: 'Green Energy Corp',
    description: 'Monitoring and analytics platform for renewable energy assets.',
    industry: 'Energy',
    technologies: ['Sustainability', 'Dashboard'],
    status: 'Active',
    image:
      'https://images.unsplash.com/photo-1466611653911-95081537e5b7?q=80&w=600&auto=format&fit=crop',
    updatedAt: '1 month ago',
    roi: '22.4%',
    duration: '8 months'
  }
]
