<script setup lang="ts">
import type { ProjectItem } from '../../types/types.ts'
import PortofolioStatusBadge from './PortofolioStatusBadge.vue'

interface Props {
  projects: ProjectItem[]
}

defineProps<Props>()

const emit = defineEmits<{
  (e: 'view-detail' | 'edit' | 'delete', project: ProjectItem): void
}>()
</script>

<template>
  <div class="overflow-hidden rounded-xl border border-slate-200/80 bg-white shadow-xs">
    <div class="overflow-x-auto">
      <table class="w-full text-left text-sm text-slate-600">
        <!-- Table Header -->
        <thead
          class="border-b border-slate-100 bg-slate-50/75 text-[11px] font-bold uppercase tracking-wider text-slate-500"
        >
          <tr>
            <th scope="col" class="py-3.5 pr-4 pl-6">Project</th>
            <th scope="col" class="px-4 py-3.5">Industry</th>
            <th scope="col" class="px-4 py-3.5">Technology</th>
            <th scope="col" class="px-4 py-3.5">Status</th>
            <th scope="col" class="px-4 py-3.5">Client</th>
            <th scope="col" class="px-4 py-3.5">Updated</th>
            <th scope="col" class="py-3.5 pr-6 pl-4 text-right">Action</th>
          </tr>
        </thead>

        <!-- Table Body -->
        <tbody class="divide-y divide-slate-100 font-medium">
          <tr
            v-for="item in projects"
            :key="item.id"
            class="transition-colors hover:bg-slate-50/80"
          >
            <!-- Project Name & Thumbnail -->
            <td class="py-3.5 pr-4 pl-6">
              <div class="flex items-center gap-3">
                <img
                  :src="item.image"
                  :alt="item.title"
                  class="h-10 w-12 shrink-0 rounded-lg object-cover shadow-2xs"
                  loading="lazy"
                />
                <span
                  class="font-bold text-slate-900 line-clamp-1 hover:text-blue-600 cursor-pointer"
                  @click="emit('view-detail', item)"
                >
                  {{ item.title }}
                </span>
              </div>
            </td>

            <!-- Industry -->
            <td class="px-4 py-3.5 whitespace-nowrap">
              <span
                class="rounded-md bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-700"
              >
                {{ item.industry }}
              </span>
            </td>

            <!-- Technology -->
            <td class="px-4 py-3.5">
              <div class="flex flex-wrap gap-1.5">
                <span
                  v-for="tech in item.technologies"
                  :key="tech"
                  class="rounded-md bg-slate-100 px-2 py-0.5 text-[11px] text-slate-600 font-medium"
                >
                  {{ tech }}
                </span>
              </div>
            </td>

            <!-- Status -->
            <td class="px-4 py-3.5 whitespace-nowrap">
              <PortofolioStatusBadge :status="item.status" />
            </td>

            <!-- Client -->
            <td class="px-4 py-3.5 whitespace-nowrap text-slate-800 text-xs font-semibold">
              {{ item.client }}
            </td>

            <!-- Updated -->
            <td class="px-4 py-3.5 whitespace-nowrap text-xs text-slate-400">
              {{ item.updatedAt }}
            </td>

            <!-- Action -->
            <td class="py-3.5 pr-6 pl-4 text-right whitespace-nowrap">
              <button
                type="button"
                class="inline-flex h-8 w-8 items-center justify-center rounded-lg text-slate-400 transition-colors hover:bg-slate-100 hover:text-slate-700 cursor-pointer"
                aria-label="Actions"
                @click="emit('view-detail', item)"
              >
                <UIcon name="i-lucide-more-vertical" class="h-4 w-4" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
