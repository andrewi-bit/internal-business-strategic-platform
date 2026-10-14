<script setup lang="ts">
interface Props {
  locationName: string
}

defineProps<Props>()
</script>

<template>
  <div class="space-y-3 rounded-2xl border border-slate-200/80 bg-white p-5 shadow-2xs">
    <!-- Header -->
    <div class="flex items-center gap-2 border-b border-slate-100 pb-3 text-slate-900">
      <UIcon name="i-lucide-map-pin" class="h-4 w-4 text-blue-600" />
      <h3 class="text-sm font-bold">Project Location</h3>
    </div>

    <!-- Map Preview Placeholder Visual -->
    <div
      class="relative h-36 w-full overflow-hidden rounded-xl border border-slate-200 bg-slate-100"
    >
      <!-- Background Map Texture Graphic -->
      <div
        class="absolute inset-0 bg-slate-100 bg-[radial-gradient(#cbd5e1_1px,transparent_1px)] [background-size:16px_16px] opacity-70"
      />

      <!-- Center Map Pin Marker -->
      <div class="absolute inset-0 flex flex-col items-center justify-center gap-1">
        <div
          class="flex items-center gap-1 rounded-md bg-white px-2 py-0.5 text-[11px] font-bold text-slate-800 shadow-md ring-1 ring-slate-900/5"
        >
          <UIcon name="i-lucide-map-pin" class="h-3 w-3 text-rose-500" />
          <span>{{ locationName }}</span>
        </div>
        <div class="h-3 w-3 rounded-full bg-rose-500 ring-4 ring-rose-200 animate-pulse" />
      </div>
    </div>
  </div>
</template>
