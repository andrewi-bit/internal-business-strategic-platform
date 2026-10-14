<script setup lang="ts">
import DashboardCard from '../shared/DashboardCard.vue'
// ✅ Benar (Sangat direkomendasikan):
import PortofolioStatusBadge from '~/modules/portofolio/components/portofolio-list/PortofolioStatusBadge.vue'
import type { FeaturedProject } from '../../types/types'

defineProps<{
  projects: FeaturedProject[]
}>()
</script>

<template>
  <DashboardCard
    title="Featured Portfolio"
    subtitle="Flagship engagements across the industry portfolio"
    :padded="false"
  >
    <template #actions>
      <NuxtLink
        to="/portofolio"
        class="inline-flex items-center gap-1 text-xs leading-4 font-semibold text-blue-600 transition-colors hover:text-blue-700"
      >
        <span>View all</span>
        <UIcon name="i-lucide-arrow-right" class="h-3.5 w-3.5" />
      </NuxtLink>
    </template>

    <div class="grid grid-cols-1 gap-3 px-4 pt-1 pb-4 sm:grid-cols-2 xl:grid-cols-4">
      <div
        v-for="project in projects"
        :key="project.id"
        class="group flex min-w-0 items-center gap-2 rounded-lg border border-slate-100 bg-slate-50/60 p-1 transition-colors hover:border-blue-100 hover:bg-blue-50/40"
      >
        <img
          :src="project.image"
          :alt="project.title"
          class="h-12 w-12 shrink-0 rounded-md object-cover"
          loading="lazy"
        />

        <div class="min-w-0 flex-1">
          <p
            class="truncate text-[11px] leading-4 font-semibold text-slate-900 transition-colors group-hover:text-blue-600"
            :title="project.title"
          >
            {{ project.title }}
          </p>

          <p
            class="mt-1 truncate text-[11px] leading-4 text-slate-500"
            :title="`${project.industry} · ${project.client}`"
          >
            {{ project.industry }} · {{ project.client }}
          </p>

          <div class="mt-1 flex items-center justify-between gap-2">
            <PortofolioStatusBadge :status="project.status" class="shrink-0" />
            <span
              class="shrink-0 text-[11px] leading-4 font-semibold tabular-nums text-emerald-600"
            >
              {{ project.roi }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </DashboardCard>
</template>
