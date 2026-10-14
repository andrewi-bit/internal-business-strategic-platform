<script setup lang="ts">
import type { PartnershipStat, StatTone } from './partnership.types'

defineProps<{
  stats: PartnershipStat[]
}>()

const toneClasses: Record<StatTone, string> = {
  blue: 'bg-blue-50 text-blue-600',
  emerald: 'bg-emerald-50 text-emerald-600',
  amber: 'bg-amber-50 text-amber-600',
  orange: 'bg-orange-50 text-orange-600',
  rose: 'bg-rose-50 text-rose-600'
}
</script>

<template>
  <div class="grid grid-cols-1 gap-1.5 sm:grid-cols-2 lg:grid-cols-5">
    <article
      v-for="stat in stats"
      :key="stat.key"
      class="flex min-w-0 items-center gap-1.5 rounded-lg border border-slate-200/80 bg-white p-1.5 shadow-xs"
    >
      <div
        class="flex h-6.5 w-6.5 shrink-0 items-center justify-center rounded-md"
        :class="toneClasses[stat.tone]"
      >
        <UIcon
          :name="stat.icon"
          class="h-3.5 w-3.5"
        />
      </div>

      <div class="min-w-0 leading-tight">
        <p class="text-[11px] leading-4 font-semibold text-slate-500">
          {{ stat.label }}
        </p>
        <p class="text-base leading-5 font-bold text-slate-900">
          {{ stat.value }}
        </p>
        <p
          v-if="stat.hint"
          class="text-[10px] leading-3.5 font-medium text-slate-400"
        >
          {{ stat.hint }}
        </p>
      </div>
    </article>
  </div>
</template>
