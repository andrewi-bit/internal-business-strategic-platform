import axios from 'axios'
import { useAuthStore } from '~/modules/auth/stores/auth.store'

// Baca base URL dari Nuxt runtimeConfig jika tersedia, atau fallback ke env / localhost:8000
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
    const data = error.response?.data

    // Ambil langsung isi detail dari backend (jika objek/array di-stringify, jika string langsung dipakai)
    const message =
      typeof data?.detail === 'object'
        ? JSON.stringify(data.detail)
        : data?.detail || error.message || 'Request failed'

    return Promise.reject(new Error(message))
  }
)
