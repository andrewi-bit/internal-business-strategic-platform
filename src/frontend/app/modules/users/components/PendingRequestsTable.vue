<script setup lang="ts">
import { ref, computed } from 'vue'
import type { PendingUserRequest } from '../types/types'

interface Props {
  requests?: PendingUserRequest[]
}

const props = withDefaults(defineProps<Props>(), {
  requests: () => []
})

const emit = defineEmits<{
  (e: 'review', user: PendingUserRequest): void
}>()

const search = ref('')
const currentPage = ref(1)
const pageSize = 5

// Filter pencarian aman (dengan fallback array kosong dan optional chaining)
const filteredRequests = computed(() => {
  const list = props.requests || []
  if (!search.value) return list
  const q = search.value.toLowerCase().trim()
  return list.filter(
    (item) =>
      item.name?.toLowerCase().includes(q) ||
      item.email?.toLowerCase().includes(q) ||
      item.division?.toLowerCase().includes(q) ||
      String(item.requestedRole || '')
        .toLowerCase()
        .includes(q)
  )
})

// Pagination
const paginatedRequests = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredRequests.value.slice(start, start + pageSize)
})

const totalPages = computed(() => Math.ceil(filteredRequests.value.length / pageSize) || 1)

// Helper badge style untuk Requested Role
const getRoleBadgeClass = (role?: string) => {
  const r = String(role || '').toLowerCase()
  if (r.includes('engineer')) {
    return 'bg-[#e8f2fe] text-[#2563eb]'
  }
  if (r.includes('commercial')) {
    return 'bg-[#f3e8ff] text-[#9333ea]'
  }
  return 'bg-[#fef3c7] text-[#b45309]'
}
</script>

