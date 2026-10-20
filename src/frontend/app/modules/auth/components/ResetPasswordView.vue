<template>
  <!-- Background Image Fullscreen dari assets/blue-bg.png -->
  <div
    class="relative isolate flex min-h-screen w-full items-center justify-center bg-cover bg-center bg-no-repeat p-4 font-sans select-none"
    :style="{ backgroundImage: `url(${blueBg})` }"
  >
    <!-- Card Utama (Proporsi & Shadow sama persis dengan OTP & Forgot Password) -->
    <div
      class="relative z-10 w-full rounded-[24px] bg-white px-8 py-9 shadow-[0_20px_60px_-15px_rgba(2,18,66,0.35)] sm:px-10 sm:py-10"
      style="max-width: 440px"
    >
      <!-- ========================================== -->
      <!-- STATE 1: FORM RESET PASSWORD               -->
      <!-- ========================================== -->
      <div v-if="!isSuccess">
        <!-- Icon Perisai Gembok Biru Pucat di Atas -->
        <div class="flex justify-center">
          <div
            class="flex h-12 w-12 items-center justify-center rounded-full bg-[#e8f1fd] text-[#1a73e8]"
          >
            <UIcon name="i-lucide-shield-check" class="h-6 w-6 stroke-[1.8]" />
          </div>
        </div>

        <!-- Header Teks -->
        <div class="mt-4 text-center">
          <h1 class="text-[22px] font-bold tracking-tight text-[#111827]">Reset Password</h1>
          <p class="mt-1.5 text-[13px] text-[#6b7280] leading-relaxed">
            Please enter your new password below to regain access to your account.
          </p>
        </div>

        <!-- Warning jika Token di URL tidak ditemukan -->
        <div
          v-if="!token"
          class="mt-4 flex items-center gap-2 rounded-xl border border-amber-200 bg-amber-50 p-3 text-[12px] text-amber-800"
        >
          <UIcon name="i-lucide-alert-circle" class="h-4 w-4 shrink-0 text-amber-600" />
          <span>Invalid or missing reset token. Please request a new link.</span>
        </div>

        <!-- Form Input -->
        <form class="mt-6 space-y-4" @submit.prevent="handleSubmit">
          <!-- 1. Field: New Password -->
          <div class="space-y-1.5 text-left">
            <label for="newPassword" class="block text-[12px] font-semibold text-[#374151]">
              New Password
            </label>
            <div class="relative">
              <UInput
                id="newPassword"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                icon="i-lucide-lock"
                placeholder="At least 8 characters"
                size="lg"
                block
                class="w-full"
                :disabled="isLoading || !token"
                :ui="{
                  base: 'h-11 rounded-xl text-[13px]',
                  leading: 'ps-3.5 text-[#9ca3af]',
                  trailing: 'pe-3.5'
                }"
                :class="passwordError ? '!border-rose-500 focus:!ring-rose-500/20' : ''"
              >
                <!-- Toggle Show/Hide Password -->
                <template #trailing>
                  <button
                    type="button"
                    class="flex items-center text-[#9ca3af] hover:text-[#4b5563] cursor-pointer"
                    @click="showPassword = !showPassword"
                  >
                    <UIcon
                      :name="showPassword ? 'i-lucide-eye-off' : 'i-lucide-eye'"
                      class="h-4 w-4"
                    />
                  </button>
                </template>
              </UInput>
            </div>
            <!-- Error New Password -->
            <p v-if="passwordError" class="text-[11px] font-medium text-rose-500 transition-all">
              {{ passwordError }}
            </p>
          </div>

          <!-- 2. Field: Confirm Password -->
          <div class="space-y-1.5 text-left">
            <label for="confirmPassword" class="block text-[12px] font-semibold text-[#374151]">
              Confirm Password
            </label>
            <div class="relative">
              <UInput
                id="confirmPassword"
                v-model="confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                icon="i-lucide-lock"
                placeholder="Re-enter your new password"
                size="lg"
                block
                class="w-full"
                :disabled="isLoading || !token"
                :ui="{
                  base: 'h-11 rounded-xl text-[13px]',
                  leading: 'ps-3.5 text-[#9ca3af]',
                  trailing: 'pe-3.5'
                }"
                :class="confirmError ? '!border-rose-500 focus:!ring-rose-500/20' : ''"
              >
                <!-- Toggle Show/Hide Confirm Password -->
                <template #trailing>
                  <button
                    type="button"
                    class="flex items-center text-[#9ca3af] hover:text-[#4b5563] cursor-pointer"
                    @click="showConfirmPassword = !showConfirmPassword"
                  >
                    <UIcon
                      :name="showConfirmPassword ? 'i-lucide-eye-off' : 'i-lucide-eye'"
                      class="h-4 w-4"
                    />
                  </button>
                </template>
              </UInput>
            </div>
            <!-- Error Confirm Password -->
            <p v-if="confirmError" class="text-[11px] font-medium text-rose-500 transition-all">
              {{ confirmError }}
            </p>
          </div>

          <!-- Tombol Reset Password -->
          <UButton
            type="submit"
            block
            size="lg"
            :disabled="isButtonDisabled"
            :loading="isLoading"
            class="mt-6 h-11 rounded-xl bg-[#1a73e8] text-[14px] font-semibold text-white shadow-[0_8px_20px_-6px_rgba(26,115,232,0.5)] transition-all hover:bg-[#1557b0] active:scale-[0.99] disabled:bg-[#93c5fd] disabled:opacity-80 disabled:shadow-none cursor-pointer"
          >
            Reset Password
          </UButton>
        </form>

        <!-- Garis Pemisah (Divider) -->
        <div class="my-5 flex items-center">
          <div class="h-px flex-1 bg-[#f1f5f9]" />
          <span class="px-3 text-[12px] text-[#9ca3af]">or</span>
          <div class="h-px flex-1 bg-[#f1f5f9]" />
        </div>

        <!-- Tombol Back to Login -->
        <NuxtLink
          to="/login"
          class="inline-flex w-full items-center justify-center gap-2 text-[13px] font-medium text-[#4b5563] transition-colors hover:text-[#1a73e8]"
        >
          <UIcon name="i-lucide-arrow-left" class="h-4 w-4" />
          <span>Back to log in</span>
        </NuxtLink>
      </div>

      <!-- ========================================== -->
      <!-- STATE 2: BERHASIL DIRESET (SUCCESS CARD)   -->
      <!-- ========================================== -->
      <div v-else class="text-center">
        <!-- Icon Centang Hijau Sukses -->
        <div class="flex justify-center">
          <div
            class="flex h-12 w-12 items-center justify-center rounded-full bg-[#ecfdf5] text-[#059669]"
          >
            <UIcon name="i-lucide-check-circle-2" class="h-6 w-6 stroke-[1.8]" />
          </div>
        </div>

        <h2 class="mt-4 text-[22px] font-bold tracking-tight text-[#111827]">Password Reset!</h2>
        <p class="mt-1.5 text-[13px] text-[#6b7280] leading-relaxed">
          Your password has been successfully reset. You can now log in with your new credentials.
        </p>

        <!-- Tombol Menuju Login -->
        <UButton
          block
          size="lg"
          class="mt-6 h-11 rounded-xl bg-[#1a73e8] text-[14px] font-semibold text-white shadow-[0_8px_20px_-6px_rgba(26,115,232,0.5)] transition-all hover:bg-[#1557b0] active:scale-[0.99]"
          @click="navigateTo('/login')"
        >
          Proceed to Log in
        </UButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import blueBg from '~/assets/blue-bg.png'

