<script setup lang="ts">
const emit = defineEmits<{
  (e: 'add-project'): void
}>()
</script>

<template>
  <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
    <div>
      <h1 class="text-2xl font-bold tracking-tight text-slate-900">
        Portfolio Directory
      </h1>
      <p class="mt-1 text-sm text-slate-500">
        Browse and manage company project portfolio
      </p>
    </div>

    <!-- Tombol Add Project -->
    <button
      type="button"
      class="inline-flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition-all hover:bg-blue-700 active:scale-95 cursor-pointer"
      @click="emit('add-project')"
    >
      <UIcon
        name="i-lucide-plus"
        class="h-4 w-4"
      />
      <span>Add Portofolio</span>
    </button>
  </div>
</template>
