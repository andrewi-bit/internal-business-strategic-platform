<script setup lang="ts">
interface Props {
  industry: string
  technologies: string[]
  serviceType: string
  projectType: string
}

defineProps<Props>()
</script>

<template>
  <div class="space-y-4 rounded-2xl border border-slate-200/80 bg-white p-5 shadow-2xs">
    <!-- Header -->
    <div class="flex items-center gap-2 border-b border-slate-100 pb-3 text-slate-900">
      <UIcon name="i-lucide-box" class="h-4 w-4 text-blue-600" />
      <h3 class="text-sm font-bold">Industry & Technology</h3>
    </div>

    <div class="space-y-3.5 text-xs">
      <div class="flex items-center justify-between">
        <span class="text-slate-400 font-medium">Industry</span>
        <span class="font-semibold text-slate-800">{{ industry }}</span>
      </div>

      <div>
        <span class="text-slate-400 font-medium">Technology</span>
        <div class="mt-2 flex flex-wrap gap-1.5">
          <span
            v-for="tech in technologies"
            :key="tech"
            class="rounded-md bg-blue-50 border border-blue-100/80 px-2 py-0.5 text-[11px] font-semibold text-blue-600"
          >
            {{ tech }}
          </span>
        </div>
      </div>

      <div class="flex items-center justify-between border-t border-slate-50 pt-2">
        <span class="text-slate-400 font-medium">Service Type</span>
        <span class="font-semibold text-slate-800">{{ serviceType }}</span>
      </div>

      <div class="flex items-center justify-between">
        <span class="text-slate-400 font-medium">Project Type</span>
        <span class="font-semibold text-slate-800">{{ projectType }}</span>
      </div>
    </div>
  </div>
</template>
