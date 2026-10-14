<script setup lang="ts">
import type { PartnerDetailItem } from '../../types/detail.types'

interface Props {
  partner: PartnerDetailItem
}

defineProps<Props>()

const emit = defineEmits<{
  (e: 'edit'): void
}>()
</script>

<template>
  <div class="space-y-3">
    <!-- Breadcrumb -->
    <nav class="flex items-center gap-2 text-xs font-medium text-slate-500">
      <NuxtLink to="/partnership" class="hover:text-blue-600 transition-colors">
        Partnership
      </NuxtLink>
      <UIcon name="i-lucide-chevron-right" class="h-3 w-3 text-slate-400" />
      <NuxtLink to="/partnership" class="hover:text-blue-600 transition-colors">
        All Partners
      </NuxtLink>
      <UIcon name="i-lucide-chevron-right" class="h-3 w-3 text-slate-400" />
      <span class="font-semibold text-slate-800">
        {{ partner.code }}
      </span>
    </nav>

    <!-- Partner Hero Identity Header (Transparan, Tanpa Box Putih) -->
    <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between pt-1">
      <!-- Sisi Kiri: Logo + Info -->
      <div class="flex items-center gap-4">
        <!-- Logo Box Putih Kecil -->
        <div
          class="flex h-14 w-14 shrink-0 items-center justify-center rounded-xl border border-slate-200/80 bg-white p-2 shadow-2xs"
        >
          <img :src="partner.logo" :alt="partner.name" class="h-full w-full object-contain" />
        </div>

        <!-- Detail Text & Tags -->
        <div class="space-y-1">
          <p class="text-[11px] font-semibold text-slate-400 leading-none">
            {{ partner.code }}
          </p>

          <div class="flex flex-wrap items-center gap-2">
            <h1 class="text-xl font-bold tracking-tight text-slate-900 leading-none">
              {{ partner.name }}
            </h1>
            <span
              class="inline-flex items-center rounded-full bg-emerald-50 border border-emerald-200 px-2 py-0.2 text-[11px] font-semibold text-emerald-700"
            >
              {{ partner.status }}
            </span>
          </div>

          <p class="text-xs font-medium text-slate-500">
            {{ partner.legalName }}
          </p>

          <!-- Badges & Tags -->
          <div class="flex flex-wrap items-center gap-1.5 pt-0.5">
            <span
              class="rounded-md bg-blue-50 border border-blue-100 px-2 py-0.5 text-[10px] font-bold text-blue-600"
            >
              {{ partner.category }}
            </span>
            <span
              v-for="tag in partner.tags"
              :key="tag"
              class="rounded-md bg-white border border-slate-200/80 px-2 py-0.5 text-[10px] font-medium text-slate-600 shadow-2xs"
            >
              {{ tag }}
            </span>
            <span
              class="rounded-md bg-white border border-slate-200/80 px-2 py-0.5 text-[10px] font-semibold text-slate-500 shadow-2xs"
            >
              +2
            </span>
          </div>
        </div>
      </div>

      <!-- Sisi Kanan: Action Buttons -->
      <div class="flex items-center gap-2 self-start sm:self-center">
        <button
          type="button"
          class="inline-flex items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700 shadow-2xs transition-colors hover:bg-slate-50 cursor-pointer"
          @click="emit('edit')"
        >
          <UIcon name="i-lucide-edit" class="h-3.5 w-3.5 text-slate-500" />
          <span>Edit Partner</span>
        </button>

        <button
          type="button"
          class="inline-flex items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700 shadow-2xs transition-colors hover:bg-slate-50 cursor-pointer"
        >
          <span>More Actions</span>
          <UIcon name="i-lucide-chevron-down" class="h-3.5 w-3.5 text-slate-400" />
        </button>
      </div>
    </div>
  </div>
</template>
