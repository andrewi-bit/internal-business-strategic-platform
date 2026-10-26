<script setup lang="ts">
import notFoundIllustration from '~/assets/404.png'

defineProps<{
  isLoggedIn?: boolean
}>()
</script>

<template>
  <div
    class="flex h-full w-full flex-col items-center justify-center p-6 text-center select-none overflow-hidden"
    :class="isLoggedIn ? 'min-h-full' : 'h-screen min-h-screen'"
    style="background-color: #f8fafc"
  >
    <!-- Gambar 404: Dikecilkan sesuai desain asli (compact & proporsional) -->
    <div class="flex items-center justify-center w-full max-w-[340px] sm:max-w-[380px]">
      <img
        :src="notFoundIllustration"
        alt="404 Page Not Found"
        class="h-auto max-h-[170px] sm:max-h-[190px] w-auto max-w-full object-contain pointer-events-none drop-shadow-xs"
      />
    </div>

    <!-- Teks Judul & Deskripsi Sesuai Desain Mockup -->
    <div class="mt-4 max-w-md space-y-1.5">
      <h1 class="text-xl sm:text-[22px] font-bold tracking-tight text-[#0f172a]">Page Not Found</h1>
      <p class="text-xs sm:text-[13px] text-[#64748b] leading-relaxed font-normal">
        The page you’re looking for doesn’t exist or may have been moved.<br
          class="hidden sm:inline"
        />
        Please check the URL or go back to a valid page.
      </p>
    </div>

    <!-- Action Buttons Berdampingan -->
    <div class="mt-5 flex flex-wrap items-center justify-center gap-3">
      <!-- Tombol Biru Solid (Back to Dashboard / Login) -->
      <UButton
        size="lg"
        variant="solid"
        icon="i-lucide-home"
        style="background-color: #1570ef; color: #ffffff"
        class="h-9.5 rounded-xl px-4.5 text-xs font-semibold shadow-xs hover:opacity-90 active:scale-95 transition-all cursor-pointer"
        :to="isLoggedIn ? '/dashboard' : '/login'"
      >
        {{ isLoggedIn ? 'Back to Dashboard' : 'Back to Login' }}
      </UButton>

      <!-- Tombol Outline (Go Back) -->
      <UButton
        size="lg"
        variant="outline"
        color="neutral"
        icon="i-lucide-arrow-left"
        class="h-9.5 rounded-xl border border-[#e2e8f0] bg-white px-4.5 text-xs font-semibold text-[#334155] shadow-xs hover:bg-slate-50 active:scale-95 transition-all cursor-pointer"
        @click="$router.back()"
      >
        Go Back
      </UButton>
    </div>
  </div>
</template>
