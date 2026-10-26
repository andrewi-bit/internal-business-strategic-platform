<template>
  <!-- Background Image Fullscreen dari assets/blue-bg.png -->
  <div
    class="relative isolate flex min-h-screen w-full items-center justify-center bg-cover bg-center bg-no-repeat p-4 font-sans select-none"
    :style="{ backgroundImage: `url(${blueBg})` }"
  >
    <!-- Card Utama (Proporsi & Shadow mengambang persis sesuai gambar) -->
    <div
      class="relative z-10 w-full rounded-[24px] bg-white px-8 py-9 shadow-[0_20px_60px_-15px_rgba(2,18,66,0.35)] sm:px-10 sm:py-10"
      style="max-width: 440px"
    >
      <!-- Icon Amplop Lingkaran Biru Pucat di Atas -->
      <div class="flex justify-center">
        <div
          class="flex h-12 w-12 items-center justify-center rounded-full bg-[#e8f1fd] text-[#1a73e8]"
        >
          <UIcon name="i-lucide-mail" class="h-6 w-6 stroke-[1.8]" />
        </div>
      </div>

      <!-- Header Teks -->
      <div class="mt-4 text-center">
        <h1 class="text-[22px] font-bold tracking-tight text-[#111827]">Verify Your Email</h1>
        <p class="mt-1 text-[13px] text-[#6b7280]">We've sent a 6-digit verification code to</p>

        <!-- Email Badge Pill -->
        <div class="mt-3 flex justify-center">
          <div
            class="inline-flex items-center gap-1.5 rounded-lg border border-[#e5eaf2] bg-[#f4f7fb] px-3 py-1.5 text-[13px] font-medium text-[#4b5563]"
          >
            <UIcon name="i-lucide-mail" class="h-3.5 w-3.5 text-[#1a73e8]" />
            <span>{{ email }}</span>
          </div>
        </div>
      </div>

      <!-- 6 Kotak Input OTP (Nuxt UI UPinInput) -->
      <div class="mt-7 flex flex-col items-center">
        <UPinInput
          v-model="otpDigits"
          :length="6"
          type="number"
          otp
          autofocus
          size="lg"
          class="justify-center gap-2 sm:gap-2.5"
          :ui="{
            base: 'h-11 w-11 sm:h-12 sm:w-12 text-center text-lg font-bold rounded-xl border border-[#e2e8f0] bg-white text-[#111827] shadow-none transition-all focus:border-[#1a73e8] focus:ring-2 focus:ring-[#1a73e8]/20'
          }"
          @complete="handleVerify"
        />

        <p class="mt-3 text-center text-[12px] text-[#9ca3af]">
          Enter the 6-digit code sent to your email.
        </p>
      </div>

      <!-- Tombol Verify Code (Warna Biru Royal sesuai gambar) -->
      <UButton
        block
        size="lg"
        :loading="isVerifying"
        :disabled="isVerifying || otpValue.length < 6"
        class="mt-6 h-11 rounded-xl bg-[#1a73e8] text-[14px] font-semibold text-white shadow-[0_8px_20px_-6px_rgba(26,115,232,0.5)] transition-all hover:bg-[#1557b0] active:scale-[0.99] disabled:bg-[#93c5fd] disabled:opacity-80 disabled:shadow-none"
        @click="handleVerify"
      >
        Verify Code
      </UButton>

      <!-- Garis Pemisah (Divider "or") -->
      <div class="my-5 flex items-center">
        <div class="h-px flex-1 bg-[#f1f5f9]" />
        <span class="px-3 text-[12px] text-[#9ca3af]">or</span>
        <div class="h-px flex-1 bg-[#f1f5f9]" />
      </div>

      <!-- Tombol Get OTP (02:00) -->
      <UButton
        block
        size="lg"
        variant="outline"
        color="neutral"
        :disabled="isTimerRunning || isRequesting"
        :loading="isRequesting"
        icon="i-lucide-rotate-ccw"
        class="h-11 rounded-xl cursor-pointer border-[#e2e8f0] bg-[#f8fafc] text-[13px] font-medium text-[#475569] transition-all hover:bg-[#f1f5f9] disabled:bg-[#f8fafc] disabled:text-[#94a3b8]"
        @click="handleGetOtp"
      >
        {{ isTimerRunning ? `Get OTP (${formattedTimer})` : 'Get OTP' }}
      </UButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import blueBg from '~/assets/blue-bg.png'
import { useAuthStore } from '../stores/auth.store'

const props = withDefaults(
  defineProps<{
    email?: string
    durationSeconds?: number
  }>(),
  {
    email: '',
    durationSeconds: 300 // 5 menit (300 detik)
  }
)

const emit = defineEmits<{
  (e: 'verify', code: string): void
  (e: 'get-otp'): void
}>()

const authStore = useAuthStore()
const route = useRoute()
const toast = useToast()

// 1. Resolusi Email: Ambil dari prop, state Pinia, atau URL Query (?email=...)
const email = computed(() => {
  if (props.email) return props.email
  const queryEmail = (route.query.email as string) || ''
  return authStore.pendingEmail || queryEmail
})

const otpDigits = ref<string[]>([])
const otpValue = computed(() => otpDigits.value.join(''))

const isVerifying = ref(false)
const isRequesting = ref(false)

