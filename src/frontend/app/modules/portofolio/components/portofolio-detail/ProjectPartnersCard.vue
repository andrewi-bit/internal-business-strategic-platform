<script setup lang="ts">
import type { RelatedPartner } from '../../types/types'

interface Props {
  partners: RelatedPartner[]
}

defineProps<Props>()
</script>

<template>
  <div class="space-y-3 rounded-2xl border border-slate-200/80 bg-white p-5 shadow-2xs">
    <!-- Header -->
    <div class="flex items-center gap-2 border-b border-slate-100 pb-3 text-slate-900">
      <UIcon name="i-lucide-users" class="h-4 w-4 text-blue-600" />
      <h3 class="text-sm font-bold">Related Partners</h3>
    </div>

    <!-- Partners List -->
    <div class="space-y-3">
      <div v-for="partner in partners" :key="partner.name" class="flex items-start gap-3">
        <!-- Partner Logo / Avatar Placeholder -->
        <div
          class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-slate-600 shadow-2xs"
        >
          <UIcon name="i-lucide-building-2" class="h-4.5 w-4.5" />
        </div>

        <div class="flex-1 min-w-0">
          <p class="text-xs font-bold text-slate-900 truncate">
            {{ partner.name }}
          </p>
          <p class="text-[11px] text-slate-500 font-medium">
            {{ partner.role }}
          </p>
          <div class="mt-1">
            <span
              class="inline-block rounded-md bg-slate-100 px-2 py-0.5 text-[10px] font-medium text-slate-600"
            >
              {{ partner.tag }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
