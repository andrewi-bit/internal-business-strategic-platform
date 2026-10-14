<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'

const emit = defineEmits<{
  (e: 'add-partner'): void
  (e: 'export', scope: 'filtered' | 'all'): void
}>()

const isExportOpen = ref(false)
const exportContainer = ref<HTMLElement | null>(null)

interface ExportOption {
  scope: 'filtered' | 'all'
  label: string
  description: string
  icon: string
}

const exportOptions: ExportOption[] = [
  {
    scope: 'filtered',
    label: 'Export filtered',
    description: 'Current search & filters',
    icon: 'i-lucide-filter'
  },
  {
    scope: 'all',
    label: 'Export all partners',
    description: 'Every partner in the list',
    icon: 'i-lucide-database'
  }
]

const handleExport = (scope: 'filtered' | 'all') => {
  isExportOpen.value = false
  emit('export', scope)
}

const onDocumentClick = (event: MouseEvent) => {
  if (exportContainer.value && !exportContainer.value.contains(event.target as Node)) {
    isExportOpen.value = false
  }
}

onMounted(() => document.addEventListener('click', onDocumentClick))
onBeforeUnmount(() => document.removeEventListener('click', onDocumentClick))
</script>

<template>
  <div class="flex flex-col gap-1.5">
    <nav class="flex items-center gap-1 text-[11px] font-medium text-slate-400">
      <span>Partnership</span>
      <UIcon
        name="i-lucide-chevron-right"
        class="h-3 w-3"
      />
      <span class="font-semibold text-slate-700">All Partners</span>
    </nav>

    <div class="flex flex-col gap-1.5 lg:flex-row lg:items-center lg:justify-between">
      <div>
        <h1 class="text-base leading-5 font-bold tracking-tight text-slate-900">
          All Partners
        </h1>
        <p class="max-w-2xl text-[11px] leading-4 text-slate-500">
          Manage partner information, view collaboration status, and track partnership performance.
        </p>
      </div>

      <div class="flex shrink-0 items-center gap-1.5">
        <div
          ref="exportContainer"
          class="relative"
        >
          <button
            type="button"
            class="inline-flex h-7.5 items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-2.5 text-[11px] font-semibold text-slate-700 shadow-xs transition-colors hover:bg-slate-50 cursor-pointer"
            @click="isExportOpen = !isExportOpen"
          >
            <UIcon
              name="i-lucide-download"
              class="h-3.5 w-3.5 text-slate-500"
            />
            <span>Export</span>
            <UIcon
              name="i-lucide-chevron-down"
              class="h-3 w-3 text-slate-400 transition-transform duration-200"
              :class="{ 'rotate-180': isExportOpen }"
            />
          </button>

          <div
            v-show="isExportOpen"
            class="absolute right-0 z-50 mt-1.5 w-60 rounded-xl border border-slate-200 bg-white p-1.5 shadow-lg ring-1 ring-black/5"
          >
            <button
              v-for="option in exportOptions"
              :key="option.scope"
              type="button"
              class="flex w-full items-start gap-2.5 rounded-lg px-2.5 py-2 text-left transition-colors hover:bg-slate-50 cursor-pointer"
              @click="handleExport(option.scope)"
            >
              <UIcon
                :name="option.icon"
                class="mt-0.5 h-4 w-4 shrink-0 text-slate-400"
              />
              <span class="flex flex-col">
                <span class="text-xs font-semibold text-slate-800">{{ option.label }}</span>
                <span class="text-[11px] text-slate-400">{{ option.description }}</span>
              </span>
            </button>
          </div>
        </div>

        <button
          type="button"
          class="inline-flex h-7.5 items-center gap-1.5 rounded-lg bg-blue-600 px-2.5 text-[11px] font-semibold text-white shadow-sm transition-all hover:bg-blue-700 active:scale-95 cursor-pointer"
          @click="emit('add-partner')"
        >
          <UIcon
            name="i-lucide-plus"
            class="h-3.5 w-3.5"
          />
          <span>Add Partner</span>
        </button>
      </div>
    </div>
  </div>
</template>