// =========================================================================
// LOGIKA TIMER AKURAT (KEBAL REFRESH F5 DENGAN TIMESTAMP)
// =========================================================================
const timeLeft = ref(0)
const isTimerRunning = computed(() => timeLeft.value > 0)
let timerInterval: ReturnType<typeof setInterval> | null = null

const getStorageKey = () => `otp_expires_at_${email.value}`

// Menghitung sisa detik dari target timestamp yang tersimpan
const calculateTimeLeft = () => {
  if (!import.meta.client) return

  const savedExpiresAt = sessionStorage.getItem(getStorageKey())
  if (!savedExpiresAt) {
    timeLeft.value = 0
    if (timerInterval) {
      clearInterval(timerInterval)
      timerInterval = null
    }
    return
  }

  const diffMs = parseInt(savedExpiresAt, 10) - Date.now()
  const diffSec = Math.ceil(diffMs / 1000)

  if (diffSec > 0) {
    timeLeft.value = diffSec
  } else {
    // 5 Menit sudah lewat / habis
    timeLeft.value = 0
    if (timerInterval) {
      clearInterval(timerInterval)
      timerInterval = null
    }
  }
}

// Memulai timer 5 menit baru
const startTimer = (seconds = props.durationSeconds) => {
  if (!import.meta.client) return

  if (timerInterval) clearInterval(timerInterval)

  // Target selesai = jam saat ini + detik durasi
  const expiresAt = Date.now() + seconds * 1000
  sessionStorage.setItem(getStorageKey(), expiresAt.toString())

  calculateTimeLeft()

  timerInterval = setInterval(() => {
    calculateTimeLeft()
  }, 1000)
}

// Format tampilan MM:SS
const formattedTimer = computed(() => {
  const minutes = Math.floor(timeLeft.value / 60)
  const seconds = timeLeft.value % 60
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
})

// =========================================================================
// AKSI 1: USER KLIK TOMBOL "GET OTP" (MANUAL RESEND)
// =========================================================================
const handleGetOtp = async () => {
  if (isTimerRunning.value || isRequesting.value) return
  isRequesting.value = true
  try {
    emit('get-otp')
    await authStore.resendOtp(email.value)
    toast.add({
      title: 'OTP Resent',
      description: `A new 6-digit verification code has been sent to ${email.value}`,
      color: 'success'
    })

    // Mulai hitung mundur 5 menit baru
    startTimer(props.durationSeconds)
  } catch (error: any) {
    toast.add({
      title: 'Resend Failed',
      description: error?.message || 'Failed to resend OTP. Please try again.',
      color: 'error'
    })
  } finally {
    isRequesting.value = false
  }
}

// =========================================================================
// AKSI 2: USER KLIK TOMBOL "VERIFY CODE"
// =========================================================================
const handleVerify = async () => {
  if (otpValue.value.length !== 6) return

  isVerifying.value = true
  try {
    emit('verify', otpValue.value)
    await authStore.verifyEmail(email.value, otpValue.value)

    toast.add({
      title: 'Verification Successful',
      description: 'Your email has been verified.',
      color: 'success'
    })

    // Bersihkan storage timer dan pending state
    if (import.meta.client) {
      sessionStorage.removeItem(getStorageKey())
    }
    authStore.setPendingEmail('')
    authStore.hasJustSentOtp = false

    // Pindah ke landing page
    await navigateTo('/login', { replace: true })
  } catch (error: any) {
    toast.add({
      title: 'Verification Failed',
      description: error?.message || 'Invalid or expired OTP code. Please try again.',
      color: 'error'
    })
  } finally {
    isVerifying.value = false
  }
}

// =========================================================================
// LIFECYCLE & GUARD: DETEKSI DARI REGISTER vs REFRESH (F5)
// =========================================================================
onMounted(() => {
  // 1. Guard: Jika email kosong, tendang ke signup
  if (!email.value) {
    toast.add({
      title: 'Access Restricted',
      description: 'Please complete registration first.',
      color: 'warning'
    })
    navigateTo('/signup', { replace: true })
    return
  }

  // 2. Sinkronkan email dari URL Query ke Pinia jika F5
  if (!authStore.pendingEmail && email.value) {
    authStore.setPendingEmail(email.value)
  }

  // 3. LOGIKA PATEN TIMER:
  if (authStore.hasJustSentOtp) {
    // KONDISI A: Baru saja selesai Register/Login (State Pinia bernilai true)
    startTimer(props.durationSeconds)

    // Matikan flag-nya sekarang juga di memori
    // Jadi kalau nanti user tekan F5, flag ini sudah false!
    authStore.hasJustSentOtp = false
  } else {
    // KONDISI B: Halaman di-refresh (F5) -> authStore.hasJustSentOtp pasti false
    const savedExpiresAt = sessionStorage.getItem(getStorageKey())
    if (savedExpiresAt) {
      calculateTimeLeft()
      if (timeLeft.value > 0) {
        // Jika masih ada sisa waktu, lanjutkan countdown
        timerInterval = setInterval(() => {
          calculateTimeLeft()
        }, 1000)
      }
      // JIKA 5 MENIT SUDAH HABIS (timeLeft === 0), TETAP MATI! TIDAK JALAN LAGI!
    }
  }
})

onBeforeUnmount(() => {
  if (timerInterval) clearInterval(timerInterval)
})
</script>
