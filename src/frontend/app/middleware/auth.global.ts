import { useAuthStore } from '~/modules/auth/stores/auth.store'

export default defineNuxtRouteMiddleware(async (to) => {
  // 1. Lewati eksekusi jika sedang berada di Server (SSR)!
  // Ini kunci agar server tidak me-redirect kamu ke /login sebelum browser sempat refresh token
  if (import.meta.server) {
    return
  }

  const authStore = useAuthStore()

  // 2. Daftar Halaman Auth / Publik
  const authPages = ['/login', '/signup', '/forgot-password', '/otp', '/reset-password']

  const isAuthPage = authPages.includes(to.path)

  // 3. Abaikan halaman 404
  if (to.matched.length === 0) {
    return
  }

  // 4. SILENT REFRESH DI BROWSER:
  // Cek token terlebih dahulu di client-side jika RAM Pinia masih kosong
  if (!authStore.isAuthenticated) {
    try {
      await authStore.refreshToken()
    } catch {
      // Refresh gagal, artinya sesi habis / belum login
    }
  }

  // 5. JIKA SUDAH LOGIN:
  if (authStore.isAuthenticated) {
    // Kalau sudah login tapi buka halaman auth, lempar ke landing
    if (isAuthPage) {
      return navigateTo('/landing', { replace: true })
    }
    // Kalau buka halaman internal (dashboard/landing), IZINKAN LANGSUNG!
    return
  }

  // 6. JIKA BELUM LOGIN:
  if (!authStore.isAuthenticated) {
    // Kalau belum login dan buka halaman internal, baru tendang ke login
    if (!isAuthPage) {
      return navigateTo('/login', { replace: true })
    }
    // Kalau buka halaman login/signup biasa, izinkan masuk
    return
  }
})
