<script setup lang="ts">
import { ref, computed } from 'vue'

interface MediaItem {
  type: 'image' | 'video'
  url: string
  title: string
}

interface Props {
  media: MediaItem[]
}

const props = defineProps<Props>()

const activeTab = ref<'all' | 'image' | 'video'>('all')

const filteredMedia = computed(() => {
  if (activeTab.value === 'all') return props.media
  return props.media.filter((item) => item.type === activeTab.value)
})
</script>

<template>
  <div class="space-y-4 rounded-2xl border border-slate-200/80 bg-white p-5 sm:p-6 shadow-2xs">
    <!-- Header & Filter Tabs -->
    <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div class="flex items-center gap-2.5 text-slate-900">
        <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-50 text-blue-600">
          <UIcon name="i-lucide-image" class="h-4.5 w-4.5" />
        </div>
        <h2 class="text-base font-bold tracking-tight">Media Gallery</h2>
      </div>

      <!-- Tabs (All, Images, Videos) -->
      <div class="inline-flex items-center rounded-lg border border-slate-200 bg-slate-50 p-0.5">
        <button
          type="button"
          class="rounded-md px-3 py-1 text-xs font-semibold transition-all cursor-pointer"
          :class="[
            activeTab === 'all'
              ? 'bg-blue-600 text-white shadow-xs'
              : 'text-slate-600 hover:text-slate-900'
          ]"
          @click="activeTab = 'all'"
        >
          All
        </button>
        <button
          type="button"
          class="rounded-md px-3 py-1 text-xs font-semibold transition-all cursor-pointer"
          :class="[
            activeTab === 'image'
              ? 'bg-blue-600 text-white shadow-xs'
              : 'text-slate-600 hover:text-slate-900'
          ]"
          @click="activeTab = 'image'"
        >
          Images
        </button>
        <button
          type="button"
          class="rounded-md px-3 py-1 text-xs font-semibold transition-all cursor-pointer"
          :class="[
            activeTab === 'video'
              ? 'bg-blue-600 text-white shadow-xs'
              : 'text-slate-600 hover:text-slate-900'
          ]"
          @click="activeTab = 'video'"
        >
          Videos
        </button>
      </div>
    </div>

    <!-- 5 Thumbnail Gallery Grid -->
    <div class="grid grid-cols-2 gap-3 sm:grid-cols-5">
      <div
        v-for="(item, idx) in filteredMedia"
        :key="idx"
        class="group relative h-24 sm:h-28 overflow-hidden rounded-xl border border-slate-200 bg-slate-100 cursor-pointer shadow-2xs transition-all hover:scale-102"
      >
        <img
          :src="item.url"
          :alt="item.title"
          class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
          loading="lazy"
        />

        <!-- Video Play Icon Overlay -->
        <div
          v-if="item.type === 'video'"
          class="absolute inset-0 flex items-center justify-center bg-black/30 text-white backdrop-blur-2xs transition-opacity group-hover:bg-black/40"
        >
          <div
            class="flex h-8 w-8 items-center justify-center rounded-full bg-white/90 text-blue-600 shadow-md"
          >
            <UIcon name="i-lucide-play" class="h-4 w-4 fill-current ml-0.5" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
