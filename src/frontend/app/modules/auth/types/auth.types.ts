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

export interface ResetPasswordPayload {
  token: string
  new_password: string
}

export interface LoginPayload {
  email: string
  password: string
}

export interface LoginResponse {
  success?: boolean
  message?: string
  data?: {
    access_token?: string
    token?: string
    user?: any
    is_verified?: boolean
    [key: string]: any
  }
  access_token?: string
  [key: string]: any
}
