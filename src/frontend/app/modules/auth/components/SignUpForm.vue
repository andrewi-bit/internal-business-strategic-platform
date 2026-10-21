<template>
  <AuthShell labelledby="signup-title">
    <h1
      id="signup-title"
      class="text-[26px] leading-tight font-semibold tracking-[-0.02em] text-blue-950"
    >
      Create your account
    </h1>
    <p class="mt-2 text-[15px] leading-relaxed text-slate-500">
      Set up your workspace access in a few seconds.
    </p>

    <form class="mt-7 space-y-4" novalidate @submit.prevent="handleSubmit">
      <AuthInput
        id="signup-name"
        v-model="form.fullName"
        label="Full Name"
        type="text"
        placeholder="Jane Doe"
        autocomplete="name"
        :disabled="isSubmitting"
        :error="errors.fullName"
      />

      <AuthInput
        id="signup-email"
        v-model="form.email"
        label="Email"
        type="email"
        placeholder="you@company.com"
        autocomplete="email"
        :disabled="isSubmitting"
        :error="errors.email"
      />

      <AuthInput
        id="signup-password"
        v-model="form.password"
        label="Password"
        type="password"
        placeholder="Create a password"
        autocomplete="new-password"
        :disabled="isSubmitting"
        :error="errors.password"
        :hint="PASSWORD_RULE_MESSAGE"
      />

      <AuthInput
        id="signup-confirm-password"
        v-model="form.confirmPassword"
        label="Confirm Password"
        type="password"
        placeholder="Re-enter your password"
        autocomplete="new-password"
        :disabled="isSubmitting"
        :error="errors.confirmPassword"
      />

      <!-- Feedback Error dari Server -->
      <p
        v-if="formMessage"
        class="rounded-xl px-3.5 py-2.5 text-xs font-medium"
        :class="
          formMessage.type === 'error'
            ? 'bg-rose-50 text-rose-600 border border-rose-200'
            : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
        "
        role="status"
      >
        {{ formMessage.text }}
      </p>

      <button
        type="submit"
        :disabled="isSubmitting"
        :aria-busy="isSubmitting"
        class="relative flex h-11 w-full cursor-pointer items-center justify-center rounded-xl bg-blue-600 px-5 text-[15px] font-semibold text-white shadow-[0_10px_24px_-12px_rgba(29,78,216,0.7)] transition-[background-color,box-shadow,transform] duration-200 ease-out hover:bg-blue-700 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 active:translate-y-px active:shadow-none disabled:cursor-not-allowed disabled:bg-slate-300 disabled:shadow-none"
      >
        <UIcon
          v-if="isSubmitting"
          name="i-lucide-loader-circle"
          aria-hidden="true"
          class="absolute left-4 size-5 animate-spin text-white"
        />
        {{ isSubmitting ? 'Creating account...' : 'Sign Up' }}
      </button>
    </form>

    <p class="mt-6 text-center text-sm text-slate-500">
      Already have an account?
      <NuxtLink
        to="/login"
        class="font-semibold text-blue-600 transition-colors hover:text-blue-700"
      >
        Back to Login
      </NuxtLink>
    </p>
  </AuthShell>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import AuthShell from './AuthShell.vue'
import AuthInput from './AuthInput.vue'
import {
  PASSWORD_RULE_MESSAGE,
  validateSignUp,
  type AuthFieldErrors,
  type SignUpValues
} from '../validation'
import { useAuthStore } from '../stores/auth.store'

const authStore = useAuthStore()
const toast = useToast()

const form = reactive<SignUpValues>({
  fullName: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const errors = reactive<AuthFieldErrors<keyof SignUpValues>>({})
const isSubmitting = ref(false)
const formMessage = ref<{ type: 'error' | 'info'; text: string } | null>(null)

const handleSubmit = async () => {
  formMessage.value = null
  errors.fullName = undefined
  errors.email = undefined
  errors.password = undefined
  errors.confirmPassword = undefined

  // 1. Validasi Frontend
  const nextErrors = validateSignUp(form)
  if (
    nextErrors.fullName ||
    nextErrors.email ||
    nextErrors.password ||
    nextErrors.confirmPassword
  ) {
    Object.assign(errors, nextErrors)
    return
  }

  isSubmitting.value = true
  try {
    // 2. Hit Register & Otomatis Minta OTP via Pinia Store
    const response = await authStore.register({
      full_name: form.fullName.trim(),
      email: form.email.trim(),
      password: form.password
    })

    // 3. Tampilkan Toast Sukses
    toast.add({
      title: 'Registration Successful',
      description:
        response?.message || 'Verification code has been sent to your email. Redirecting...',
      color: 'success'
    })

    formMessage.value = {
      type: 'info',
      text: 'Registration successful! Redirecting to email verification...'
    }

    // 4. Beri jeda 1.8 detik agar user sempat membaca feedback sukses
    await new Promise((resolve) => setTimeout(resolve, 1800))

    // 5. Pindah ke halaman OTP dengan email di query param (supaya di-refresh F5 tetap ada)
    await navigateTo(`/otp?email=${encodeURIComponent(form.email.trim())}`, { replace: true })
  } catch (error: any) {
    // 6. Tangkap Error dari Backend
    const errorMsg = error?.message || 'Registration failed. Please try again.'
    formMessage.value = {
      type: 'error',
      text: errorMsg
    }

    toast.add({
      title: 'Registration Failed',
      description: errorMsg,
      color: 'error'
    })
  } finally {
    isSubmitting.value = false
  }
}
</script>
