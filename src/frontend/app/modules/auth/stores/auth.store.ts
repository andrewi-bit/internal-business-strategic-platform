import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { authApi } from '../api/auth.api'
import type { RegisterPayload, LoginPayload } from '../types/auth.types'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref<string | null>(null)
  const user = ref<any | null>(null)
  const pendingEmail = ref<string>('')
  const hasJustSentOtp = ref<boolean>(false)
  const isLoading = ref<boolean>(false)

  const isAuthenticated = computed(() => !!accessToken.value)

  const setAccessToken = (token: string | null) => {
    accessToken.value = token
  }

  const setPendingEmail = (email: string) => {
    pendingEmail.value = email
  }

  /**
   * Action Register:
   * 1. Register akun
   * 2. Langsung request OTP pertama via resendOtp
   */
  const register = async (payload: RegisterPayload) => {
    isLoading.value = true
    try {
      // 1. Hit API Register
      const registerRes = await authApi.register(payload)

      // Simpan email ke state Pinia
      pendingEmail.value = payload.email

      // 2. Langsung hit API Resend OTP untuk mengirimkan kode OTP ke email
      try {
        await authApi.resendOtp(payload.email)
        hasJustSentOtp.value = true
      } catch (err) {
        console.warn('Auto resend OTP failed, user can retry manually on OTP page:', err)
      }

      return registerRes
    } finally {
      isLoading.value = false
    }
  }

  const login = async (payload: LoginPayload) => {
    isLoading.value = true
    try {
      const response = await authApi.login(payload)
      // Ekstrak token dari respon (mendukung response.data.access_token atau response.access_token)
      const token =
        response.data?.access_token ||
        response.access_token ||
        (typeof response === 'string' ? response : null)
      if (token) {
        accessToken.value = token
      }
      if (response.data?.user || response.user) {
        user.value = response.data?.user || response.user
      }
      return response
    } finally {
      isLoading.value = false
    }
  }

  const refreshToken = async () => {
    try {
      const response = await authApi.refresh()
      const token =
        response.data?.access_token ||
        response.access_token ||
        (typeof response === 'string' ? response : null)
      if (token) {
        accessToken.value = token
        return token
      }
      return null
    } catch (err) {
      clearAuth()
      throw err
    }
  }
  /**
   * Action Resend OTP manual dari tombol
   */
  const resendOtp = async (email: string) => {
    return await authApi.resendOtp(email)
  }

  /**
   * Action Verify Email OTP
   */
  const verifyEmail = async (email: string, otp: string) => {
    isLoading.value = true
    try {
      const response = await authApi.verifyEmail(email, otp)
      return response
    } finally {
      isLoading.value = false
    }
  }

  const forgotPassword = async (email: string) => {
    isLoading.value = true
    try {
      const response = await authApi.forgotPassword({ email })
      return response
    } finally {
      isLoading.value = false
    }
  }

  const resetPassword = async (token: string, newPassword: string) => {
    isLoading.value = true
    try {
      const response = await authApi.resetPassword({
        token,
        new_password: newPassword
      })
      return response
    } finally {
      isLoading.value = false
    }
  }

  const clearAuth = () => {
    accessToken.value = null
    user.value = null
    pendingEmail.value = ''
  }

  return {
    accessToken,
    user,
    pendingEmail,
    isLoading,
    isAuthenticated,
    hasJustSentOtp,
    setAccessToken,
    setPendingEmail,
    register,
    login,
    refreshToken,
    resendOtp,
    verifyEmail,
    forgotPassword,
    resetPassword,
    clearAuth
  }
})