<template>
  <div class="rounded-xl border border-slate-200/90 bg-white p-5 shadow-xs space-y-4 font-sans">
    <!-- 1. Header Card & Controls -->
    <div class="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
      <div>
        <h2 class="text-[15px] font-bold text-slate-900 tracking-tight">Pending Access Requests</h2>
        <p class="text-xs text-slate-500 mt-0.5">
          Users who have requested access to the platform and waiting for approval.
        </p>
      </div>

      <!-- Controls: Search & Date Filter persis gambar -->
      <div class="flex items-center gap-2.5">
        <!-- Search Input -->
        <div class="relative w-64 sm:w-72">
          <div
            class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400"
          >
            <UIcon name="i-lucide-search" class="h-4 w-4" />
          </div>
          <input
            v-model="search"
            type="text"
            placeholder="Search name, email, or division..."
            class="h-9 w-full rounded-lg border border-slate-200 bg-white py-1 pr-3 pl-9 text-xs text-slate-800 placeholder-slate-400 transition-colors focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
        </div>

        <!-- Filter by Date Button -->
        <button
          type="button"
          class="inline-flex h-9 items-center gap-2 rounded-lg border border-slate-200 bg-white px-3 text-xs font-medium text-slate-700 shadow-2xs hover:bg-slate-50 cursor-pointer"
        >
          <UIcon name="i-lucide-calendar" class="h-4 w-4 text-slate-500" />
          <span>Filter by Date</span>
          <UIcon name="i-lucide-chevron-down" class="h-3.5 w-3.5 text-slate-400" />
        </button>
      </div>
    </div>

    <!-- 2. Table Data (6 Kolom: Name, Email, Division, Requested Role, Request Date, Status, Actions) -->
    <div class="overflow-x-auto">
      <table class="w-full text-left text-xs">
        <thead class="border-b border-slate-100 text-xs font-semibold text-slate-900">
          <tr>
            <th class="py-3 pr-4 font-semibold">Name</th>
            <th class="px-4 py-3 font-semibold">Email</th>
            <th class="px-4 py-3 font-semibold">Division</th>
            <th class="px-4 py-3 font-semibold">Requested Role</th>
            <th class="px-4 py-3 font-semibold">
              <div class="inline-flex items-center gap-1.5 cursor-pointer">
                <span>Request Date</span>
                <UIcon name="i-lucide-chevrons-up-down" class="h-3.5 w-3.5 text-blue-600" />
              </div>
            </th>
            <th class="px-4 py-3 font-semibold">Status</th>
            <th class="py-3 pl-4 font-semibold text-center">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 text-xs">
          <tr
            v-for="item in paginatedRequests"
            :key="item.id"
            class="hover:bg-slate-50/50 transition-colors"
          >
            <!-- Name -->
            <td class="py-3.5 pr-4 whitespace-nowrap font-semibold text-slate-900">
              {{ item.name }}
            </td>

            <!-- Email -->
            <td class="px-4 py-3.5 whitespace-nowrap text-[#4b6b94]">
              {{ item.email }}
            </td>

            <!-- Division -->
            <td class="px-4 py-3.5 whitespace-nowrap text-slate-600">
              {{ item.division }}
            </td>

            <!-- Requested Role (Badge Pastel) -->
            <td class="px-4 py-3.5 whitespace-nowrap">
              <span
                class="inline-flex items-center rounded-md px-2.5 py-1 text-[11px] font-medium"
                :class="getRoleBadgeClass(item.requestedRole)"
              >
                {{ item.requestedRole }}
              </span>
            </td>

            <!-- Request Date -->
            <td class="px-4 py-3.5 whitespace-nowrap text-slate-600">
              {{ item.requestDate }}
            </td>

            <!-- Status Badge (Pending Yellow) -->
            <td class="px-4 py-3.5 whitespace-nowrap">
              <span
                class="inline-flex items-center rounded-md bg-[#fef3c7] px-2.5 py-1 text-[11px] font-medium text-[#b45309]"
              >
                {{ item.status }}
              </span>
            </td>

            <!-- Actions: Tombol Review Persis Gambar -->
            <td class="py-3.5 pl-4 text-center whitespace-nowrap">
              <button
                type="button"
                class="inline-flex h-8 items-center justify-center rounded-lg border border-blue-400 bg-white px-5 text-xs font-medium text-blue-600 shadow-2xs transition-all hover:bg-blue-50 active:scale-95 cursor-pointer"
                @click="emit('review', item)"
              >
                Review
              </button>
            </td>
          </tr>

          <tr v-if="paginatedRequests.length === 0">
            <td colspan="7" class="py-8 text-center text-xs text-slate-400">
              No pending access requests found.
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 3. Bottom Pagination -->
    <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between pt-2">
      <p class="text-xs text-slate-500">
        Showing
        <span class="font-normal">{{
          filteredRequests.length ? (currentPage - 1) * pageSize + 1 : 0
        }}</span>
        to
        <span class="font-normal">{{
          Math.min(currentPage * pageSize, filteredRequests.length)
        }}</span>
        of
        <span class="font-normal">{{ filteredRequests.length }}</span>
        results
      </p>

      <div class="flex items-center gap-1.5">
        <!-- Prev Button -->
        <button
          type="button"
          class="inline-flex h-7 w-7 items-center justify-center rounded-md border border-slate-200 bg-white text-slate-500 hover:bg-slate-50 disabled:opacity-40 cursor-pointer"
          :disabled="currentPage <= 1"
          @click="currentPage--"
        >
          <UIcon name="i-lucide-chevron-left" class="h-3.5 w-3.5" />
        </button>

        <!-- Page Numbers -->
        <button
          v-for="page in totalPages"
          :key="page"
          type="button"
          class="inline-flex h-7 w-7 items-center justify-center rounded-md text-xs font-medium cursor-pointer"
          :class="[
            currentPage === page
              ? 'border border-blue-400 bg-[#e8f2fe] text-[#2563eb]'
              : 'border border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
          ]"
          @click="currentPage = page"
        >
          {{ page }}
        </button>

        <!-- Next Button -->
        <button
          type="button"
          class="inline-flex h-7 w-7 items-center justify-center rounded-md border border-slate-200 bg-white text-slate-500 hover:bg-slate-50 disabled:opacity-40 cursor-pointer"
          :disabled="currentPage >= totalPages"
          @click="currentPage++"
        >
          <UIcon name="i-lucide-chevron-right" class="h-3.5 w-3.5" />
        </button>
      </div>
    </div>
  </div>
</template>
