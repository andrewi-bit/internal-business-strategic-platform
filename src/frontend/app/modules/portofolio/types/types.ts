export type ProjectStatus = 'Completed' | 'Active' | 'On Going' | 'Planned' | 'Cancelled'

export interface ProjectItem {
  id: string
  title: string
  client: string
  description: string
  industry: string
  technologies: string[]
  status: ProjectStatus
  image: string
  updatedAt: string
}

export type ViewMode = 'grid' | 'table'

export interface PortfolioFilterState {
  search: string
  industry: string
  technology: string
  year: string
  status: string
}

// --- Tambahan Khusus untuk Halaman Detail ---

export interface ProjectDocument {
  name: string
  size: string
  date: string
}

export interface RelatedPartner {
  name: string
  role: string
  tag: string
  icon?: string
}

export interface ProjectDetailItem extends ProjectItem {
  period: string
  projectValue: string
  location: string
  teamSize: string
  serviceType: string
  projectType: string
  heroImages: string[]
  overview: string
  background: string
  challenges: string[]
  solutions: string[]
  metrics: {
    label: string
    value: string
    sublabel: string
  }[]
  mediaGallery: {
    type: 'image' | 'video'
    url: string
    title: string
  }[]
  documents: ProjectDocument[]
  partners: RelatedPartner[]
}
