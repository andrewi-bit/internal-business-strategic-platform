<script setup lang="ts">
import { ref, computed } from 'vue'
import type { ActiveUser, UserRole } from '../types/types'

interface Props {
  users: ActiveUser[]
}

const props = defineProps<Props>()

const emit = defineEmits<{
  (e: 'manage-user', user: ActiveUser): void
  (e: 'export'): void
}>()

const search = ref('')
const selectedRole = ref('')
const selectedStatus = ref('')
const currentPage = ref(1)
const pageSize = 5

// Helper warna badge role
const getRoleBadgeClass = (role: UserRole) => {
  switch (role) {
    case 'Commercial':
      return 'bg-purple-50 text-purple-700 border-purple-200'
    case 'Engineer':
      return 'bg-blue-50 text-blue-700 border-blue-200'
    case 'Executive':
      return 'bg-amber-50 text-amber-700 border-amber-200'
    default:
      return 'bg-slate-50 text-slate-700 border-slate-200'
  }
}

// Filter pencarian, role, dan status
const filteredUsers = computed(() => {
  return props.users.filter((item) => {
    const matchSearch =
      !search.value ||
      item.name.toLowerCase().includes(search.value.toLowerCase()) ||
      item.email.toLowerCase().includes(search.value.toLowerCase())

    const matchRole = !selectedRole.value || item.role === selectedRole.value
    const matchStatus = !selectedStatus.value || item.status === selectedStatus.value

    return matchSearch && matchRole && matchStatus
  })
})

const paginatedUsers = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredUsers.value.slice(start, start + pageSize)
})

const totalPages = computed(() => Math.ceil(filteredUsers.value.length / pageSize) || 1)
</script>

<template>
  <div class="rounded-xl border border-slate-200/80 bg-white p-4 shadow-2xs space-y-3.5">
    <!-- 1. Header Card & Controls -->
    <div
      class="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between border-b border-slate-100 pb-3"
    >
      <div>
        <h2 class="text-xs font-bold text-slate-900 tracking-tight">Users</h2>
        <p class="text-[11px] text-slate-400">List of users with assigned roles.</p>
      </div>

      <!-- Controls: Search, Role Filter, Status Filter, Export -->
      <div class="flex flex-wrap items-center gap-2">
        <!-- Search Input -->
        <div class="relative w-52 sm:w-60">
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

        <!-- Filter by Role -->
        <select
          v-model="selectedRole"
          class="h-8.5 rounded-lg border border-slate-200 bg-white px-2.5 text-xs font-semibold text-slate-700 shadow-2xs focus:border-blue-500 focus:outline-none cursor-pointer"
        >
          <option value="">Filter by Role</option>
          <option value="Executive">Executive</option>
          <option value="Commercial">Commercial</option>
          <option value="Engineer">Engineer</option>
        </select>

        <!-- Filter by Status -->
        <select
          v-model="selectedStatus"
          class="h-8.5 rounded-lg border border-slate-200 bg-white px-2.5 text-xs font-semibold text-slate-700 shadow-2xs focus:border-blue-500 focus:outline-none cursor-pointer"
        >
          <option value="">Filter by Status</option>
          <option value="Active">Active</option>
          <option value="Inactive">Inactive</option>
        </select>

        <!-- Export Button -->
        <button
          type="button"
          class="inline-flex h-8.5 items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-3 text-xs font-semibold text-slate-700 shadow-2xs hover:bg-slate-50 cursor-pointer"
          @click="emit('export')"
        >
          <UIcon name="i-lucide-download" class="h-3.5 w-3.5 text-slate-500" />
          <span>Export</span>
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
            <th class="px-4 py-2.5">Role</th>
            <th class="px-4 py-2.5">Status</th>
            <th class="px-4 py-2.5">Assigned Date</th>
            <th class="py-2.5 pl-4 text-right">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 font-medium">
          <tr
            v-for="item in paginatedUsers"
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

            <!-- Role Badge -->
            <td class="px-4 py-2.5 whitespace-nowrap">
              <span
                class="inline-flex items-center rounded-md border px-2.5 py-0.5 text-[10px] font-semibold"
                :class="getRoleBadgeClass(item.role)"
              >
                {{ item.role }}
              </span>
            </td>

            <!-- Status Badge -->
            <td class="px-4 py-2.5 whitespace-nowrap">
              <span
                class="inline-flex items-center rounded-full border border-emerald-200 bg-emerald-50 px-2 py-0.2 text-[10px] font-semibold text-emerald-700"
              >
                {{ item.status }}
              </span>
            </td>

            <!-- Assigned Date -->
            <td class="px-4 py-2.5 whitespace-nowrap text-slate-600">
              {{ item.assignedDate }}
            </td>

            <!-- Actions -->
            <td class="py-2.5 pl-4 text-right whitespace-nowrap">
              <div class="inline-flex items-center gap-2">
                <button
                  type="button"
                  class="rounded-lg border border-slate-200 bg-white px-2.5 py-1 text-xs font-semibold text-slate-700 shadow-2xs hover:bg-slate-50 cursor-pointer"
                  @click="emit('manage-user', item)"
                >
                  Manage
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
        <span class="font-semibold text-slate-700">{{ paginatedUsers.length }}</span>
        of
        <span class="font-semibold text-slate-700">{{ filteredUsers.length }}</span>
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
