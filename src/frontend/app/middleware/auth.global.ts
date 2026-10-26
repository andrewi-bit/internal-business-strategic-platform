import { useAuthStore } from '~/modules/auth/stores/auth.store'

export default defineNuxtRouteMiddleware(async (to) => {
  // 1. Lewati eksekusi jika sedang berada di Server (SSR)
  if (import.meta.server) {
    return
  }

  const authStore = useAuthStore()

  // 2. Daftar Halaman Auth / Publik
  const authPages = ['/login', '/signup', '/forgot-password', '/otp', '/reset-password']
  const isAuthPage = authPages.includes(to.path)

  // Abaikan halaman 404
  if (to.matched.length === 0) {
    return
  }

  // 3. SILENT REFRESH DI BROWSER:
  // Cek token terlebih dahulu di client-side jika RAM Pinia masih kosong (misal setelah refresh F5)
  if (!authStore.isAuthenticated) {
    try {
      await authStore.refreshToken()
    } catch {
      // Refresh gagal, artinya sesi habis / belum login
    }
  }

  // 4. JIKA SUDAH LOGIN:
  if (authStore.isAuthenticated) {
    // Pastikan data profil user (termasuk role_id) sudah ter-load di Pinia
    if (!authStore.user || authStore.user.role_id === undefined) {
      await authStore.fetchCurrentUser()
    }

    const hasRole = authStore.hasRole // true jika punya role, false jika null

    // Skenario A: User mencoba buka halaman Auth (/login, /signup, dll)
    if (isAuthPage) {
      return navigateTo(hasRole ? '/dashboard' : '/landing', { replace: true })
    }

    // Skenario B: User SUDAH PUNYA ROLE mencoba buka /landing
    if (hasRole && to.path === '/landing') {
      return navigateTo('/dashboard', { replace: true, external: true })
    }

    // Skenario C: User BELUM PUNYA ROLE mencoba buka halaman internal selain /landing (misal /dashboard)
    if (!hasRole && to.path !== '/landing') {
      return navigateTo('/landing', { replace: true, external: true })
    }

    // Izinkan akses rute yang sesuai
    return
  }

  // 5. JIKA BELUM LOGIN:
  if (!authStore.isAuthenticated) {
    // Kalau belum login dan buka halaman internal apa pun (termasuk /landing), tendang ke login
    if (!isAuthPage) {
      return navigateTo('/login', { replace: true, external: true })
    }
    // Kalau buka halaman login biasa, izinkan
    return
  }
})
