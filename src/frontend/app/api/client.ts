import axios from 'axios'
import { useAuthStore } from '~/modules/auth/stores/auth.store'
import { ENDPOINTS } from './endpoints'

const getBaseUrl = () => {
  try {
    const config = useRuntimeConfig()
    return config.public.apiBaseUrl || 'http://localhost:8000'
  } catch {
    return import.meta.env.NUXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
  }
}

export const apiClient = axios.create({
  baseURL: getBaseUrl(),
  timeout: 10000,
  withCredentials: true, // WAJIB: Mengizinkan pengiriman Cookie refresh token ke backend
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json'
  }
})

// Request Interceptor: Pasang Bearer Token dari Memory Pinia
apiClient.interceptors.request.use(
  (config) => {
    try {
      const authStore = useAuthStore()
      if (authStore.accessToken && config.headers) {
        config.headers.Authorization = `Bearer ${authStore.accessToken}`
      }
    } catch {
      // Pinia belum siap
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response Interceptor: Menangani Error Pesan & Auto Refresh jika 401
let isRefreshing = false
let failedQueue: Array<{ resolve: (token: string) => void; reject: (err: any) => void }> = []

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach((promise) => {
    if (error) {
      promise.reject(error)
    } else {
      promise.resolve(token!)
    }
  })
  failedQueue = []
}

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    const data = error.response?.data
    const status = error.response?.status

    // 1. Tangani Kasus 401 Unauthorized (Token Kedaluwarsa)
    if (
      status === 401 &&
      !originalRequest._retry &&
      !originalRequest.url?.includes(ENDPOINTS.AUTH.LOGIN) &&
      !originalRequest.url?.includes(ENDPOINTS.AUTH.REFRESH)
    ) {
      if (isRefreshing) {
        // Jika sedang proses refresh, masukkan request ke antrean tunggu
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        })
          .then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`
            return apiClient(originalRequest)
          })
          .catch((err) => Promise.reject(err))
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        const authStore = useAuthStore()
        const newToken = await authStore.refreshToken()

        if (newToken) {
          processQueue(null, newToken)
          originalRequest.headers.Authorization = `Bearer ${newToken}`
          return apiClient(originalRequest)
        }
      } catch (refreshErr) {
        processQueue(refreshErr, null)
        const authStore = useAuthStore()
        authStore.clearAuth()
        // JANGAN panggil navigateTo('/login') di sini agar tidak memicu reload loop!
        return Promise.reject(refreshErr)
      } finally {
        isRefreshing = false
      }
    }

    // 2. Format Pesan Error Biasa dari Backend
    const message =
      data?.message ||
      (typeof data?.detail === 'string' ? data.detail : null) ||
      error.message ||
      'Request failed. Please try again.'

    const customError = new Error(message) as any
    customError.code = data?.error?.code || null
    customError.data = data || null

    return Promise.reject(customError)
  }
)
