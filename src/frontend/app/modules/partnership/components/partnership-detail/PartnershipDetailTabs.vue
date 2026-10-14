<script setup lang="ts">
export type TabKey =
  | 'overview'
  | 'company-profile'
  | 'partnership-details'
  | 'legal-documents'
  | 'collaboration-history'
  | 'evaluation'
  | 'related-portfolios'
  | 'notes-activities'

interface Props {
  activeTab: TabKey
}

defineProps<Props>()

const emit = defineEmits<{
  (e: 'update:activeTab', tab: TabKey): void
}>()

const tabs: { key: TabKey; label: string; icon: string }[] = [
  { key: 'overview', label: 'Overview', icon: 'i-lucide-layout-grid' },
  { key: 'company-profile', label: 'Company Profile', icon: 'i-lucide-building-2' },
  { key: 'partnership-details', label: 'Partnership Details', icon: 'i-lucide-handshake' },
  { key: 'legal-documents', label: 'Legal Documents', icon: 'i-lucide-file-text' },
  { key: 'collaboration-history', label: 'Collaboration History', icon: 'i-lucide-history' },
  { key: 'evaluation', label: 'Evaluation & Performance', icon: 'i-lucide-trending-up' },
  { key: 'related-portfolios', label: 'Related Portfolios', icon: 'i-lucide-briefcase' },
  { key: 'notes-activities', label: 'Notes & Activities', icon: 'i-lucide-clipboard-list' }
]
</script>

<template>
  <!-- Container Tab Berwarna Putih dengan Border Halus -->
  <div class="rounded-xl border border-slate-200/80 bg-white px-2 shadow-2xs">
    <!-- Hilangkan scrollbar bawaan browser -->
    <div
      class="flex items-center gap-1 overflow-x-auto [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
    >
      <button
        v-for="tab in tabs"
        :key="tab.key"
        type="button"
        class="inline-flex items-center gap-1.5 border-b-2 px-3 py-2.5 text-xs font-semibold whitespace-nowrap transition-all cursor-pointer"
        :class="[
          activeTab === tab.key
            ? 'border-blue-600 text-blue-600'
            : 'border-transparent text-slate-500 hover:text-slate-800'
        ]"
        @click="emit('update:activeTab', tab.key)"
      >
        <UIcon :name="tab.icon" class="h-3.5 w-3.5" />
        <span>{{ tab.label }}</span>
      </button>
    </div>
  </div>
</template>
