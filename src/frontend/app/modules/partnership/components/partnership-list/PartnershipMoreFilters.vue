<script setup lang="ts">
import { computed, ref } from 'vue'
import type {
  ContractEndPreset,
  LastUpdatedPreset,
  PartnershipAdvancedFilters
} from './partnership.types'
import { createAdvancedFilters, partnerTypes } from './partnership.data'
import PartnershipDateRangeFields from './PartnershipDateRangeFields.vue'

interface Props {
  modelValue: PartnershipAdvancedFilters
}

const props = defineProps<Props>()

const emit = defineEmits<{
  (e: 'apply', value: PartnershipAdvancedFilters): void
  (e: 'close'): void
}>()

const draft = ref<PartnershipAdvancedFilters>({
  ...props.modelValue,
  partnerTypes: [...props.modelValue.partnerTypes]
})

const contractEndOptions: { value: ContractEndPreset, label: string }[] = [
  { value: 'any', label: 'Any time' },
  { value: '30', label: 'Next 30 days' },
  { value: '90', label: 'Next 90 days' },
  { value: '180', label: 'Next 180 days' },
  { value: 'custom', label: 'Custom range' }
]

const lastUpdatedOptions: { value: LastUpdatedPreset, label: string }[] = [
  { value: 'any', label: 'Any time' },
  { value: '7', label: 'Last 7 days' },
  { value: '30', label: 'Last 30 days' },
  { value: '90', label: 'Last 90 days' },
  { value: 'custom', label: 'Custom range' }
]

const isPartnerTypeSelected = (value: string) => draft.value.partnerTypes.includes(value)

const togglePartnerType = (value: string) => {
  draft.value.partnerTypes = isPartnerTypeSelected(value)
    ? draft.value.partnerTypes.filter(item => item !== value)
    : [...draft.value.partnerTypes, value]
}

const contractEndError = computed(() => {
  if (draft.value.contractEndPreset !== 'custom') return ''
  const { contractEndStart: start, contractEndEnd: end } = draft.value
  return start && end && end < start ? 'End date cannot be earlier than the start date.' : ''
})

const lastUpdatedError = computed(() => {
  if (draft.value.lastUpdatedPreset !== 'custom') return ''
  const { lastUpdatedStart: start, lastUpdatedEnd: end } = draft.value
  return start && end && end < start ? 'End date cannot be earlier than the start date.' : ''
})

const hasDateError = computed(() => Boolean(contractEndError.value || lastUpdatedError.value))

const apply = () => {
  if (hasDateError.value) return
  emit('apply', { ...draft.value, partnerTypes: [...draft.value.partnerTypes] })
}

const reset = () => {
  draft.value = createAdvancedFilters()
}
</script>

<template>
  <section class="rounded-xl border border-slate-200/80 bg-white p-4 shadow-xs">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <UIcon
          name="i-lucide-sliders-horizontal"
          class="h-4 w-4 text-slate-500"
        />
        <h2 class="text-sm font-bold text-slate-800">
          More Filters
        </h2>
      </div>
      <button
        type="button"
        class="inline-flex h-8 w-8 items-center justify-center rounded-lg text-slate-400 transition-colors hover:bg-slate-100 hover:text-slate-700 cursor-pointer"
        aria-label="Close more filters"
        @click="emit('close')"
      >
        <UIcon
          name="i-lucide-x"
          class="h-4 w-4"
        />
      </button>
    </div>

    <div class="mt-3 grid grid-cols-1 gap-x-6 gap-y-4 lg:grid-cols-2">
      <div>
        <p class="text-xs font-semibold text-slate-600">
          Contract End Date
        </p>
        <div class="mt-2 space-y-1.5">
          <label
            v-for="option in contractEndOptions"
            :key="option.value"
            class="flex items-center gap-2 text-sm text-slate-700 cursor-pointer"
          >
            <input
              v-model="draft.contractEndPreset"
              type="radio"
              name="contract-end"
              :value="option.value"
              class="h-4 w-4 accent-blue-600"
            >
            <span>{{ option.label }}</span>
          </label>
        </div>

        <PartnershipDateRangeFields
          v-if="draft.contractEndPreset === 'custom'"
          v-model:start="draft.contractEndStart"
          v-model:end="draft.contractEndEnd"
          :error="contractEndError"
        />
      </div>

      <div>
        <p class="text-xs font-semibold text-slate-600">
          Last Updated
        </p>
        <div class="mt-2 space-y-1.5">
          <label
            v-for="option in lastUpdatedOptions"
            :key="option.value"
            class="flex items-center gap-2 text-sm text-slate-700 cursor-pointer"
          >
            <input
              v-model="draft.lastUpdatedPreset"
              type="radio"
              name="last-updated"
              :value="option.value"
              class="h-4 w-4 accent-blue-600"
            >
            <span>{{ option.label }}</span>
          </label>
        </div>

        <PartnershipDateRangeFields
          v-if="draft.lastUpdatedPreset === 'custom'"
          v-model:start="draft.lastUpdatedStart"
          v-model:end="draft.lastUpdatedEnd"
          :error="lastUpdatedError"
        />
      </div>

      <div>
        <p class="text-xs font-semibold text-slate-600">
          Partner Type
        </p>
        <div class="mt-2 grid grid-cols-1 gap-1.5 sm:grid-cols-2">
          <label
            v-for="option in partnerTypes"
            :key="option.value"
            class="flex items-center gap-2 text-sm text-slate-700 cursor-pointer"
          >
            <input
              type="checkbox"
              class="h-4 w-4 accent-blue-600"
              :checked="isPartnerTypeSelected(option.value)"
              @change="togglePartnerType(option.value)"
            >
            <span>{{ option.label }}</span>
          </label>
        </div>
      </div>

      <div>
        <p class="text-xs font-semibold text-slate-600">
          Has Active Project
        </p>
        <div class="mt-2 space-y-1.5">
          <label class="flex items-center gap-2 text-sm text-slate-700 cursor-pointer">
            <input
              v-model="draft.activeProjectWith"
              type="checkbox"
              class="h-4 w-4 accent-blue-600"
            >
            <span>With Active Project</span>
          </label>
          <label class="flex items-center gap-2 text-sm text-slate-700 cursor-pointer">
            <input
              v-model="draft.activeProjectWithout"
              type="checkbox"
              class="h-4 w-4 accent-blue-600"
            >
            <span>Without Active Project</span>
          </label>
        </div>
        <p class="mt-1.5 text-[11px] text-slate-400">
          Pick one to narrow results. Selecting both or neither shows all partners.
        </p>
      </div>
    </div>

    <div class="mt-4 flex items-center justify-end gap-3 border-t border-slate-100 pt-3">
      <button
        type="button"
        class="inline-flex h-8.5 items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-4 text-xs font-semibold text-slate-600 transition-colors hover:bg-slate-50 cursor-pointer"
        @click="reset"
      >
        <UIcon
          name="i-lucide-rotate-ccw"
          class="h-3.5 w-3.5 text-slate-500"
        />
        <span>Reset</span>
      </button>
      <button
        type="button"
        class="inline-flex h-8.5 items-center gap-2 rounded-lg bg-blue-600 px-4 text-xs font-semibold text-white shadow-sm transition-colors"
        :class="hasDateError ? 'cursor-not-allowed opacity-40' : 'hover:bg-blue-700 cursor-pointer'"
        :disabled="hasDateError"
        @click="apply"
      >
        <UIcon
          name="i-lucide-check"
          class="h-3.5 w-3.5"
        />
        <span>Apply Filters</span>
      </button>
    </div>
  </section>
</template>
