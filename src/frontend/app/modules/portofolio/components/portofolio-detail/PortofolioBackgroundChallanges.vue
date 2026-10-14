<script setup lang="ts">
interface Props {
  background: string
  challenges: string[]
}

defineProps<Props>()
</script>

<template>
  <div class="space-y-4 rounded-2xl border border-slate-200/80 bg-white p-5 sm:p-6 shadow-2xs">
    <!-- Header -->
    <div class="flex items-center gap-2.5 text-slate-900">
      <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-50 text-blue-600">
        <UIcon name="i-lucide-file-text" class="h-4.5 w-4.5" />
      </div>
      <h2 class="text-base font-bold tracking-tight">Background & Challenges</h2>
    </div>

    <!-- 2-Col Grid: Background vs Challenges -->
    <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
      <!-- Background Card -->
      <div class="rounded-xl border border-blue-100 bg-blue-50/40 p-4 space-y-2">
        <div class="flex items-center gap-2 text-blue-700 font-bold text-xs sm:text-sm">
          <UIcon name="i-lucide-info" class="h-4 w-4 shrink-0 text-blue-600" />
          <span>Background</span>
        </div>
        <p class="text-xs sm:text-sm leading-relaxed text-slate-600">
          {{ background }}
        </p>
      </div>

      <!-- Challenges Card -->
      <div class="rounded-xl border border-rose-100 bg-rose-50/40 p-4 space-y-2">
        <div class="flex items-center gap-2 text-rose-700 font-bold text-xs sm:text-sm">
          <UIcon name="i-lucide-alert-circle" class="h-4 w-4 shrink-0 text-rose-600" />
          <span>Challenges</span>
        </div>
        <ul class="space-y-2 text-xs sm:text-sm text-slate-600">
          <li v-for="(item, idx) in challenges" :key="idx" class="flex items-start gap-2">
            <span class="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-rose-500" />
            <span>{{ item }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
