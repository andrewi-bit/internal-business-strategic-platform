<script setup lang="ts">
import type { PartnerDetailItem } from '../../../types/detail.types'

interface Props {
  partner: PartnerDetailItem
}

defineProps<Props>()

const emit = defineEmits<{
  (e: 'edit-overview'): void
  (e: 'edit-expertise'): void
  (e: 'view-all-collaborations'): void
  (e: 'view-all-evaluations'): void
}>()
</script>

<template>
  <div class="space-y-3.5">
    <!-- 1. Top 3 Status Cards -->
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
      <!-- Partnership Status Card -->
      <div
        class="flex items-center gap-4 rounded-xl border border-slate-200/80 bg-white p-4 shadow-2xs"
      >
        <div
          class="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600"
        >
          <UIcon name="i-lucide-handshake" class="h-6 w-6" />
        </div>
        <div class="min-w-0 flex-1">
          <p class="text-xs font-semibold text-slate-500">Partnership Status</p>
          <div class="mt-1 flex items-center gap-2">
            <span class="h-2 w-2 rounded-full bg-emerald-500" />
            <span class="text-base font-bold text-slate-900">{{ partner.status }}</span>
          </div>
          <p class="mt-0.5 text-xs text-slate-400">Since {{ partner.partnershipSince }}</p>
        </div>
      </div>

      <!-- Contract Status Card -->
      <div
        class="flex items-center gap-4 rounded-xl border border-slate-200/80 bg-white p-4 shadow-2xs"
      >
        <div
          class="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-blue-50 text-blue-600"
        >
          <UIcon name="i-lucide-file-text" class="h-6 w-6" />
        </div>
        <div class="min-w-0 flex-1">
          <p class="text-xs font-semibold text-slate-500">Contract Status</p>
          <div class="mt-1 flex items-center gap-2">
            <span class="h-2 w-2 rounded-full bg-emerald-500" />
            <span class="text-base font-bold text-slate-900">{{ partner.contract.status }}</span>
          </div>
          <p class="mt-0.5 text-xs text-slate-400">
            Valid until {{ partner.contract.validUntil }} ({{ partner.contract.remainingTime }})
          </p>
        </div>
      </div>

      <!-- Partnership Category Card -->
      <div
        class="flex items-center gap-4 rounded-xl border border-slate-200/80 bg-white p-4 shadow-2xs"
      >
        <div
          class="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-purple-50 text-purple-600"
        >
          <UIcon name="i-lucide-layers" class="h-6 w-6" />
        </div>
        <div class="min-w-0 flex-1">
          <p class="text-xs font-semibold text-slate-500">Partnership Category</p>
          <div class="mt-1.5">
            <span
              class="inline-flex rounded-md bg-blue-50 border border-blue-100 px-2.5 py-1 text-xs font-bold text-blue-600"
            >
              {{ partner.category }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 2. Middle Row: Company Overview vs Key Expertise & Quick Info -->
    <div class="grid grid-cols-1 gap-3.5 lg:grid-cols-12 items-start">
      <!-- Left: Company Overview (7 Kolom) -->
      <div
        class="rounded-xl border border-slate-200/80 bg-white p-4 shadow-2xs space-y-3.5 lg:col-span-7"
      >
        <div class="flex items-center justify-between border-b border-slate-100 pb-3">
          <h2 class="text-sm font-bold text-slate-900">Company Overview</h2>
          <button
            type="button"
            class="inline-flex items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-2.5 py-1 text-xs font-semibold text-slate-700 shadow-2xs hover:bg-slate-50 cursor-pointer"
            @click="emit('edit-overview')"
          >
            <UIcon name="i-lucide-edit" class="h-3 w-3 text-slate-500" />
            <span>Edit</span>
          </button>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-12 gap-3.5 items-start">
          <!-- Logo & Brand di Kiri -->
          <div
            class="sm:col-span-4 flex flex-col items-center justify-center rounded-xl border border-slate-100 bg-slate-50/50 p-4 text-center"
          >
            <img :src="partner.logo" :alt="partner.name" class="h-16 w-16 object-contain" />
            <p class="mt-2 text-xs font-bold text-slate-800">
              {{ partner.name }}
            </p>
          </div>

          <!-- Metadata List di Kanan -->
          <div class="sm:col-span-8 space-y-3 text-xs">
            <div class="grid grid-cols-3 gap-2">
              <span class="text-slate-400 font-medium">Company Name</span>
              <span class="col-span-2 font-semibold text-slate-800">{{ partner.legalName }}</span>
            </div>

            <div class="grid grid-cols-3 gap-2">
              <span class="text-slate-400 font-medium">Website</span>
              <a
                :href="partner.companyOverview.website"
                target="_blank"
                class="col-span-2 inline-flex items-center gap-1 font-semibold text-blue-600 hover:underline"
              >
                <span>{{ partner.companyOverview.website }}</span>
                <UIcon name="i-lucide-external-link" class="h-3 w-3" />
              </a>
            </div>

            <div class="grid grid-cols-3 gap-2">
              <span class="text-slate-400 font-medium">Headquarters</span>
              <span class="col-span-2 font-medium text-slate-700">{{
                partner.companyOverview.headquarters
              }}</span>
            </div>

            <div class="grid grid-cols-3 gap-2">
              <span class="text-slate-400 font-medium">Industry</span>
              <span class="col-span-2 font-semibold text-slate-800">{{
                partner.companyOverview.industry
              }}</span>
            </div>

            <div class="grid grid-cols-3 gap-2">
              <span class="text-slate-400 font-medium">Business Focus</span>
              <span class="col-span-2 font-medium text-slate-700">{{
                partner.companyOverview.businessFocus
              }}</span>
            </div>

            <div class="grid grid-cols-3 gap-2 items-center">
              <span class="text-slate-400 font-medium">Key Markets</span>
              <div class="col-span-2 flex flex-wrap gap-1">
                <span
                  v-for="market in partner.companyOverview.keyMarkets"
                  :key="market"
                  class="rounded-md bg-slate-100 px-2 py-0.5 text-[10px] font-semibold text-slate-600"
                >
                  {{ market }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Description -->
        <div class="border-t border-slate-100 pt-4">
          <div class="grid grid-cols-1 sm:grid-cols-12 gap-2 text-xs">
            <span class="sm:col-span-3 text-slate-400 font-medium">Description</span>
            <p class="sm:col-span-9 leading-relaxed text-slate-600">
              {{ partner.companyOverview.description }}
            </p>
          </div>
        </div>
      </div>

      <!-- Right: Key Expertise & Quick Info (5 Kolom) -->
      <div class="space-y-3.5 lg:col-span-5">
        <!-- Key Expertise Card -->
        <div class="rounded-xl border border-slate-200/80 bg-white p-4 shadow-2xs space-y-4">
          <div class="flex items-center justify-between border-b border-slate-100 pb-3">
            <h2 class="text-sm font-bold text-slate-900">Key Expertise</h2>
            <button
              type="button"
              class="inline-flex items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-2.5 py-1 text-xs font-semibold text-slate-700 shadow-2xs hover:bg-slate-50 cursor-pointer"
              @click="emit('edit-expertise')"
            >
              <UIcon name="i-lucide-edit" class="h-3 w-3 text-slate-500" />
              <span>Edit</span>
            </button>
          </div>

          <div class="flex flex-wrap gap-2">
            <div
              v-for="exp in partner.keyExpertise"
              :key="exp.name"
              class="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 py-2 text-xs font-bold text-slate-700 shadow-2xs"
            >
              <UIcon :name="exp.icon" class="h-4 w-4 text-blue-600" />
              <span>{{ exp.name }}</span>
            </div>
          </div>
        </div>

        <!-- Quick Information Card -->
        <div class="rounded-xl border border-slate-200/80 bg-white p-4 shadow-2xs space-y-3.5">
          <div class="border-b border-slate-100 pb-3">
            <h2 class="text-sm font-bold text-slate-900">Quick Information</h2>
          </div>

          <div class="space-y-3 text-xs">
            <div class="flex items-center justify-between">
              <span class="text-slate-400 font-medium">Partner Type</span>
              <span class="font-semibold text-slate-800">{{ partner.quickInfo.partnerType }}</span>
            </div>

            <div class="flex items-center justify-between">
              <span class="text-slate-400 font-medium">Has Active Project</span>
              <span class="inline-flex items-center gap-1 font-semibold text-emerald-700">
                <UIcon name="i-lucide-check-circle-2" class="h-3.5 w-3.5 text-emerald-600" />
                <span>Yes ({{ partner.quickInfo.activeProjectsCount }} projects)</span>
              </span>
            </div>

            <div class="flex items-center justify-between">
              <span class="text-slate-400 font-medium">Last Evaluation</span>
              <span class="inline-flex items-center gap-1 font-medium text-slate-700">
                <UIcon name="i-lucide-info" class="h-3.5 w-3.5 text-slate-400" />
                <span>{{ partner.quickInfo.lastEvaluation }}</span>
              </span>
            </div>

            <div class="flex items-center justify-between">
              <span class="text-slate-400 font-medium">Next Evaluation</span>
              <span class="inline-flex items-center gap-1 font-medium text-slate-700">
                <UIcon name="i-lucide-info" class="h-3.5 w-3.5 text-slate-400" />
                <span>{{ partner.quickInfo.nextEvaluation }}</span>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 3. Bottom Row: Recent Collaboration vs Latest Evaluation -->
    <div class="grid grid-cols-1 gap-3.5 lg:grid-cols-12 items-start">
      <!-- Left: Recent Collaboration Table (7 Kolom) -->
      <div
        class="rounded-xl border border-slate-200/80 bg-white p-4 shadow-2xs space-y-4 lg:col-span-7"
      >
        <div class="flex items-center justify-between border-b border-slate-100 pb-3">
          <h2 class="text-sm font-bold text-slate-900">Recent Collaboration</h2>
          <button
            type="button"
            class="text-xs font-semibold text-blue-600 hover:text-blue-700 cursor-pointer"
            @click="emit('view-all-collaborations')"
          >
            View All
          </button>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead class="border-b border-slate-100 text-[11px] font-bold text-slate-400">
              <tr>
                <th class="py-2 pr-3">Project Name</th>
                <th class="px-3 py-2">Contribution</th>
                <th class="px-3 py-2">Status</th>
                <th class="px-3 py-2">Start Date</th>
                <th class="py-2 pl-3">End Date</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr
                v-for="item in partner.recentCollaborations"
                :key="item.id"
                class="hover:bg-slate-50/60"
              >
                <td class="py-3 pr-3">
                  <div class="flex items-center gap-2">
                    <div
                      class="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-blue-50 text-blue-600"
                    >
                      <UIcon name="i-lucide-briefcase" class="h-3.5 w-3.5" />
                    </div>
                    <div>
                      <p class="font-bold text-slate-800 line-clamp-1">{{ item.name }}</p>
                      <p class="text-[10px] text-slate-400">{{ item.code }}</p>
                    </div>
                  </div>
                </td>
                <td class="px-3 py-3 text-slate-600 font-medium whitespace-nowrap">
                  {{ item.contribution }}
                </td>
                <td class="px-3 py-3 whitespace-nowrap">
                  <span
                    class="rounded-full px-2 py-0.5 text-[10px] font-semibold"
                    :class="[
                      item.status === 'In Progress'
                        ? 'bg-blue-50 text-blue-700 border border-blue-200'
                        : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                    ]"
                  >
                    {{ item.status }}
                  </span>
                </td>
                <td class="px-3 py-3 text-slate-500 whitespace-nowrap">{{ item.startDate }}</td>
                <td class="py-3 pl-3 text-slate-500 whitespace-nowrap">{{ item.endDate }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Right: Latest Evaluation Scorecard (5 Kolom) -->
      <div
        class="rounded-xl border border-slate-200/80 bg-white p-4 shadow-2xs space-y-4 lg:col-span-5"
      >
        <div class="flex items-center justify-between border-b border-slate-100 pb-3">
          <h2 class="text-sm font-bold text-slate-900">Latest Evaluation</h2>
          <button
            type="button"
            class="text-xs font-semibold text-blue-600 hover:text-blue-700 cursor-pointer"
            @click="emit('view-all-evaluations')"
          >
            View All
          </button>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-12 gap-4 items-start">
          <!-- Score Box -->
          <div
            class="sm:col-span-5 flex flex-col items-center justify-center rounded-xl bg-emerald-50/70 border border-emerald-100 p-4 text-center"
          >
            <p class="text-[10px] font-semibold text-slate-500">Overall Score</p>
            <div class="mt-1 flex items-baseline gap-1">
              <span class="text-2xl font-bold text-slate-900">{{
                partner.latestEvaluation.overallScore
              }}</span>
              <span class="text-xs text-slate-400">/ 100</span>
            </div>
            <span
              class="mt-1.5 rounded-full bg-emerald-100 px-2.5 py-0.5 text-[10px] font-bold text-emerald-800"
            >
              {{ partner.latestEvaluation.ratingLabel }}
            </span>
          </div>

          <!-- Evaluation Info -->
          <div class="sm:col-span-7 space-y-2 text-xs">
            <div class="flex justify-between">
              <span class="text-slate-400">Evaluation Date</span>
              <span class="font-semibold text-slate-800">{{
                partner.latestEvaluation.evaluationDate
              }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-400">Evaluator</span>
              <span class="font-medium text-slate-700">{{
                partner.latestEvaluation.evaluator
              }}</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-slate-400">Recommendation</span>
              <span
                class="rounded-md bg-emerald-50 border border-emerald-200 px-2 py-0.5 text-[10px] font-bold text-emerald-700"
              >
                {{ partner.latestEvaluation.recommendation }}
              </span>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-400">Next Evaluation</span>
              <span class="font-medium text-slate-700">{{
                partner.latestEvaluation.nextEvaluation
              }}</span>
            </div>
          </div>
        </div>

        <!-- Remarks -->
        <div class="border-t border-slate-100 pt-3 text-xs">
          <p class="text-[11px] font-bold text-slate-700">Key Remarks</p>
          <p class="mt-1 text-slate-500 leading-relaxed">
            {{ partner.latestEvaluation.remarks }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
