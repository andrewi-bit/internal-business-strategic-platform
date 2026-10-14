<script setup lang="ts">
import { computed } from 'vue'
import type { ContractStatus, PartnershipCategory, PartnershipStatus } from './partnership.types'

type BadgeVariant = 'partner' | 'contract' | 'category'

interface Props {
  status: string
  variant?: BadgeVariant
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'partner'
})

const categoryClasses: Record<PartnershipCategory, string> = {
  'Technology Partner': 'bg-blue-50 text-blue-700 border-blue-200',
  'Channel Partner': 'bg-violet-50 text-violet-700 border-violet-200',
  'Service Partner': 'bg-sky-50 text-sky-700 border-sky-200',
  'Marketing Partner': 'bg-pink-50 text-pink-700 border-pink-200'
}

const partnerStatusClasses: Record<PartnershipStatus, string> = {
  'Draft': 'bg-slate-100 text-slate-600 border-slate-200',
  'Under Review': 'bg-amber-50 text-amber-700 border-amber-200',
  'Active': 'bg-emerald-50 text-emerald-700 border-emerald-200',
  'Expired': 'bg-orange-50 text-orange-700 border-orange-200',
  'Terminated': 'bg-rose-50 text-rose-700 border-rose-200'
}

const partnerStatusDots: Record<PartnershipStatus, string> = {
  'Draft': 'bg-slate-400',
  'Under Review': 'bg-amber-500',
  'Active': 'bg-emerald-500',
  'Expired': 'bg-orange-500',
  'Terminated': 'bg-rose-500'
}

const contractStatusClasses: Record<ContractStatus, string> = {
  Active: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  Pending: 'bg-amber-50 text-amber-700 border-amber-200',
  Expired: 'bg-orange-50 text-orange-700 border-orange-200',
  Terminated: 'bg-rose-50 text-rose-700 border-rose-200'
}

const contractStatusDots: Record<ContractStatus, string> = {
  Active: 'bg-emerald-500',
  Pending: 'bg-amber-500',
  Expired: 'bg-orange-500',
  Terminated: 'bg-rose-500'
}

const badgeClass = computed(() => {
  if (props.variant === 'category') {
    return categoryClasses[props.status as PartnershipCategory] ?? 'bg-slate-100 text-slate-600 border-slate-200'
  }
  if (props.variant === 'contract') {
    return contractStatusClasses[props.status as ContractStatus] ?? 'bg-slate-100 text-slate-600 border-slate-200'
  }
  return partnerStatusClasses[props.status as PartnershipStatus] ?? 'bg-slate-100 text-slate-600 border-slate-200'
})

const dotClass = computed(() => {
  if (props.variant === 'category') return ''
  if (props.variant === 'contract') {
    return contractStatusDots[props.status as ContractStatus] ?? 'bg-slate-400'
  }
  return partnerStatusDots[props.status as PartnershipStatus] ?? 'bg-slate-400'
})
</script>

<template>
  <span
    class="inline-flex items-center gap-1 whitespace-nowrap rounded-full border px-1.5 py-0.5 text-[10px] font-semibold"
    :class="badgeClass"
  >
    <span
      v-if="variant !== 'category'"
      class="h-1.5 w-1.5 shrink-0 rounded-full"
      :class="dotClass"
    />
    {{ status }}
  </span>
</template>
