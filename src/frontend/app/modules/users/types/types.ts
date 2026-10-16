// 3 Role Utama di Sistem Internal (Executive, Commercial, Engineer)
export type SystemRole = 'Executive' | 'Commercial' | 'Engineer'

// Requested Role di tabel Pending Access Requests
export type RequestedRole =
  | SystemRole
  | 'Engineer / Project Lead'
  | 'Commercial / Partnership Officer'
  | 'Executive / Super Admin'

export type UserRole = SystemRole

export type UserStatus = 'Active' | 'Pending' | 'Inactive'

// Tabel 1: Pending Access Requests
export interface PendingUserRequest {
  id: string
  name: string
  email: string
  division: string
  requestedRole: RequestedRole
  requestDate: string
  status: 'Pending'
  requestReason?: string
}

// Tabel 2: Users (Active Users Table di bawahnya)
export interface ActiveUser {
  id: string
  name: string
  email: string
  role: UserRole
  status: 'Active' | 'Inactive'
  assignedDate: string
}

// Top KPI Cards
export interface UserStats {
  pendingRequests: number
  totalUsers: number
  activeUsers: number
  inactiveUsers: number
}
