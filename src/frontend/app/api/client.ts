import axios from 'axios'
import { useAuthStore } from '~/modules/auth/stores/auth.store'

export const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json'
  }
})

// Request Interceptor: Menempelkan Bearer Token langsung dari Memory State Pinia
apiClient.interceptors.request.use(
  (config) => {
    try {
      const authStore = useAuthStore()
      if (authStore.accessToken && config.headers) {
        config.headers.Authorization = `Bearer ${authStore.accessToken}`
      }
    } catch {
      // Pinia mungkin belum siap saat inisialisasi awal
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response Interceptor: Menyeragamkan pesan error dari backend
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.message ||
      error.response?.data?.error ||
      error.message ||
      'Request failed. Please try again.'

    return Promise.reject(new Error(message))
  }
)
