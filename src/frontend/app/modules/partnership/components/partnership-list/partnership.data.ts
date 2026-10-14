import type {
  FilterOption,
  Partner,
  PartnershipAdvancedFilters,
  PartnershipFilterState,
  PartnershipStat
} from './partnership.types'

export const createPartnershipFilters = (): PartnershipFilterState => ({
  search: '',
  categories: [],
  statuses: [],
  contractStatuses: [],
  industries: [],
  expertises: [],
  locations: []
})

export const createAdvancedFilters = (): PartnershipAdvancedFilters => ({
  contractEndPreset: 'any',
  contractEndStart: '',
  contractEndEnd: '',
  lastUpdatedPreset: 'any',
  lastUpdatedStart: '',
  lastUpdatedEnd: '',
  partnerTypes: [],
  activeProjectWith: false,
  activeProjectWithout: false
})

export const partnershipCategories: FilterOption[] = [
  { label: 'Technology Partner', value: 'Technology Partner' },
  { label: 'Channel Partner', value: 'Channel Partner' },
  { label: 'Service Partner', value: 'Service Partner' },
  { label: 'Marketing Partner', value: 'Marketing Partner' }
]

export const partnershipStatuses: FilterOption[] = [
  { label: 'Draft', value: 'Draft' },
  { label: 'Under Review', value: 'Under Review' },
  { label: 'Active', value: 'Active' },
  { label: 'Expired', value: 'Expired' },
  { label: 'Terminated', value: 'Terminated' }
]

export const contractStatuses: FilterOption[] = [
  { label: 'Active', value: 'Active' },
  { label: 'Pending', value: 'Pending' },
  { label: 'Expired', value: 'Expired' },
  { label: 'Terminated', value: 'Terminated' }
]

export const industries: FilterOption[] = [
  { label: 'Technology', value: 'Technology' },
  { label: 'Telecommunications', value: 'Telecommunications' },
  { label: 'Energy & Utilities', value: 'Energy & Utilities' },
  { label: 'Financial Services', value: 'Financial Services' },
  { label: 'Manufacturing', value: 'Manufacturing' },
  { label: 'Healthcare', value: 'Healthcare' },
  { label: 'Transportation & Logistics', value: 'Transportation & Logistics' },
  { label: 'Retail & Consumer Goods', value: 'Retail & Consumer Goods' },
  { label: 'Government & Public Sector', value: 'Government & Public Sector' },
  { label: 'Other', value: 'Other' }
]

export const expertises: FilterOption[] = [
  { label: 'Cloud Platform', value: 'Cloud Platform' },
  { label: 'Data Analytics', value: 'Data Analytics' },
  { label: 'AI & Machine Learning', value: 'AI & Machine Learning' },
  { label: 'Network Solution', value: 'Network Solution' },
  { label: 'IoT Solution', value: 'IoT Solution' },
  { label: 'Cybersecurity', value: 'Cybersecurity' },
  { label: 'Digital Transformation', value: 'Digital Transformation' },
  { label: 'Business Consulting', value: 'Business Consulting' },
  { label: 'Industrial Automation', value: 'Industrial Automation' },
  { label: 'Other', value: 'Other' }
]

export const locations: FilterOption[] = [
  { label: 'Indonesia', value: 'Indonesia' },
  { label: 'Singapore', value: 'Singapore' },
  { label: 'Malaysia', value: 'Malaysia' },
  { label: 'Thailand', value: 'Thailand' },
  { label: 'Vietnam', value: 'Vietnam' },
  { label: 'Philippines', value: 'Philippines' },
  { label: 'United States', value: 'United States' },
  { label: 'Japan', value: 'Japan' },
  { label: 'Australia', value: 'Australia' },
  { label: 'Europe', value: 'Europe' },
  { label: 'Other', value: 'Other' }
]

export const partnerTypes: FilterOption[] = [
  { label: 'Strategic Partner', value: 'Strategic Partner' },
  { label: 'Implementation Partner', value: 'Implementation Partner' },
  { label: 'Consulting Partner', value: 'Consulting Partner' },
  { label: 'Reseller', value: 'Reseller' },
  { label: 'Technology Provider', value: 'Technology Provider' },
  { label: 'Other', value: 'Other' }
]

