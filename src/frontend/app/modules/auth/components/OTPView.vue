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
        class="h-11 rounded-xl border-[#e2e8f0] bg-[#f8fafc] text-[13px] font-medium text-[#475569] transition-all hover:bg-[#f1f5f9] disabled:bg-[#f8fafc] disabled:text-[#94a3b8]"
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

const props = withDefaults(
  defineProps<{
    email?: string
    durationSeconds?: number
  }>(),
  {
    email: '',
    durationSeconds: 300 // 5 menit (05:00)
  }
)
const emit = defineEmits<{
  (e: 'verify', code: string): void
  (e: 'get-otp'): void
}>()

const route = useRoute()
const toast = useToast()

const email = computed(() => {
  if (props.email) return props.email
  return (route.query.email as string) || 'you@company.com'
})

const otpDigits = ref<string[]>([])
const otpValue = computed(() => otpDigits.value.join(''))

const isVerifying = ref(false)
const isRequesting = ref(false)
const timeLeft = ref(props.durationSeconds)
const isTimerRunning = computed(() => timeLeft.value > 0)
let timerInterval: ReturnType<typeof setInterval> | null = null

const formattedTimer = computed(() => {
  const minutes = Math.floor(timeLeft.value / 60)
  const seconds = timeLeft.value % 60
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
})

const startTimer = () => {
  if (timerInterval) clearInterval(timerInterval)
  timeLeft.value = props.durationSeconds

  timerInterval = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--
    } else {
      if (timerInterval) {
        clearInterval(timerInterval)
        timerInterval = null
      }
    }
  }, 1000)
}

const handleGetOtp = async () => {
  if (isTimerRunning.value || isRequesting.value) return
  isRequesting.value = true
  try {
    emit('get-otp')
    toast.add({
      title: 'OTP Resent',
      description: `A new 6-digit code has been sent to ${email.value}`,
      color: 'success'
    })
    startTimer()
  } finally {
    isRequesting.value = false
  }
}

const handleVerify = async () => {
  if (otpValue.value.length !== 6) return

  isVerifying.value = true
  try {
    emit('verify', otpValue.value)
    toast.add({
      title: 'Verification successful',
      description: 'Your email has been verified.',
      color: 'success'
    })
    await navigateTo('/dashboard')
  } catch (error) {
    toast.add({
      title: 'Verification failed',
      description: 'Please check your code and try again.',
      color: 'error'
    })
  } finally {
    isVerifying.value = false
  }
}

onMounted(() => {
  startTimer()
})

onBeforeUnmount(() => {
  if (timerInterval) clearInterval(timerInterval)
})
</script>
