<script setup lang="ts">
import type { ProjectItem } from '../../types/types.ts'
import PortfolioCard from './PortofolioCard.vue'

interface Props {
  projects: ProjectItem[]
}

defineProps<Props>()

const emit = defineEmits<{
  (e: 'view-detail', project: ProjectItem): void
}>()
</script>

<template>
  <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
    <PortfolioCard
      v-for="item in projects"
      :key="item.id"
      :project="item"
      @view-detail="emit('view-detail', $event)"
    />
  </div>
</template>
