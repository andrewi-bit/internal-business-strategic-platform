<script setup lang="ts">
import type { PartnerDetailItem } from '../../../types/detail.types'

interface Props {
  partner?: PartnerDetailItem
}

withDefaults(defineProps<Props>(), {
  partner: () => ({
    id: 'PTN-2026-001',
    code: 'PTN-2026-001',
    name: 'Google Cloud',
    legalName: 'Google LLC',
    logo: '',
    status: 'Active',
    partnershipSince: 'Jan 15, 2024',
    category: 'Technology Partner',
    tags: ['Cloud Platform', 'Data Analytics', 'AI & Machine Learning'],
    contract: {
      status: 'Active',
      validUntil: 'Dec 31, 2027',
      remainingTime: '1 year 2 months left'
    },
    companyOverview: {
      website: '',
      headquarters: '',
      industry: '',
      businessFocus: '',
      keyMarkets: [],
      description: ''
    },
    keyExpertise: [],
    keyContacts: [],
    quickInfo: {
      partnerType: '',
      hasActiveProject: true,
      activeProjectsCount: 3,
      lastEvaluation: '',
      nextEvaluation: ''
    },
    recentCollaborations: [],
    latestEvaluation: {
      overallScore: 85,
      ratingLabel: 'Good',
      evaluationDate: '',
      evaluator: '',
      recommendation: '',
      nextEvaluation: '',
      remarks: ''
    }
  })
})

const emit = defineEmits<{
  (e: 'edit-info'): void
  (e: 'edit-contract'): void
  (e: 'edit-capabilities'): void
  (e: 'go-to-legal'): void
}>()

// Daftar kapabilitas teknis terperinci
const capabilities = [
  {
    name: 'Cloud Platform',
    icon: 'i-lucide-cloud',
    iconColor: 'text-blue-600',
    description:
      'Infrastructure, migration, and cloud-native solutions on Google Cloud Platform (GCP).'
  },
  {
    name: 'Data Analytics',
    icon: 'i-lucide-bar-chart-2',
    iconColor: 'text-purple-600',
    description: 'Data warehouse, data visualization, and big data analytics solutions.'
  },
  {
    name: 'AI & Machine Learning',
    icon: 'i-lucide-cpu',
    iconColor: 'text-emerald-600',
    description: 'AI/ML platform, generative AI, and machine learning model deployment.'
  },
  {
    name: 'Security',
    icon: 'i-lucide-shield-check',
    iconColor: 'text-purple-600',
    description: 'Cloud security, identity management, and threat detection.'
  },
  {
    name: 'DevOps',
    icon: 'i-lucide-settings',
    iconColor: 'text-teal-600',
    description: 'CI/CD, infrastructure automation, and containerization.'
  }
]
</script>

