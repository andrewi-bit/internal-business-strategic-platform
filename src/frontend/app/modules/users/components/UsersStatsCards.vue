<script setup lang="ts">
import type { UserStats } from '../types/types'

interface Props {
  stats: UserStats
}

defineProps<Props>()
</script>

<template>
  <div class="grid grid-cols-1 gap-3.5 sm:grid-cols-2 lg:grid-cols-4">
    <!-- 1. Pending Requests Card -->
    <div
      class="flex items-center gap-3.5 rounded-xl border border-slate-200/80 bg-white p-4 shadow-2xs"
    >
      <div
        class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-amber-50 text-amber-600"
      >
        <UIcon name="i-lucide-clock" class="h-5 w-5" />
      </div>
      <div class="min-w-0 flex-1">
        <p class="text-xs font-semibold text-slate-500">Pending Requests</p>
        <p class="mt-0.5 text-2xl font-bold text-slate-900 leading-tight">
          {{ stats.pendingRequests }}
        </p>
        <p class="text-[11px] text-slate-400 truncate">Users waiting for role assignment</p>
      </div>
    </div>

    <!-- 2. Total Users Card -->
    <div
      class="flex items-center gap-3.5 rounded-xl border border-slate-200/80 bg-white p-4 shadow-2xs"
    >
      <div
        class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-blue-50 text-blue-600"
      >
        <UIcon name="i-lucide-users" class="h-5 w-5" />
      </div>
      <div class="min-w-0 flex-1">
        <p class="text-xs font-semibold text-slate-500">Total Users</p>
        <p class="mt-0.5 text-2xl font-bold text-slate-900 leading-tight">
          {{ stats.totalUsers }}
        </p>
        <p class="text-[11px] text-slate-400 truncate">All registered users</p>
      </div>
    </div>

    <!-- 3. Active Users Card -->
    <div
      class="flex items-center gap-3.5 rounded-xl border border-slate-200/80 bg-white p-4 shadow-2xs"
    >
      <div
        class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600"
      >
        <UIcon name="i-lucide-user-check" class="h-5 w-5" />
      </div>
      <div class="min-w-0 flex-1">
        <p class="text-xs font-semibold text-slate-500">Active Users</p>
        <p class="mt-0.5 text-2xl font-bold text-slate-900 leading-tight">
          {{ stats.activeUsers }}
        </p>
        <p class="text-[11px] text-slate-400 truncate">Users with assigned role</p>
      </div>
    </div>

    <!-- 4. Inactive Users Card -->
    <div
      class="flex items-center gap-3.5 rounded-xl border border-slate-200/80 bg-white p-4 shadow-2xs"
    >
      <div
        class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-slate-600"
      >
        <UIcon name="i-lucide-user-x" class="h-5 w-5" />
      </div>
      <div class="min-w-0 flex-1">
        <p class="text-xs font-semibold text-slate-500">Inactive Users</p>
        <p class="mt-0.5 text-2xl font-bold text-slate-900 leading-tight">
          {{ stats.inactiveUsers }}
        </p>
        <p class="text-[11px] text-slate-400 truncate">Deactivated users</p>
      </div>
    </div>
  </div>
</template>
