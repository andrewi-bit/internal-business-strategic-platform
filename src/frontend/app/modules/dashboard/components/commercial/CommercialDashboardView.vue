<script setup lang="ts">
import DashboardKpiCard from '../shared/DashboardKpiCard.vue'
import SalesPipelineCard from './SalesPipelineCard.vue'
import PartnershipStatusCard from './PartnershipStatusCard.vue'
import ConversionRateTrendCard from './ConversionRateTrendCard.vue'
import FeaturedPartnershipCard from './FeaturedPartnershipCard.vue'

import {
  commercialKpis,
  conversionTarget,
  conversionTrend,
  featuredPartnerships,
  openSalesValue,
  partnershipStatus,
  salesPipeline
} from '../../data/commercial.data'

const selectedPeriod = ref('Jan 2026 – Dec 2026')
</script>

<template>
  <div class="flex flex-col gap-2">
    <!-- Header -->
    <div class="flex shrink-0 flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
      <div class="min-w-0">
        <h1 class="text-xl leading-7 font-bold tracking-tight text-slate-900">
          Commercial Dashboard
        </h1>
        <p class="mt-0.5 truncate text-xs leading-4 text-slate-500">
          Sales pipeline, partnership prospects, and revenue conversion performance.
        </p>
      </div>

      <div
        class="inline-flex shrink-0 items-center gap-2 rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700 shadow-xs"
      >
        <UIcon
          name="i-lucide-calendar"
          class="h-4 w-4 text-slate-500"
        />
        <span>{{ selectedPeriod }}</span>
      </div>
    </div>

    <!-- KPI Cards -->
    <div class="grid shrink-0 grid-cols-1 gap-2 sm:grid-cols-3">
      <DashboardKpiCard
        v-for="kpi in commercialKpis"
        :key="kpi.label"
        v-bind="kpi"
      />
    </div>

    <!-- Sales Pipeline + Partnership Prospect Status -->
    <div class="grid shrink-0 grid-cols-1 gap-2 lg:grid-cols-3">
      <SalesPipelineCard
        :stages="salesPipeline"
        :open-value="openSalesValue"
        class="lg:col-span-2"
      />
      <PartnershipStatusCard :slices="partnershipStatus" />
    </div>

    <!-- Conversion Rate Trend -->
    <ConversionRateTrendCard
      :points="conversionTrend"
      :target="conversionTarget"
      class="shrink-0"
    />

    <!-- Featured Partnerships -->
    <FeaturedPartnershipCard
      :partnerships="featuredPartnerships"
      class="shrink-0"
    />
  </div>
</template>
