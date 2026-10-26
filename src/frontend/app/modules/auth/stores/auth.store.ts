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
  const hasRole = computed(() => !!user.value?.role_id)

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
      const data = response.data || response

      // 1. Ekstrak Access Token
      const token =
        data?.access_token ||
        response.access_token ||
        (typeof response === 'string' ? response : null)

      if (token) {
        accessToken.value = token
      }

      // 2. Simpan Data User & Role secara aman
      const existingUserData = data?.user || response.user || {}

      user.value = {
        ...existingUserData,
        role_id: data?.role_id ?? existingUserData.role_id ?? null,
        role_name: data?.role_name ?? existingUserData.role_name ?? null,
        role_code: data?.role_code ?? existingUserData.role_code ?? null
      }

      return response
    } finally {
      isLoading.value = false
    }
  }

  const openCenteredPopup = (url: string, title = 'Google Sign In', w = 500, h = 600) => {
    const left = window.screenX + (window.outerWidth - w) / 2
    const top = window.screenY + (window.outerHeight - h) / 2
    return window.open(
      url,
      title,
      `width=${w},height=${h},top=${top},left=${left},status=no,menubar=no,toolbar=no`
    )
  }

  /**
   * Action Login Google via OAuth Popup
   */
  const loginWithGoogle = async () => {
    isLoading.value = true
    try {
      // 1. Dapatkan login URL dari backend
      const res = await authApi.getGoogleLoginUrl()
      const loginUrl = res.data?.login_url

      if (!loginUrl) {
        throw new Error('Google login URL not found.')
      }

      // 2. Buka popup OAuth Google
      const popup = openCenteredPopup(loginUrl)

      if (!popup) {
        throw new Error('Popup blocked. Please allow popups for this site.')
      }

      // 3. Pantau sesi secara berkala (Polling Silent Refresh)
      // Begitu callback backend selesai, cookie terpasang dan refreshToken() akan sukses
      await new Promise<void>((resolve, reject) => {
        let attempts = 0
        const maxAttempts = 120 // batas waktu 60 detik (120 x 500ms)

        const timer = setInterval(async () => {
          attempts++

          // Jika popup ditutup manual oleh user sebelum login selesai
          if (popup.closed) {
            clearInterval(timer)
            // Cek sekali lagi barangkali tepat sebelum ditutup sudah sukses
            try {
              const token = await refreshToken()
              if (token) {
                return resolve()
              }
            } catch {
              // Abaikan jika memang belum selesai
            }
            return resolve()
          }

          // Coba panggil refreshToken di background
          try {
            const token = await refreshToken()
            if (token) {
              clearInterval(timer)
              try {
                popup.close() // Otomatis tutup popup!
              } catch {
                // Abaikan jika browser membatasi close
              }
              return resolve()
            }
          } catch {
            // Belum selesai proses di Google / backend, lanjutkan tunggu
          }

          if (attempts >= maxAttempts) {
            clearInterval(timer)
            try {
              popup.close()
            } catch {}
            reject(new Error('Google sign in timed out. Please try again.'))
          }
        }, 600)
      })

      // 4. Jika token sudah didapat, redirect ke landing
      if (isAuthenticated.value) {
        const currentUser = await fetchCurrentUser()
        if (currentUser?.role_id) {
          await navigateTo('/dashboard')
        } else {
          await navigateTo('/landing')
        }
      }
    } catch (err: any) {
      console.error('Google login error:', err)
      throw err
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

  const logout = async () => {
    isLoading.value = true
    try {
      await authApi.logout()
    } catch (err) {
      console.warn('Backend logout failed or session already expired:', err)
    } finally {
      clearAuth()
      isLoading.value = false
      await navigateTo('/login', { replace: true, external: true })
    }
  }

  const fetchCurrentUser = async () => {
    try {
      const res = await authApi.getMe()
      if (res.data) {
        user.value = res.data
      }
      return res.data
    } catch (err) {
      console.error('Failed to fetch current user profile:', err)
      return null
    }
  }

  return {
    accessToken,
    user,
    pendingEmail,
    isLoading,
    isAuthenticated,
    hasRole,
    hasJustSentOtp,
    setAccessToken,
    setPendingEmail,
    register,
    login,
    loginWithGoogle,
    refreshToken,
    resendOtp,
    verifyEmail,
    forgotPassword,
    resetPassword,
    clearAuth,
    logout,
    fetchCurrentUser
  }
})
