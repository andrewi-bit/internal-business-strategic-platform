import { apiClient } from '~/api/client'
import { ENDPOINTS } from '~/api/endpoints'
import type { RegisterPayload, RegisterResponse } from '../types/auth.types'

export const authApi = {
  /**
   * Panggil POST /api/v1/auth/register
   */
  async register(payload: RegisterPayload): Promise<RegisterResponse> {
    const response = await apiClient.post<RegisterResponse>(ENDPOINTS.AUTH.REGISTER, payload)
    return response.data
  },

  /**
   * POST /api/v1/auth/resend-otp
   */
  async resendOtp(email: string): Promise<{ success?: boolean; message: string }> {
    const response = await apiClient.post(ENDPOINTS.AUTH.RESEND_OTP, { email })
    return response.data
  },
  /**
   * POST /api/v1/auth/verify-email
   */
  async verifyEmail(
    email: string,
    otp: string
  ): Promise<{ success?: boolean; message: string; data?: any }> {
    const response = await apiClient.post(ENDPOINTS.AUTH.VERIFY_EMAIL, { email, otp })
    return response.data
  }
}
