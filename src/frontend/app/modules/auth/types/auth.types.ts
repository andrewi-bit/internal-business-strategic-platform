export interface RegisterPayload {
  fullName: string
  email: string
  password: string
}

export interface RegisterResponse {
  success?: boolean
  message: string
  data?: {
    userId?: string
    email?: string
    [key: string]: any
  }
}
