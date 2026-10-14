<script setup lang="ts">
import { ref } from 'vue'
import type { ProjectStatus } from '../../types/types'

interface Props {
  title: string
  subtitle: string
  status: ProjectStatus
  images: string[]
  tags: string[]
}

const props = defineProps<Props>()

const currentSlide = ref(0)

const prevSlide = () => {
  if (currentSlide.value > 0) {
    currentSlide.value--
  } else {
    currentSlide.value = props.images.length - 1
  }
}

const nextSlide = () => {
  if (currentSlide.value < props.images.length - 1) {
    currentSlide.value++
  } else {
    currentSlide.value = 0
  }
}
</script>

<template>
  <div class="space-y-4">
    <!-- Image Carousel Container -->
    <div
      class="relative h-64 sm:h-80 w-full overflow-hidden rounded-2xl border border-slate-200/80 bg-slate-900 shadow-sm"
    >
      <!-- Active Image -->
      <img
        :src="images[currentSlide] || images[0]"
        :alt="title"
        class="h-full w-full object-cover transition-all duration-500"
      />

      <!-- Floating Badge Status di Pojok Kiri Atas -->
      <div class="absolute top-4 left-4">
        <span
          class="inline-flex items-center gap-1.5 rounded-full border border-emerald-200 bg-white/95 px-3 py-1 text-xs font-bold text-emerald-700 shadow-sm backdrop-blur-xs"
        >
          <span class="h-2 w-2 rounded-full bg-emerald-500" />
          <span>{{ status }}</span>
        </span>
      </div>

      <!-- Tombol Navigasi Carousel Kiri -->
      <button
        type="button"
        class="absolute top-1/2 left-4 -translate-y-1/2 flex h-9 w-9 items-center justify-center rounded-full bg-black/40 text-white backdrop-blur-xs transition-all hover:bg-black/60 active:scale-95 cursor-pointer"
        aria-label="Previous Slide"
        @click="prevSlide"
      >
        <UIcon name="i-lucide-chevron-left" class="h-5 w-5" />
      </button>

      <!-- Tombol Navigasi Carousel Kanan -->
      <button
        type="button"
        class="absolute top-1/2 right-4 -translate-y-1/2 flex h-9 w-9 items-center justify-center rounded-full bg-black/40 text-white backdrop-blur-xs transition-all hover:bg-black/60 active:scale-95 cursor-pointer"
        aria-label="Next Slide"
        @click="nextSlide"
      >
        <UIcon name="i-lucide-chevron-right" class="h-5 w-5" />
      </button>

      <!-- Slide Counter Indicator di Pojok Kanan Bawah -->
      <div
        class="absolute right-4 bottom-4 rounded-md bg-black/60 px-2.5 py-1 text-xs font-semibold text-white backdrop-blur-xs"
      >
        {{ currentSlide + 1 }} / {{ images.length }}
      </div>
    </div>

    <!-- Title, Subtitle, & Badges -->
    <div class="space-y-2.5">
      <h1 class="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900">
        {{ title }}
      </h1>
      <p class="text-sm sm:text-base text-slate-500 leading-relaxed">
        {{ subtitle }}
      </p>

      <!-- Tags List -->
      <div class="flex flex-wrap gap-2 pt-1">
        <span
          v-for="tag in tags"
          :key="tag"
          class="rounded-lg bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700"
        >
          {{ tag }}
        </span>
      </div>
    </div>
  </div>
</template>
