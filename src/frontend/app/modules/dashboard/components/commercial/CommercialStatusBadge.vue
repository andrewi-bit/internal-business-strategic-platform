<script setup lang="ts">
import type { CommercialStatus } from '../../types/commercial.types'

const props = defineProps<{
  status: CommercialStatus
}>()

const statusClasses: Record<CommercialStatus, string> = {
  'Lead': 'bg-slate-100 text-slate-600 border-slate-200',
  'New': 'bg-slate-100 text-slate-600 border-slate-200',
  'Qualified': 'bg-sky-50 text-sky-700 border-sky-200',
  'Proposal': 'bg-indigo-50 text-indigo-700 border-indigo-200',
  'In Progress': 'bg-amber-50 text-amber-700 border-amber-200',
  'Negotiation': 'bg-amber-50 text-amber-700 border-amber-200',
  'Won': 'bg-emerald-50 text-emerald-700 border-emerald-200',
  'Lost': 'bg-rose-50 text-rose-700 border-rose-200'
}

const badgeClass = computed(() => statusClasses[props.status] ?? 'bg-slate-50 text-slate-700 border-slate-200')
</script>

<template>
  <span
    class="inline-flex items-center rounded-full border px-2 py-0.5 text-[10px] leading-4 font-semibold"
    :class="badgeClass"
  >
    {{ status }}
  </span>
</template>
