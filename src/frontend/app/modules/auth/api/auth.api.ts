import { apiClient } from '~/api/client'
import { ENDPOINTS } from '~/api/endpoints'
import type {
  RegisterPayload,
  RegisterResponse,
  ForgotPasswordPayload,
  ForgotPasswordResponse,
  ResetPasswordPayload,
  LoginPayload,
  LoginResponse
} from '../types/auth.types'

export const authApi = {
  async register(payload: RegisterPayload): Promise<RegisterResponse> {
    const response = await apiClient.post<RegisterResponse>(ENDPOINTS.AUTH.REGISTER, payload)
    return response.data
  },

  async resendOtp(email: string): Promise<{ success?: boolean; message: string }> {
    const response = await apiClient.post(ENDPOINTS.AUTH.RESEND_OTP, { email })
    return response.data
  },

  async verifyEmail(
    email: string,
    otp: string
  ): Promise<{ success?: boolean; message: string; data?: any }> {
    const response = await apiClient.post(ENDPOINTS.AUTH.VERIFY_EMAIL, { email, otp })
    return response.data
  },

  async forgotPassword(payload: ForgotPasswordPayload): Promise<ForgotPasswordResponse> {
    const response = await apiClient.post<ForgotPasswordResponse>(
      ENDPOINTS.AUTH.FORGOT_PASSWORD,
      payload
    )
    return response.data
  },

  async resetPassword(
    payload: ResetPasswordPayload
  ): Promise<{ success?: boolean; message: string }> {
    const response = await apiClient.post(ENDPOINTS.AUTH.RESET_PASSWORD, payload)
    return response.data
  },

  async login(payload: LoginPayload): Promise<LoginResponse> {
    const response = await apiClient.post<LoginResponse>(ENDPOINTS.AUTH.LOGIN, payload)
    return response.data
  },

  async getGoogleLoginUrl(): Promise<{
    success?: boolean
    message?: string
    data: { login_url: string }
  }> {
    const response = await apiClient.get(ENDPOINTS.AUTH.GOOGLE_LOGIN)
    return response.data
  },

  async refresh(): Promise<any> {
    const response = await apiClient.post(ENDPOINTS.AUTH.REFRESH)
    return response.data
  },

  async logout(): Promise<{ success?: boolean; message?: string }> {
    const response = await apiClient.post(ENDPOINTS.AUTH.LOGOUT)
    return response.data
  },

  async getMe(): Promise<{
    success?: boolean
    message?: string
    data: {
      id: string
      email: string
      full_name: string
      role_id: string | null
      is_active: boolean
    }
  }> {
    const response = await apiClient.get(ENDPOINTS.AUTH.ME)
    return response.data
  }
}
