export interface RegisterPayload {
  full_name: string
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
