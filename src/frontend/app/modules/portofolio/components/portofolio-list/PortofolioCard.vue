<script setup lang="ts">
import type { ProjectItem } from '../../types/types.ts'
import PortofolioStatusBadge from './PortofolioStatusBadge.vue'

interface Props {
  project: ProjectItem
}

defineProps<Props>()

const emit = defineEmits<{
  (e: 'view-detail', project: ProjectItem): void
}>()
</script>

<template>
  <div
    class="group flex flex-col overflow-hidden rounded-xl border border-slate-200/80 bg-white shadow-xs transition-all duration-200 hover:-translate-y-1 hover:shadow-md"
  >
    <!-- Card Image Header & Floating Status Badge -->
    <div class="relative h-44 w-full overflow-hidden bg-slate-100">
      <img
        :src="project.image"
        :alt="project.title"
        class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
        loading="lazy"
      />
      <!-- Floating Badge -->
      <div class="absolute top-3 left-3">
        <PortofolioStatusBadge :status="project.status" />
      </div>
    </div>

    <!-- Card Content Body -->
    <div class="flex flex-1 flex-col p-4.5">
      <!-- Title -->
      <h3
        class="text-base font-bold text-slate-900 group-hover:text-blue-600 transition-colors line-clamp-1"
      >
        {{ project.title }}
      </h3>

      <!-- Industry & Tech Badges -->
      <div class="mt-2.5 flex flex-wrap gap-1.5">
        <span class="rounded-md bg-slate-100 px-2 py-0.5 text-[11px] font-medium text-slate-600">
          {{ project.industry }}
        </span>
        <span
          v-for="tech in project.technologies"
          :key="tech"
          class="rounded-md bg-slate-100 px-2 py-0.5 text-[11px] font-medium text-slate-600"
        >
          {{ tech }}
        </span>
      </div>

      <!-- Description -->
      <p class="mt-3 flex-1 text-xs leading-relaxed text-slate-500 line-clamp-2">
        {{ project.description }}
      </p>

      <!-- Footer Info -->
      <div class="mt-4 flex items-center justify-between border-t border-slate-100 pt-3 text-xs">
        <span class="text-slate-400 font-medium"> Updated {{ project.updatedAt }} </span>

        <button
          type="button"
          class="inline-flex items-center gap-1 font-semibold text-blue-600 transition-colors hover:text-blue-700 cursor-pointer"
          @click="emit('view-detail', project)"
        >
          <span>View Details</span>
          <UIcon
            name="i-lucide-arrow-right"
            class="h-3.5 w-3.5 transition-transform group-hover:translate-x-0.5"
          />
        </button>
      </div>
    </div>
  </div>
</template>