<template>
  <div class="space-y-3.5">
    <!-- 1. Top Row: 2 Cards Grid (Partnership Info vs Contract Summary) -->
    <div class="grid grid-cols-1 gap-3.5 lg:grid-cols-2 items-stretch">
      <!-- Card 1: Partnership Information -->
      <div
        class="flex flex-col justify-between rounded-xl border border-slate-200/80 bg-white p-4 shadow-2xs space-y-3"
      >
        <div class="flex items-center justify-between border-b border-slate-100 pb-2.5">
          <h2 class="text-xs font-bold text-slate-900 tracking-tight">Partnership Information</h2>
          <button
            type="button"
            class="inline-flex items-center gap-1 rounded-md border border-slate-200 bg-white px-2 py-0.5 text-[11px] font-semibold text-slate-700 shadow-2xs hover:bg-slate-50 cursor-pointer"
            @click="emit('edit-info')"
          >
            <UIcon name="i-lucide-edit" class="h-3 w-3 text-slate-500" />
            <span>Edit</span>
          </button>
        </div>

        <div class="space-y-3 text-xs flex-1">
          <div class="grid grid-cols-3 gap-2">
            <span class="text-slate-400 font-medium">Partnership ID</span>
            <span class="col-span-2 font-semibold text-slate-800">{{ partner.code }}</span>
          </div>

          <div class="grid grid-cols-3 gap-2 items-center">
            <span class="text-slate-400 font-medium">Partnership Category</span>
            <div class="col-span-2">
              <span
                class="inline-flex rounded-md bg-blue-50 border border-blue-100 px-2 py-0.5 text-[11px] font-semibold text-blue-600"
              >
                {{ partner.category }}
              </span>
            </div>
          </div>

          <div class="grid grid-cols-3 gap-2 items-center">
            <span class="text-slate-400 font-medium">Partnership Status</span>
            <div class="col-span-2">
              <span
                class="inline-flex items-center rounded-full bg-emerald-50 border border-emerald-200 px-2 py-0.2 text-[10px] font-semibold text-emerald-700"
              >
                {{ partner.status }}
              </span>
            </div>
          </div>

          <div class="grid grid-cols-3 gap-2 items-start">
            <span class="text-slate-400 font-medium pt-0.5">Areas of Expertise</span>
            <div class="col-span-2 flex flex-wrap gap-1.5">
              <span
                v-for="item in [
                  'Cloud Platform',
                  'Data Analytics',
                  'AI & Machine Learning',
                  'Security',
                  'DevOps'
                ]"
                :key="item"
                class="rounded-md bg-slate-100 px-2 py-0.5 text-[10px] font-medium text-slate-600"
              >
                {{ item }}
              </span>
            </div>
          </div>

          <div class="grid grid-cols-3 gap-2 border-t border-slate-50 pt-2.5">
            <span class="text-slate-400 font-medium">Partnership Description</span>
            <p class="col-span-2 leading-relaxed text-slate-600">
              Strategic technology partnership to deliver cloud infrastructure, data analytics, and
              AI/ML solutions for enterprise customers, supporting digital transformation and
              innovation.
            </p>
          </div>
        </div>
      </div>

      <!-- Card 2: Contract Summary -->
      <div
        class="flex flex-col justify-between rounded-xl border border-slate-200/80 bg-white p-4 shadow-2xs space-y-3"
      >
        <div class="flex items-center justify-between border-b border-slate-100 pb-2.5">
          <h2 class="text-xs font-bold text-slate-900 tracking-tight">Contract Summary</h2>
          <button
            type="button"
            class="inline-flex items-center gap-1 rounded-md border border-slate-200 bg-white px-2 py-0.5 text-[11px] font-semibold text-slate-700 shadow-2xs hover:bg-slate-50 cursor-pointer"
            @click="emit('edit-contract')"
          >
            <UIcon name="i-lucide-edit" class="h-3 w-3 text-slate-500" />
            <span>Edit</span>
          </button>
        </div>

        <div class="space-y-3 text-xs flex-1">
          <div class="grid grid-cols-3 gap-2 items-center">
            <span class="text-slate-400 font-medium">Contract Status</span>
            <div class="col-span-2">
              <span
                class="inline-flex items-center rounded-full bg-emerald-50 border border-emerald-200 px-2 py-0.2 text-[10px] font-semibold text-emerald-700"
              >
                {{ partner.contract.status }}
              </span>
            </div>
          </div>

          <div class="grid grid-cols-3 gap-2">
            <span class="text-slate-400 font-medium">Contract Start Date</span>
            <span class="col-span-2 font-medium text-slate-800">Jan 15, 2024</span>
          </div>

          <div class="grid grid-cols-3 gap-2 items-center">
            <span class="text-slate-400 font-medium">Contract End Date</span>
            <div class="col-span-2 flex items-center gap-2">
              <span class="font-medium text-slate-800">{{ partner.contract.validUntil }}</span>
              <span
                class="rounded-full bg-blue-50 border border-blue-100 px-2 py-0.2 text-[10px] font-semibold text-blue-600"
              >
                1 year 2 months left
              </span>
            </div>
          </div>

          <div class="grid grid-cols-3 gap-2">
            <span class="text-slate-400 font-medium">Contract Type</span>
            <span class="col-span-2 font-medium text-slate-800">Master Partnership Agreement</span>
          </div>

          <div class="grid grid-cols-3 gap-2 items-center">
            <span class="text-slate-400 font-medium">Renewal Status</span>
            <div class="col-span-2">
              <span
                class="inline-flex items-center gap-1 rounded-full bg-blue-50 border border-blue-100 px-2.5 py-0.5 text-[10px] font-semibold text-blue-700"
              >
                <UIcon name="i-lucide-clock" class="h-3 w-3 text-blue-600" />
                <span>Auto-renewal (Under Review)</span>
              </span>
            </div>
          </div>
        </div>

        <!-- Info Callout Banner di Bawah Contract -->
        <div
          class="flex items-center justify-between rounded-lg border border-blue-100 bg-blue-50/50 p-2.5 text-xs"
        >
          <div class="flex items-center gap-2 text-slate-600">
            <UIcon name="i-lucide-info" class="h-4 w-4 shrink-0 text-blue-600" />
            <span class="text-[11px] leading-tight"
              >Detailed contract information and related documents can be found in Legal
              Documents.</span
            >
          </div>
          <button
            type="button"
            class="inline-flex items-center gap-1 shrink-0 font-semibold text-blue-600 hover:text-blue-700 hover:underline cursor-pointer text-[11px] ml-2"
            @click="emit('go-to-legal')"
          >
            <span>View Legal Documents</span>
            <UIcon name="i-lucide-arrow-right" class="h-3 w-3" />
          </button>
        </div>
      </div>
    </div>

    <!-- 2. Bottom Row: Expertise & Capabilities Full Width Card -->
    <div class="rounded-xl border border-slate-200/80 bg-white p-4 shadow-2xs space-y-3">
      <div class="flex items-center justify-between border-b border-slate-100 pb-2.5">
        <h2 class="text-xs font-bold text-slate-900 tracking-tight">Expertise & Capabilities</h2>
        <button
          type="button"
          class="inline-flex items-center gap-1 rounded-md border border-slate-200 bg-white px-2 py-0.5 text-[11px] font-semibold text-slate-700 shadow-2xs hover:bg-slate-50 cursor-pointer"
          @click="emit('edit-capabilities')"
        >
          <UIcon name="i-lucide-edit" class="h-3 w-3 text-slate-500" />
          <span>Edit</span>
        </button>
      </div>

      <div class="divide-y divide-slate-100">
        <div
          v-for="item in capabilities"
          :key="item.name"
          class="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-6 py-2.5 first:pt-1 last:pb-1 text-xs"
        >
          <!-- Nama & Icon (Lebar Tetap) -->
          <div class="flex items-center gap-2.5 sm:w-56 shrink-0">
            <UIcon :name="item.icon" class="h-4 w-4" :class="item.iconColor" />
            <span class="font-bold text-slate-800">{{ item.name }}</span>
          </div>

          <!-- Deskripsi Kapabilitas -->
          <p class="text-slate-600 leading-relaxed flex-1">
            {{ item.description }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