export const partnershipStats: PartnershipStat[] = [
  {
    key: 'total',
    label: 'Total Partners',
    value: 28,
    icon: 'i-lucide-handshake',
    tone: 'blue'
  },
  {
    key: 'active',
    label: 'Active Partners',
    value: 16,
    icon: 'i-lucide-circle-check-big',
    tone: 'emerald'
  },
  {
    key: 'review',
    label: 'Under Review',
    value: 4,
    icon: 'i-lucide-clock',
    tone: 'amber'
  },
  {
    key: 'expiring',
    label: 'Expiring Soon',
    value: 3,
    icon: 'i-lucide-calendar-clock',
    tone: 'orange',
    hint: 'In less than 30 days'
  },
  {
    key: 'terminated',
    label: 'Terminated',
    value: 2,
    icon: 'i-lucide-circle-x',
    tone: 'rose'
  }
]

export const partners: Partner[] = [
  {
    id: 'PIN-2026-001',
    name: 'Accenture',
    category: 'Technology Partner',
    industry: 'Technology',
    expertise: 'Business Consulting',
    location: 'United States',
    status: 'Active',
    contractStatus: 'Active',
    contractEndDate: '2027-05-31',
    lastUpdated: '2026-10-01T08:44:00',
    partnerType: 'Strategic Partner',
    hasActiveProject: true
  },
  {
    id: 'PIN-2026-002',
    name: 'Toshiba Infrastructure Systems',
    category: 'Service Partner',
    industry: 'Manufacturing',
    expertise: 'Industrial Automation',
    location: 'Japan',
    status: 'Expired',
    contractStatus: 'Expired',
    contractEndDate: '2025-04-30',
    lastUpdated: '2026-09-27T09:18:00',
    partnerType: 'Technology Provider',
    hasActiveProject: false
  },
  {
    id: 'PIN-2026-003',
    name: 'Schneider Electric',
    category: 'Service Partner',
    industry: 'Energy & Utilities',
    expertise: 'Industrial Automation',
    location: 'Europe',
    status: 'Active',
    contractStatus: 'Active',
    contractEndDate: '2026-10-05',
    lastUpdated: '2026-10-02T13:58:00',
    partnerType: 'Strategic Partner',
    hasActiveProject: true
  },
  {
    id: 'PIN-2026-004',
    name: 'Enterprise Software Group',
    category: 'Technology Partner',
    industry: 'Technology',
    expertise: 'Cloud Platform',
    location: 'Singapore',
    status: 'Active',
    contractStatus: 'Active',
    contractEndDate: '2027-08-15',
    lastUpdated: '2026-09-28T15:22:00',
    partnerType: 'Reseller',
    hasActiveProject: true
  },
  {
    id: 'PIN-2026-005',
    name: 'Global Cloud Solutions',
    category: 'Channel Partner',
    industry: 'Technology',
    expertise: 'Cloud Platform',
    location: 'Indonesia',
    status: 'Active',
    contractStatus: 'Active',
    contractEndDate: '2026-11-01',
    lastUpdated: '2026-09-29T17:10:00',
    partnerType: 'Reseller',
    hasActiveProject: true
  },
  {
    id: 'PIN-2026-006',
    name: 'PT Nusantara Teknologi',
    category: 'Technology Partner',
    industry: 'Technology',
    expertise: 'Digital Transformation',
    location: 'Indonesia',
    status: 'Under Review',
    contractStatus: 'Pending',
    contractEndDate: '2027-01-15',
    lastUpdated: '2026-09-20T10:05:00',
    partnerType: 'Implementation Partner',
    hasActiveProject: false
  },
  {
    id: 'PIN-2026-007',
    name: 'DataSphere Analytics',
    category: 'Technology Partner',
    industry: 'Financial Services',
    expertise: 'Data Analytics',
    location: 'Singapore',
    status: 'Active',
    contractStatus: 'Active',
    contractEndDate: '2027-03-22',
    lastUpdated: '2026-09-15T14:30:00',
    partnerType: 'Strategic Partner',
    hasActiveProject: true
  },
  {
    id: 'PIN-2026-008',
    name: 'AI Vision Labs',
    category: 'Technology Partner',
    industry: 'Technology',
    expertise: 'AI & Machine Learning',
    location: 'United States',
    status: 'Active',
    contractStatus: 'Active',
    contractEndDate: '2027-06-30',
    lastUpdated: '2026-09-10T11:20:00',
    partnerType: 'Technology Provider',
    hasActiveProject: true
  },
  {
    id: 'PIN-2026-009',
    name: 'CloudNine Infrastructure',
    category: 'Channel Partner',
    industry: 'Telecommunications',
    expertise: 'Network Solution',
    location: 'Malaysia',
    status: 'Active',
    contractStatus: 'Active',
    contractEndDate: '2026-12-20',
    lastUpdated: '2026-08-05T09:00:00',
    partnerType: 'Reseller',
    hasActiveProject: true
  },
  {
    id: 'PIN-2026-010',
    name: 'SecureNet Cyber',
    category: 'Technology Partner',
    industry: 'Financial Services',
    expertise: 'Cybersecurity',
    location: 'United States',
    status: 'Active',
    contractStatus: 'Active',
    contractEndDate: '2027-02-28',
    lastUpdated: '2026-09-25T16:45:00',
    partnerType: 'Strategic Partner',
    hasActiveProject: true
  },
  {
    id: 'PIN-2026-011',
    name: 'IoT Dynamics',
    category: 'Technology Partner',
    industry: 'Manufacturing',
    expertise: 'IoT Solution',
    location: 'Japan',
    status: 'Under Review',
    contractStatus: 'Pending',
    contractEndDate: '2027-04-10',
    lastUpdated: '2026-09-18T13:15:00',
    partnerType: 'Implementation Partner',
    hasActiveProject: false
  },
  {
    id: 'PIN-2026-012',
    name: 'Digital Consulting Partners',
    category: 'Service Partner',
    industry: 'Other',
    expertise: 'Business Consulting',
    location: 'Australia',
    status: 'Active',
    contractStatus: 'Active',
    contractEndDate: '2027-07-31',
    lastUpdated: '2026-09-05T10:00:00',
    partnerType: 'Consulting Partner',
    hasActiveProject: true
  },
  {
    id: 'PIN-2026-013',
    name: 'GreenGrid Energy Systems',
    category: 'Service Partner',
    industry: 'Energy & Utilities',
    expertise: 'Digital Transformation',
    location: 'Europe',
    status: 'Active',
    contractStatus: 'Active',
    contractEndDate: '2026-10-20',
    lastUpdated: '2026-09-12T15:40:00',
    partnerType: 'Strategic Partner',
    hasActiveProject: true
  },
  {
    id: 'PIN-2026-014',
    name: 'FinEdge Financial Tech',
    category: 'Technology Partner',
    industry: 'Financial Services',
    expertise: 'Data Analytics',
    location: 'Singapore',
    status: 'Active',
    contractStatus: 'Active',
    contractEndDate: '2027-05-18',
    lastUpdated: '2026-09-22T08:50:00',
    partnerType: 'Technology Provider',
    hasActiveProject: true
  },
  {
    id: 'PIN-2026-015',
    name: 'MedTech Solutions',
    category: 'Service Partner',
    industry: 'Healthcare',
    expertise: 'AI & Machine Learning',
    location: 'United States',
    status: 'Active',
    contractStatus: 'Active',
    contractEndDate: '2027-09-30',
    lastUpdated: '2026-08-28T12:10:00',
    partnerType: 'Implementation Partner',
    hasActiveProject: true
  },
  {
    id: 'PIN-2026-016',
    name: 'LogiChain Systems',
    category: 'Channel Partner',
    industry: 'Transportation & Logistics',
    expertise: 'Network Solution',
    location: 'Indonesia',
    status: 'Under Review',
    contractStatus: 'Pending',
    contractEndDate: '2026-11-15',
    lastUpdated: '2026-09-08T17:25:00',
    partnerType: 'Reseller',
    hasActiveProject: false
  },
  {
    id: 'PIN-2026-017',
    name: 'RetailFlow Digital',
    category: 'Marketing Partner',
    industry: 'Retail & Consumer Goods',
    expertise: 'Digital Transformation',
    location: 'Thailand',
    status: 'Active',
    contractStatus: 'Active',
    contractEndDate: '2026-10-28',
    lastUpdated: '2026-09-30T09:05:00',
    partnerType: 'Reseller',
    hasActiveProject: true
  },
  {
    id: 'PIN-2026-018',
    name: 'GovTech Integrators',
    category: 'Service Partner',
    industry: 'Government & Public Sector',
    expertise: 'Digital Transformation',
    location: 'Indonesia',
    status: 'Under Review',
    contractStatus: 'Pending',
    contractEndDate: '2027-03-05',
    lastUpdated: '2026-09-02T11:55:00',
    partnerType: 'Strategic Partner',
    hasActiveProject: false
  },
  {
    id: 'PIN-2026-019',
    name: 'TelcoBridge Communications',
    category: 'Channel Partner',
    industry: 'Telecommunications',
    expertise: 'Network Solution',
    location: 'Malaysia',
    status: 'Active',
    contractStatus: 'Active',
    contractEndDate: '2027-04-25',
    lastUpdated: '2026-09-26T14:20:00',
    partnerType: 'Strategic Partner',
    hasActiveProject: true
  },
  {
    id: 'PIN-2026-020',
    name: 'RenewCo Energy',
    category: 'Service Partner',
    industry: 'Energy & Utilities',
    expertise: 'Industrial Automation',
    location: 'Australia',
    status: 'Expired',
    contractStatus: 'Expired',
    contractEndDate: '2026-02-28',
    lastUpdated: '2026-07-15T10:40:00',
    partnerType: 'Technology Provider',
    hasActiveProject: false
  },
  {
    id: 'PIN-2026-021',
    name: 'AdWorx Marketing',
    category: 'Marketing Partner',
    industry: 'Retail & Consumer Goods',
    expertise: 'Business Consulting',
    location: 'Vietnam',
    status: 'Expired',
    contractStatus: 'Expired',
    contractEndDate: '2026-01-31',
    lastUpdated: '2026-09-19T16:00:00',
    partnerType: 'Reseller',
    hasActiveProject: false
  },
  {
    id: 'PIN-2026-022',
    name: 'LegacyCore Systems',
    category: 'Service Partner',
    industry: 'Manufacturing',
    expertise: 'Industrial Automation',
    location: 'Europe',
    status: 'Terminated',
    contractStatus: 'Terminated',
    contractEndDate: '2026-03-31',
    lastUpdated: '2026-06-20T09:30:00',
    partnerType: 'Consulting Partner',
    hasActiveProject: false
  },
  {
    id: 'PIN-2026-023',
    name: 'NorthStar Consulting',
    category: 'Service Partner',
    industry: 'Other',
    expertise: 'Business Consulting',
    location: 'United States',
    status: 'Active',
    contractStatus: 'Active',
    contractEndDate: '2027-08-12',
    lastUpdated: '2026-09-14T13:45:00',
    partnerType: 'Consulting Partner',
    hasActiveProject: true
  },
  {
    id: 'PIN-2026-024',
    name: 'Pacific Cloud Services',
    category: 'Channel Partner',
    industry: 'Technology',
    expertise: 'Cloud Platform',
    location: 'Philippines',
    status: 'Active',
    contractStatus: 'Active',
    contractEndDate: '2027-02-14',
    lastUpdated: '2026-09-21T08:15:00',
    partnerType: 'Reseller',
    hasActiveProject: true
  },
  {
    id: 'PIN-2026-025',
    name: 'SmartFactory Automation',
    category: 'Technology Partner',
    industry: 'Manufacturing',
    expertise: 'Industrial Automation',
    location: 'Japan',
    status: 'Draft',
    contractStatus: 'Pending',
    contractEndDate: '2027-10-01',
    lastUpdated: '2026-09-29T10:50:00',
    partnerType: 'Technology Provider',
    hasActiveProject: false
  },
  {
    id: 'PIN-2026-026',
    name: 'Insight Retail Analytics',
    category: 'Technology Partner',
    industry: 'Retail & Consumer Goods',
    expertise: 'Data Analytics',
    location: 'Indonesia',
    status: 'Draft',
    contractStatus: 'Pending',
    contractEndDate: '2027-06-18',
    lastUpdated: '2026-09-27T14:35:00',
    partnerType: 'Implementation Partner',
    hasActiveProject: false
  },
  {
    id: 'PIN-2026-027',
    name: 'CyberShield Defense',
    category: 'Technology Partner',
    industry: 'Government & Public Sector',
    expertise: 'Cybersecurity',
    location: 'United States',
    status: 'Terminated',
    contractStatus: 'Terminated',
    contractEndDate: '2026-04-15',
    lastUpdated: '2026-05-30T11:05:00',
    partnerType: 'Strategic Partner',
    hasActiveProject: false
  },
  {
    id: 'PIN-2026-028',
    name: 'Vertex AI Solutions',
    category: 'Technology Partner',
    industry: 'Healthcare',
    expertise: 'AI & Machine Learning',
    location: 'Singapore',
    status: 'Draft',
    contractStatus: 'Pending',
    contractEndDate: '2027-11-20',
    lastUpdated: '2026-09-30T15:10:00',
    partnerType: 'Technology Provider',
    hasActiveProject: false
  }
]
