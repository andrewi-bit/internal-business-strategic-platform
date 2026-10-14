<script setup lang="ts">
import { ref, computed } from 'vue'
import type { PendingUserRequest } from '../types/types'

interface Props {
  requests: PendingUserRequest[]
}

const props = defineProps<Props>()

const emit = defineEmits<{
  (e: 'assign-role', user: PendingUserRequest): void
}>()

const search = ref('')
const currentPage = ref(1)
const pageSize = 5

// Filter pencarian berdasarkan nama atau email
const filteredRequests = computed(() => {
  if (!search.value) return props.requests
  const q = search.value.toLowerCase()
  return props.requests.filter(
    (item) => item.name.toLowerCase().includes(q) || item.email.toLowerCase().includes(q)
  )
})

// Hitung data untuk pagination
const paginatedRequests = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredRequests.value.slice(start, start + pageSize)
})

const totalPages = computed(() => Math.ceil(filteredRequests.value.length / pageSize) || 1)
</script>

<template>
  <div class="rounded-xl border border-slate-200/80 bg-white p-4 shadow-2xs space-y-3.5">
    <!-- 1. Header Card & Controls -->
    <div
      class="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between border-b border-slate-100 pb-3"
    >
      <div>
        <h2 class="text-xs font-bold text-slate-900 tracking-tight">Pending Access Requests</h2>
        <p class="text-[11px] text-slate-400">
          Users who have requested access to the platform and waiting for role assignment.
        </p>
      </div>

      <!-- Controls: Search & Date Filter -->
      <div class="flex flex-wrap items-center gap-2">
        <!-- Search Input -->
        <div class="relative w-56 sm:w-64">
          <div
            class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-2.5 text-slate-400"
          >
            <UIcon name="i-lucide-search" class="h-3.5 w-3.5" />
          </div>
          <input
            v-model="search"
            type="text"
            placeholder="Search name or email..."
            class="h-8.5 w-full rounded-lg border border-slate-200 bg-white py-1 pr-3 pl-8 text-xs text-slate-800 placeholder-slate-400 transition-colors focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
        </div>

        <!-- Filter by Date -->
        <button
          type="button"
          class="inline-flex h-8.5 items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-2.5 text-xs font-semibold text-slate-700 shadow-2xs hover:bg-slate-50 cursor-pointer"
        >
          <UIcon name="i-lucide-calendar" class="h-3.5 w-3.5 text-slate-400" />
          <span>Filter by Date</span>
          <UIcon name="i-lucide-chevron-down" class="h-3 w-3 text-slate-400" />
        </button>
      </div>
    </div>

    <!-- 2. Table Data -->
    <div class="overflow-x-auto">
      <table class="w-full text-left text-xs">
        <thead class="border-b border-slate-100 text-[11px] font-bold text-slate-400">
          <tr>
            <th class="py-2.5 pr-4">Name</th>
            <th class="px-4 py-2.5">Email</th>
            <th class="px-4 py-2.5">Request Date</th>
            <th class="px-4 py-2.5">Status</th>
            <th class="py-2.5 pl-4 text-right">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 font-medium">
          <tr
            v-for="item in paginatedRequests"
            :key="item.id"
            class="hover:bg-slate-50/60 transition-colors"
          >
            <!-- Name -->
            <td class="py-2.5 pr-4 whitespace-nowrap font-bold text-slate-900">
              {{ item.name }}
            </td>

            <!-- Email -->
            <td class="px-4 py-2.5 whitespace-nowrap text-slate-500">
              {{ item.email }}
            </td>

            <!-- Request Date -->
            <td class="px-4 py-2.5 whitespace-nowrap text-slate-600">
              {{ item.requestDate }}
            </td>

            <!-- Status Badge -->
            <td class="px-4 py-2.5 whitespace-nowrap">
              <span
                class="inline-flex items-center rounded-full border border-amber-200 bg-amber-50 px-2.5 py-0.5 text-[10px] font-bold text-amber-700"
              >
                {{ item.status }}
              </span>
            </td>

            <!-- Actions -->
            <td class="py-2.5 pl-4 text-right whitespace-nowrap">
              <div class="inline-flex items-center gap-2">
                <button
                  type="button"
                  class="rounded-lg border border-blue-200 bg-blue-50/70 px-2.5 py-1 text-xs font-semibold text-blue-600 transition-colors hover:bg-blue-100 cursor-pointer"
                  @click="emit('assign-role', item)"
                >
                  Assign Role
                </button>

                <button
                  type="button"
                  class="inline-flex h-6 w-6 items-center justify-center rounded-md text-slate-400 hover:bg-slate-100 hover:text-slate-700 cursor-pointer"
                  aria-label="More"
                >
                  <UIcon name="i-lucide-more-vertical" class="h-3.5 w-3.5" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 3. Bottom Pagination -->
    <div
      class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between border-t border-slate-100 pt-3"
    >
      <p class="text-xs text-slate-500">
        Showing
        <span class="font-semibold text-slate-700">1</span>
        to
        <span class="font-semibold text-slate-700">{{ paginatedRequests.length }}</span>
        of
        <span class="font-semibold text-slate-700">{{ filteredRequests.length }}</span>
        results
      </p>

      <div class="flex items-center gap-1">
        <button
          type="button"
          class="inline-flex h-7 w-7 items-center justify-center rounded-lg border border-slate-200 bg-white text-slate-600 hover:bg-slate-50 disabled:opacity-40 cursor-pointer"
          :disabled="currentPage <= 1"
          @click="currentPage--"
        >
          <UIcon name="i-lucide-chevron-left" class="h-3.5 w-3.5" />
        </button>

        <button
          v-for="page in totalPages"
          :key="page"
          type="button"
          class="inline-flex h-7 w-7 items-center justify-center rounded-lg text-xs font-semibold cursor-pointer"
          :class="[
            currentPage === page
              ? 'bg-blue-600 text-white shadow-2xs'
              : 'border border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
          ]"
          @click="currentPage = page"
        >
          {{ page }}
        </button>

        <button
          type="button"
          class="inline-flex h-7 w-7 items-center justify-center rounded-lg border border-slate-200 bg-white text-slate-600 hover:bg-slate-50 disabled:opacity-40 cursor-pointer"
          :disabled="currentPage >= totalPages"
          @click="currentPage++"
        >
          <UIcon name="i-lucide-chevron-right" class="h-3.5 w-3.5" />
        </button>
      </div>
    </div>
  </div>
</template>
