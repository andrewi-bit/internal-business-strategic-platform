<script setup lang="ts">
interface Props {
  overviewText: string
}

defineProps<Props>()
</script>

<template>
  <div class="space-y-3 rounded-2xl border border-slate-200/80 bg-white p-5 sm:p-6 shadow-2xs">
    <div class="flex items-center gap-2.5 text-slate-900">
      <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-50 text-blue-600">
        <UIcon name="i-lucide-box" class="h-4.5 w-4.5" />
      </div>
      <h2 class="text-base font-bold tracking-tight">Project Overview</h2>
    </div>

    <p class="text-xs sm:text-sm leading-relaxed text-slate-600">
      {{ overviewText }}
    </p>
  </div>
</template>
