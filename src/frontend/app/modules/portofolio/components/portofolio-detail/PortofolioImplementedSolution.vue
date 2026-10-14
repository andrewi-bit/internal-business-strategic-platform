<script setup lang="ts">
interface Props {
  solutions: string[]
}

defineProps<Props>()
</script>

<template>
  <div class="space-y-4 rounded-2xl border border-slate-200/80 bg-white p-5 sm:p-6 shadow-2xs">
    <!-- Header -->
    <div class="flex items-center gap-2.5 text-slate-900">
      <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-50 text-blue-600">
        <UIcon name="i-lucide-cpu" class="h-4.5 w-4.5" />
      </div>
      <h2 class="text-base font-bold tracking-tight">Implemented Solution</h2>
    </div>

    <!-- Solution Description & Checklist -->
    <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
      We developed a modern, modular digital banking platform with a focus on security, scalability,
      and user experience. The solution includes:
    </p>

    <div class="grid grid-cols-1 gap-6 md:grid-cols-12 md:items-center">
      <!-- Left: Checklist Bullet Points -->
      <ul class="space-y-2.5 text-xs sm:text-sm text-slate-700 md:col-span-8">
        <li v-for="(sol, idx) in solutions" :key="idx" class="flex items-start gap-2.5">
          <div
            class="mt-0.5 flex h-4.5 w-4.5 shrink-0 items-center justify-center rounded-full bg-emerald-100 text-emerald-600"
          >
            <UIcon name="i-lucide-check" class="h-3 w-3" />
          </div>
          <span>{{ sol }}</span>
        </li>
      </ul>

      <!-- Right: Mockup Illustration Graphic -->
      <div class="flex items-center justify-center md:col-span-4">
        <div
          class="relative flex h-32 w-full items-center justify-center rounded-xl bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-100 p-3 shadow-inner"
        >
          <UIcon name="i-lucide-layers" class="h-16 w-16 text-blue-400/80" />
        </div>
      </div>
    </div>
  </div>
</template>
