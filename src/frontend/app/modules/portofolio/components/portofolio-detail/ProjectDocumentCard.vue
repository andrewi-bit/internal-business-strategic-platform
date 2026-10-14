<script setup lang="ts">
import type { ProjectDocument } from '../../types/types'

interface Props {
  documents: ProjectDocument[]
}

defineProps<Props>()
</script>

<template>
  <div class="space-y-3 rounded-2xl border border-slate-200/80 bg-white p-5 shadow-2xs">
    <!-- Header -->
    <div class="flex items-center gap-2 border-b border-slate-100 pb-3 text-slate-900">
      <UIcon name="i-lucide-file-text" class="h-4 w-4 text-blue-600" />
      <h3 class="text-sm font-bold">Internal Documentation</h3>
    </div>

    <!-- Documents List -->
    <div class="space-y-2">
      <div
        v-for="doc in documents"
        :key="doc.name"
        class="group flex items-center justify-between rounded-xl border border-slate-100 bg-slate-50/50 p-2.5 transition-colors hover:bg-slate-100/70"
      >
        <div class="flex items-center gap-2.5 min-w-0">
          <div
            class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-rose-50 text-rose-600 font-bold text-[10px]"
          >
            PDF
          </div>
          <div class="min-w-0">
            <p
              class="text-xs font-bold text-slate-800 truncate group-hover:text-blue-600 transition-colors"
            >
              {{ doc.name }}
            </p>
            <p class="text-[10px] text-slate-400">{{ doc.size }} • {{ doc.date }}</p>
          </div>
        </div>

        <button
          type="button"
          class="flex h-7 w-7 shrink-0 items-center justify-center rounded-md text-slate-400 hover:bg-white hover:text-slate-700 hover:shadow-2xs cursor-pointer"
          aria-label="Download Document"
        >
          <UIcon name="i-lucide-download" class="h-3.5 w-3.5" />
        </button>
      </div>
    </div>
  </div>
</template>
