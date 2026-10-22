<template>
  <AuthShell labelledby="login-title">
    <h1
      id="login-title"
      class="text-[26px] leading-tight font-semibold tracking-[-0.02em] text-blue-950"
    >
      Welcome back
    </h1>
    <p class="mt-2 text-[15px] leading-relaxed text-slate-500">
      Sign in to continue to your workspace.
    </p>

    <form class="mt-7 space-y-4" novalidate @submit.prevent="handleSubmit">
      <AuthInput
        id="login-email"
        v-model="form.email"
        label="Email"
        type="email"
        placeholder="you@company.com"
        autocomplete="email"
        :error="errors.email"
      />

      <AuthInput
        id="login-password"
        v-model="form.password"
        label="Password"
        type="password"
        placeholder="Enter your password"
        autocomplete="current-password"
        :error="errors.password"
      />

      <div class="flex justify-end">
        <NuxtLink
          to="/forgot-password"
          class="text-xs font-medium text-blue-600 transition-colors hover:text-blue-700"
        >
          Forgot password?
        </NuxtLink>
      </div>

      <p
        v-if="formMessage"
        class="rounded-xl px-3.5 py-2.5 text-xs font-medium"
        :class="
          formMessage.type === 'error' ? 'bg-rose-50 text-rose-600' : 'bg-blue-50 text-blue-700'
        "
        role="status"
      >
        {{ formMessage.text }}
      </p>

      <button
        type="submit"
        :disabled="isSubmitting || disabled"
        :aria-busy="isSubmitting"
        class="relative flex h-11 w-full cursor-pointer items-center justify-center rounded-xl bg-blue-600 px-5 text-[15px] font-semibold text-white shadow-[0_10px_24px_-12px_rgba(29,78,216,0.7)] transition-[background-color,box-shadow,transform] duration-200 ease-out hover:bg-blue-700 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 active:translate-y-px active:shadow-none disabled:cursor-not-allowed disabled:bg-slate-300 disabled:shadow-none"
      >
        <UIcon
          v-if="isSubmitting"
          name="i-lucide-loader-circle"
          aria-hidden="true"
          class="absolute left-4 size-5 animate-spin text-white"
        />
        Login
      </button>
    </form>

    <div class="mt-6 flex items-center gap-3">
      <span class="h-px flex-1 bg-slate-200" />
      <span class="text-xs font-medium text-slate-400">or continue with</span>
      <span class="h-px flex-1 bg-slate-200" />
    </div>

    <button
      type="button"
      :disabled="loading || disabled"
      :aria-busy="loading"
      class="relative mt-6 flex h-11 w-full cursor-pointer items-center justify-center rounded-xl border border-slate-200 bg-white px-12 text-[15px] font-medium whitespace-nowrap text-blue-950 transition-[background-color,border-color,box-shadow,transform] duration-200 ease-out hover:border-blue-300 hover:bg-blue-50 hover:shadow-[0_10px_24px_-12px_rgba(29,78,216,0.45)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 active:translate-y-px active:shadow-none disabled:cursor-not-allowed disabled:border-slate-200 disabled:bg-slate-50 disabled:text-slate-400 disabled:shadow-none"
      @click="handleGoogle"
    >
      <UIcon
        v-if="loading"
        name="i-lucide-loader-circle"
        aria-hidden="true"
        class="absolute left-4 size-5 animate-spin text-blue-600"
      />
      <UIcon
        v-else
        name="i-simple-icons-google"
        aria-hidden="true"
        class="absolute left-4 size-5 text-[#4285F4]"
      />
      Continue with Google
    </button>

    <p class="mt-6 text-center text-sm text-slate-500">
      Don't have an account?
      <NuxtLink
        to="/signup"
        class="font-semibold text-blue-600 transition-colors hover:text-blue-700"
      >
        Sign up
      </NuxtLink>
    </p>
  </AuthShell>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import AuthShell from './AuthShell.vue'
import AuthInput from './AuthInput.vue'
import { validateLogin, type AuthFieldErrors, type LoginValues } from '../validation'
import { useAuthStore } from '../stores/auth.store'

const { loading = false, disabled = false } = defineProps<{
  loading?: boolean
  disabled?: boolean
}>()

const authStore = useAuthStore()
const toast = useToast()

const form = reactive<LoginValues>({
  email: '',
  password: ''
})

const errors = reactive<AuthFieldErrors<keyof LoginValues>>({})
const isSubmitting = ref(false)
const formMessage = ref<{ type: 'error' | 'info'; text: string } | null>(null)

// Tetap pakai nama handleSubmit sesuai template form
const handleSubmit = async () => {
  formMessage.value = null
  errors.email = undefined
  errors.password = undefined

  // 1. Validasi form frontend
  const nextErrors = validateLogin(form)
  if (nextErrors.email || nextErrors.password) {
    Object.assign(errors, nextErrors)
    return
  }

  isSubmitting.value = true
  try {
    // 2. Hit API Login
    const response = await authStore.login({
      email: form.email.trim(),
      password: form.password
    })

    toast.add({
      title: 'Login Successful',
      description: response?.message || 'Welcome back!',
      color: 'success'
    })

    // 3. User sudah verified -> Masuk ke landing page
    await navigateTo('/landing', { replace: true })
  } catch (error: any) {
    // 4. CEK APAKAH ERROR KARENA "EMAIL BELUM DIVERIFIKASI"
    if (error?.code === 'EMAIL_NOT_VERIFIED' || error?.message === 'Email belum diverifikasi') {
      // Simpan email ke Pinia & pastikan flag kirim OTP = false (karena TIDAK hit resend OTP)
      authStore.setPendingEmail(form.email.trim())
      authStore.hasJustSentOtp = false

      toast.add({
        title: 'Verifikasi Diperlukan',
        description: 'Email belum diverifikasi. Mengarahkan ke halaman OTP...',
        color: 'warning'
      })
      // Tampilkan juga feedback teks di form
      formMessage.value = {
        type: 'info',
        text: 'Email belum diverifikasi. Mengarahkan ke halaman verifikasi OTP...'
      }
      // Beri jeda 2 detik (2000 ms) agar user sempat membaca toast
      await new Promise((resolve) => setTimeout(resolve, 2000))

      // Langsung pindah ke halaman OTP membawa email (tanpa hit resend OTP)
      await navigateTo(`/otp?email=${encodeURIComponent(form.email.trim())}`, { replace: true })
      return
    }

    // 5. Error biasa lainnya (Password salah, user tidak ditemukan, dll)
    const errorMsg = error?.message || 'Login failed. Please check your credentials.'

    formMessage.value = {
      type: 'error',
      text: errorMsg
    }

    toast.add({
      title: 'Login Failed',
      description: errorMsg,
      color: 'error'
    })
  } finally {
    isSubmitting.value = false
  }
}

const handleGoogle = () => {
  formMessage.value = {
    type: 'info',
    text: 'Google single sign-on is not configured yet. Provide the OAuth client credentials to enable it.'
  }
}
</script>
