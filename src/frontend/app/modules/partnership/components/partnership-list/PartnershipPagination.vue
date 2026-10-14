<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  currentPage: number
  pageSize: number
  totalItems: number
}

const props = defineProps<Props>()

const emit = defineEmits<{
  (e: 'update:currentPage' | 'update:pageSize', value: number): void
}>()

const pageSizeOptions = [10, 25, 50]

const totalPages = computed(() => Math.max(1, Math.ceil(props.totalItems / props.pageSize)))

const startItem = computed(() =>
  props.totalItems === 0 ? 0 : (props.currentPage - 1) * props.pageSize + 1
)

const endItem = computed(() => Math.min(props.currentPage * props.pageSize, props.totalItems))

const pageItems = computed<(number | 'ellipsis')[]>(() => {
  const total = totalPages.value
  const current = props.currentPage
  if (total <= 7) {
    return Array.from({ length: total }, (_, index) => index + 1)
  }
  const pages: (number | 'ellipsis')[] = [1]
  const start = Math.max(2, current - 1)
  const end = Math.min(total - 1, current + 1)
  if (start > 2) pages.push('ellipsis')
  for (let page = start; page <= end; page += 1) pages.push(page)
  if (end < total - 1) pages.push('ellipsis')
  pages.push(total)
  return pages
})

const goToPage = (page: number) => {
  const clamped = Math.min(Math.max(1, page), totalPages.value)
  if (clamped !== props.currentPage) emit('update:currentPage', clamped)
}

const handleGoTo = (event: Event) => {
  const value = Number((event.target as HTMLInputElement).value)
  if (!Number.isNaN(value)) goToPage(value)
}

const handlePageSize = (event: Event) => {
  const value = Number((event.target as HTMLSelectElement).value)
  emit('update:pageSize', value)
}
</script>

<template>
  <div class="flex flex-col gap-2 lg:flex-row lg:items-center lg:justify-between">
    <div class="flex flex-wrap items-center gap-x-4 gap-y-1.5">
      <p class="text-[11px] font-medium text-slate-500">
        Showing <span class="font-semibold text-slate-700">{{ startItem }}</span> to
        <span class="font-semibold text-slate-700">{{ endItem }}</span> of
        <span class="font-semibold text-slate-700">{{ totalItems }}</span> partners
      </p>

      <div class="flex items-center gap-1.5">
        <span class="text-[11px] font-medium text-slate-500">Rows per page</span>
        <select
          :value="pageSize"
          class="h-6.5 rounded-md border border-slate-200 bg-white px-1.5 text-[11px] font-semibold text-slate-700 focus:border-blue-500 focus:outline-none cursor-pointer"
          @change="handlePageSize"
        >
          <option
            v-for="size in pageSizeOptions"
            :key="size"
            :value="size"
          >
            {{ size }}
          </option>
        </select>
      </div>
    </div>

    <div class="flex flex-wrap items-center gap-3">
      <div class="flex items-center gap-1">
        <button
          type="button"
          class="inline-flex h-6.5 w-6.5 items-center justify-center rounded-md border border-slate-200 bg-white text-slate-600 transition-colors hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40 cursor-pointer"
          :disabled="currentPage <= 1"
          aria-label="Previous page"
          @click="goToPage(currentPage - 1)"
        >
          <UIcon
            name="i-lucide-chevron-left"
            class="h-4 w-4"
          />
        </button>

        <template
          v-for="(item, index) in pageItems"
          :key="`${item}-${index}`"
        >
          <span
            v-if="item === 'ellipsis'"
            class="inline-flex h-6.5 w-6.5 items-center justify-center text-xs font-medium text-slate-400"
          >
            ...
          </span>
          <button
            v-else
            type="button"
            class="inline-flex h-6.5 w-6.5 items-center justify-center rounded-md text-xs font-semibold transition-all cursor-pointer"
            :class="
              currentPage === item
                ? 'bg-blue-600 text-white shadow-xs'
                : 'border border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
            "
            @click="goToPage(item)"
          >
            {{ item }}
          </button>
        </template>

        <button
          type="button"
          class="inline-flex h-6.5 w-6.5 items-center justify-center rounded-md border border-slate-200 bg-white text-slate-600 transition-colors hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40 cursor-pointer"
          :disabled="currentPage >= totalPages"
          aria-label="Next page"
          @click="goToPage(currentPage + 1)"
        >
          <UIcon
            name="i-lucide-chevron-right"
            class="h-4 w-4"
          />
        </button>
      </div>

      <div class="flex items-center gap-1.5">
        <span class="text-[11px] font-medium text-slate-500">Go to</span>
        <input
          type="number"
          :value="currentPage"
          :min="1"
          :max="totalPages"
          class="h-6.5 w-14 rounded-md border border-slate-200 bg-white px-1.5 text-[11px] font-semibold text-slate-700 focus:border-blue-500 focus:outline-none"
          @change="handleGoTo"
        >
      </div>
    </div>
  </div>
</template>
