import type { ProjectItem } from '../../portofolio/types/types'

export type UserRole = 'executive' | 'commercial' | 'engineering'

export interface DashboardMetricCard {
  title: string
  value: string | number
  change?: string
  trend?: 'up' | 'down' | 'neutral'
  icon?: string
}

export interface DashboardKpi {
  label: string
  value: string
  delta: string
  deltaLabel: string
  trend: 'up' | 'down' | 'neutral'
  icon: string
  progress?: number
}

export type DashboardDateRange = '3m' | '6m' | '12m'

export interface TrendPoint {
  month: string
  revenue: number
  roi: number
  projects: number
}

export interface StatusSlice {
  label: string
  value: number
  color: string
}

export interface CategoryMetric {
  label: string
  projects: number
  share: number
  roi: number
}

export interface PipelineStage {
  label: string
  opportunities: number
  value: string
  open: boolean
  color: string
}

export interface FeaturedProject extends ProjectItem {
  roi: string
  duration: string
}
