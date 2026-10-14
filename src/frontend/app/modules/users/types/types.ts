export type UserRole = 'Executive' | 'Commercial' | 'Engineer'
export type UserStatus = 'Active' | 'Pending' | 'Inactive'

export interface PendingUserRequest {
  id: string
  name: string
  email: string
  requestDate: string
  status: 'Pending'
}

export interface ActiveUser {
  id: string
  name: string
  email: string
  role: UserRole
  status: 'Active' | 'Inactive'
  assignedDate: string
}

export interface UserStats {
  pendingRequests: number
  totalUsers: number
  activeUsers: number
  inactiveUsers: number
}
