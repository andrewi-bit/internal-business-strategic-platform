<template>
  <div
    class="relative isolate flex min-h-screen w-full items-center justify-center bg-cover bg-center bg-no-repeat p-4 font-sans select-none"
    :style="{ backgroundImage: `url(${blueBg})` }"
  >
    <div
      class="relative z-10 w-full rounded-[24px] bg-white px-8 py-9 shadow-[0_20px_60px_-15px_rgba(2,18,66,0.35)] sm:px-10 sm:py-10"
      style="max-width: 440px"
    >
      <!--  FORM INPUT EMAIL                  -->

      <div v-if="!isSubmitted">
        <div class="flex justify-center">
          <div
            class="flex h-12 w-12 items-center justify-center rounded-full bg-[#e8f1fd] text-[#1a73e8]"
          >
            <UIcon name="i-lucide-key-round" class="h-6 w-6 stroke-[1.8]" />
          </div>
        </div>

        <!-- Header Teks -->
        <div class="mt-4 text-center">
          <h1 class="text-[22px] font-bold tracking-tight text-[#111827]">Forgot Password?</h1>
          <p class="mt-1.5 text-[13px] text-[#6b7280] leading-relaxed">
            No worries! Enter your registered email and we’ll send you a link to reset your
            password.
          </p>
        </div>

        <!-- Form Input -->
        <form class="mt-7 space-y-4" @submit.prevent="handleSubmit">
          <!-- Email Input Field -->
          <div class="space-y-1.5 text-left">
            <label for="email" class="block text-[12px] font-semibold text-[#374151]">
              Email Address
            </label>
            <UInput
              id="email"
              v-model.trim="email"
              type="email"
              icon="i-lucide-mail"
              placeholder="name@company.com"
              size="lg"
              block
              :disabled="isLoading"
              :ui="{
                base: 'h-11 rounded-xl text-[13px]',
                leading: 'ps-3.5 text-[#9ca3af]'
              }"
              :class="emailError ? '!border-rose-500 w-full focus:!ring-rose-500/20' : 'w-full'"
            />
            <!-- Pesan Error Real-Time Seiring Mengetik -->
            <p v-if="emailError" class="text-[12px] font-medium text-rose-500 transition-all">
              {{ emailError }}
            </p>
          </div>

          <!-- Tombol Kirim Reset Link -->
          <UButton
            type="submit"
            block
            size="lg"
            :disabled="isButtonDisabled"
            :loading="isLoading"
            class="mt-6 h-11 rounded-xl cursor-pointer bg-[#1a73e8] text-[14px] font-semibold text-white shadow-[0_8px_20px_-6px_rgba(26,115,232,0.5)] transition-all hover:bg-[#1557b0] active:scale-[0.99] disabled:bg-[#93c5fd] disabled:opacity-80 disabled:shadow-none"
          >
            Send Email
          </UButton>
        </form>

        <!-- Garis Pemisah (Divider) -->
        <div class="my-5 flex items-center">
          <div class="h-px flex-1 bg-[#bec0c3]" />
          <span class="px-3 text-[12px] text-[#767c86]">or</span>
          <div class="h-px flex-1 bg-[#bec0c3]" />
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

      <!--  SUCCESS CHECK EMAIL NOTIFICATION  -->

      <div v-else class="text-center">
        <!-- Icon Centang / Surat Terkirim -->
        <div class="flex justify-center">
          <div
            class="flex h-12 w-12 items-center justify-center rounded-full bg-[#ecfdf5] text-[#059669]"
          >
            <UIcon name="i-lucide-mail-check" class="h-6 w-6 stroke-[1.8]" />
          </div>
        </div>

        <h2 class="mt-4 text-[22px] font-bold tracking-tight text-[#111827]">Check your email</h2>
        <p class="mt-1 text-[13px] text-[#6b7280]">We have sent password reset link to:</p>

        <!-- Badge Email Terkirim -->
        <div class="mt-3 flex justify-center">
          <div
            class="inline-flex items-center gap-1.5 rounded-lg border border-[#e5eaf2] bg-[#f4f7fb] px-3 py-1.5 text-[13px] font-medium text-[#4b5563]"
          >
            <UIcon name="i-lucide-mail" class="h-3.5 w-3.5 text-[#1a73e8]" />
            <span>{{ email }}</span>
          </div>
        </div>

        <p class="mt-4 text-[13px] text-[#9ca3af] leading-relaxed">
          Didn't receive the email? Check your spam folder or try resending.
        </p>

        <!-- Tombol Resend / Retry -->
        <UButton
          block
          size="lg"
          variant="outline"
          color="neutral"
          :loading="isLoading"
          icon="i-lucide-rotate-ccw"
          class="mt-6 h-11 rounded-xl cursor-pointer border-[#e2e8f0] bg-[#f8fafc] text-[13px] font-medium text-[#475569] transition-all hover:bg-[#f1f5f9]"
          @click="handleSubmit"
        >
          Resend Email
        </UButton>

        <div class="mt-5">
          <NuxtLink
            to="/login"
            class="inline-flex items-center gap-2 text-[13px] font-medium text-[#4b5563] transition-colors hover:text-[#1a73e8]"
          >
            <UIcon name="i-lucide-arrow-left" class="h-4 w-4" />
            <span>Back to log in</span>
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import blueBg from '~/assets/blue-bg.png'
import { useAuthStore } from '../stores/auth.store'

const authStore = useAuthStore()
const toast = useToast()

const email = ref('')
const isLoading = ref(false)
const isSubmitted = ref(false)

// Regex format email standar
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

// Validasi real-time seiring user mengetik
const emailError = computed(() => {
  if (!email.value) return ''
  if (!emailRegex.test(email.value)) {
    return 'Email invalid, silahkan masukan email yang benar'
  }
  return ''
})

// Tombol disabled jika sedang loading, email kosong, atau format belum valid
const isButtonDisabled = computed(() => {
  return isLoading.value || !email.value || !!emailError.value
})

const handleSubmit = async () => {
  if (isButtonDisabled.value) return

  isLoading.value = true

  try {
    // 1. Tembak API Forgot Password Backend via Pinia Store
    const response = await authStore.forgotPassword(email.value.trim())

    // 2. Berhasil -> Tampilkan State 2 (Cek Email Kamu)
    isSubmitted.value = true

    toast.add({
      title: 'Instructions Sent',
      description: response?.message || `Password reset link has been sent to ${email.value}`,
      color: 'success'
    })
  } catch (error: any) {
    // 3. Gagal -> Tampilkan pesan error asli dari backend
    toast.add({
      title: 'Request Failed',
      description: error?.message || 'Failed to send reset instructions. Please try again.',
      color: 'error'
    })
  } finally {
    isLoading.value = false
  }
}
</script>
