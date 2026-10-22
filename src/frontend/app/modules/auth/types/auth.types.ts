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

export interface ForgotPasswordPayload {
  email: string
}

export interface ForgotPasswordResponse {
  success?: boolean
  message: string
  [key: string]: any
}