const route = useRoute()
const toast = useToast()

// Ambil token dari URL query (?token=...)
const token = computed(() => (route.query.token as string) || '')

// State Form
const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const isLoading = ref(false)
const isSuccess = ref(false)

// Validasi Real-time Password Baru (Min. 8 Karakter)
const passwordError = computed(() => {
  if (!password.value) return ''
  if (password.value.length < 8) {
    return 'Password must be at least 8 characters.'
  }
  return ''
})

// Validasi Real-time Konfirmasi Password
const confirmError = computed(() => {
  if (!confirmPassword.value) return ''
  if (confirmPassword.value !== password.value) {
    return 'Passwords do not match.'
  }
  return ''
})

// Kondisi tombol terkunci (Disabled)
const isButtonDisabled = computed(() => {
  return (
    isLoading.value ||
    !token.value ||
    !password.value ||
    !confirmPassword.value ||
    password.value.length < 8 ||
    password.value !== confirmPassword.value
  )
})

// Cek token saat komponen di-load
onMounted(() => {
  if (!token.value) {
    toast.add({
      title: 'Missing Token',
      description: 'Reset password token is missing from the URL.',
      color: 'warning'
    })
  }
})

// Submit Reset Password
const handleSubmit = async () => {
  if (isButtonDisabled.value) return

  isLoading.value = true

  try {
    // Simulasi delay panggilan API ke Backend
    await new Promise((resolve) => setTimeout(resolve, 800))

    /* Contoh jika nanti nembak Real API:
    await $fetch('/api/v1/auth/reset-password', {
      method: 'POST',
      body: {
        token: token.value,
        password: password.value
      }
    })
    */

    isSuccess.value = true
    toast.add({
      title: 'Success',
      description: 'Your password has been successfully reset.',
      color: 'success'
    })
  } catch (error: any) {
    toast.add({
      title: 'Reset Failed',
      description: error?.message || 'Token is invalid or expired. Please request a new one.',
      color: 'error'
    })
  } finally {
    isLoading.value = false
  }
}
</script>
