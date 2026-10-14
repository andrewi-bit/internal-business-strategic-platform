<script setup lang="ts">
import DashboardCard from '../shared/DashboardCard.vue'
import CommercialStatusBadge from './CommercialStatusBadge.vue'

import type { FeaturedPartnership } from '../../types/commercial.types'

defineProps<{
  partnerships: FeaturedPartnership[]
}>()
</script>

<template>
  <DashboardCard
    title="Featured Partnerships"
    subtitle="Priority deals and engagements in progress"
    :padded="false"
  >
    <template #actions>
      <NuxtLink
        to="/partnership"
        class="inline-flex items-center gap-1 text-xs leading-4 font-semibold text-blue-600 transition-colors hover:text-blue-700"
      >
        <span>View all</span>
        <UIcon
          name="i-lucide-arrow-right"
          class="h-3.5 w-3.5"
        />
      </NuxtLink>
    </template>

    <div class="grid grid-cols-1 gap-3 px-4 pt-1 pb-4 sm:grid-cols-2 xl:grid-cols-4">
      <div
        v-for="item in partnerships"
        :key="item.id"
        class="group flex min-w-0 flex-col justify-between rounded-lg border border-slate-100 bg-slate-50/60 p-2.5 transition-colors hover:border-blue-100 hover:bg-blue-50/40"
      >
        <div class="flex min-w-0 items-center gap-2">
          <img
            :src="item.image"
            :alt="item.name"
            class="h-10 w-10 shrink-0 rounded-md object-cover"
            loading="lazy"
          >

          <div class="min-w-0 flex-1">
            <p
              class="truncate text-[11px] leading-4 font-semibold text-slate-900 transition-colors group-hover:text-blue-600"
              :title="item.name"
            >
              {{ item.name }}
            </p>
            <p
              class="mt-0.5 truncate text-[11px] leading-4 text-slate-500"
              :title="`${item.category} · ${item.client}`"
            >
              {{ item.category }} · {{ item.client }}
            </p>
          </div>

          <CommercialStatusBadge
            :status="item.status"
            class="shrink-0"
          />
        </div>

        <div class="mt-2">
          <div class="flex items-center justify-between gap-2">
            <span class="text-[11px] leading-4 text-slate-500">Potential</span>
            <span class="text-xs leading-4 font-semibold text-slate-900 tabular-nums">{{ item.value }}</span>
          </div>

          <div class="mt-1 flex items-center gap-2">
            <div class="h-1.5 min-w-0 flex-1 overflow-hidden rounded-full bg-slate-200">
              <div
                class="h-full rounded-full bg-blue-600"
                :style="{ width: `${item.progress}%` }"
              />
            </div>
            <span class="shrink-0 text-[11px] leading-4 font-semibold text-slate-600 tabular-nums">{{ item.progress }}%</span>
          </div>
        </div>
      </div>
    </div>
  </DashboardCard>
</template>
