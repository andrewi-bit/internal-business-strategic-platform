<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import type { FilterOption } from './partnership.types'

interface Props {
  modelValue: string[]
  label: string
  options: FilterOption[]
  searchPlaceholder?: string
}

const props = withDefaults(defineProps<Props>(), {
  searchPlaceholder: 'Search option...'
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string[]): void
}>()

const isOpen = ref(false)
const query = ref('')
const container = ref<HTMLElement | null>(null)
const searchInput = ref<HTMLInputElement | null>(null)

const filteredOptions = computed(() => {
  const keyword = query.value.trim().toLowerCase()
  if (!keyword) return props.options
  return props.options.filter(option => option.label.toLowerCase().includes(keyword))
})

const selectedCount = computed(() => props.modelValue.length)

const triggerLabel = computed(() => {
  if (selectedCount.value === 0) return props.label
  if (selectedCount.value === 1) return props.modelValue[0] ?? props.label
  return `${selectedCount.value} selected`
})

const isActive = computed(() => selectedCount.value > 0)

const isSelected = (value: string) => props.modelValue.includes(value)

const toggleOption = (value: string) => {
  const next = isSelected(value)
    ? props.modelValue.filter(item => item !== value)
    : [...props.modelValue, value]
  emit('update:modelValue', next)
}

const clearSelection = () => {
  emit('update:modelValue', [])
}

const toggleOpen = () => {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    query.value = ''
    nextTick(() => searchInput.value?.focus())
  }
}

const close = () => {
  isOpen.value = false
}

const onDocumentClick = (event: MouseEvent) => {
  if (container.value && !container.value.contains(event.target as Node)) {
    close()
  }
}

const onKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Escape') close()
}

onMounted(() => {
  document.addEventListener('mousedown', onDocumentClick)
  document.addEventListener('keydown', onKeydown)
})

onBeforeUnmount(() => {
  document.removeEventListener('mousedown', onDocumentClick)
  document.removeEventListener('keydown', onKeydown)
})
</script>

<template>
  <div
    ref="container"
    class="relative"
  >
    <button
      type="button"
      class="inline-flex h-8.5 w-full min-w-0 items-center justify-between gap-1.5 rounded-lg border bg-white px-2 text-[12px] font-medium transition-colors cursor-pointer"
      :class="
        isActive
          ? 'border-blue-500 text-blue-700 ring-1 ring-blue-500/30'
          : 'border-slate-200 text-slate-700 hover:bg-slate-50'
      "
      @click="toggleOpen"
    >
      <span class="flex min-w-0 items-center gap-1.5">
        <span class="truncate">{{ triggerLabel }}</span>
        <span
          v-if="isActive"
          class="inline-flex h-4 min-w-4 shrink-0 items-center justify-center rounded-full bg-blue-600 px-1 text-[10px] font-bold text-white"
        >
          {{ selectedCount }}
        </span>
      </span>
      <UIcon
        name="i-lucide-chevron-down"
        class="h-3.5 w-3.5 shrink-0 transition-transform duration-200"
        :class="{ 'rotate-180': isOpen }"
      />
    </button>

    <div
      v-show="isOpen"
      class="absolute left-0 z-50 mt-1.5 w-64 rounded-xl border border-slate-200 bg-white p-1.5 shadow-lg ring-1 ring-black/5"
    >
      <div class="relative mb-1.5">
        <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-2.5 text-slate-400">
          <UIcon
            name="i-lucide-search"
            class="h-3.5 w-3.5"
          />
        </div>
        <input
          ref="searchInput"
          v-model="query"
          type="text"
          :placeholder="searchPlaceholder"
          class="w-full rounded-lg border border-slate-200 bg-slate-50/60 py-1.5 pr-2.5 pl-8 text-xs text-slate-700 placeholder-slate-400 focus:border-blue-500 focus:bg-white focus:outline-none"
        >
      </div>

      <div class="max-h-56 space-y-0.5 overflow-y-auto">
        <button
          v-for="option in filteredOptions"
          :key="option.value"
          type="button"
          class="flex w-full items-center gap-2.5 rounded-lg px-2.5 py-1.5 text-left text-xs font-medium text-slate-700 transition-colors hover:bg-slate-50 cursor-pointer"
          @click="toggleOption(option.value)"
        >
          <span
            class="flex h-4 w-4 shrink-0 items-center justify-center rounded border transition-colors"
            :class="
              isSelected(option.value)
                ? 'border-blue-600 bg-blue-600 text-white'
                : 'border-slate-300 bg-white'
            "
          >
            <UIcon
              v-if="isSelected(option.value)"
              name="i-lucide-check"
              class="h-3 w-3"
            />
          </span>
          <span class="truncate">{{ option.label }}</span>
        </button>

        <p
          v-if="filteredOptions.length === 0"
          class="px-2.5 py-3 text-center text-xs text-slate-400"
        >
          No options found
        </p>
      </div>

      <div
        v-if="isActive"
        class="mt-1.5 border-t border-slate-100 pt-1.5"
      >
        <button
          type="button"
          class="flex w-full items-center justify-center gap-1.5 rounded-lg px-2.5 py-1.5 text-xs font-semibold text-slate-500 transition-colors hover:bg-slate-50 hover:text-rose-600 cursor-pointer"
          @click="clearSelection"
        >
          <UIcon
            name="i-lucide-rotate-ccw"
            class="h-3.5 w-3.5"
          />
          Reset selection
        </button>
      </div>
    </div>
  </div>
</template>
