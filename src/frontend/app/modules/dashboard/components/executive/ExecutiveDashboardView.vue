<script setup lang="ts">
import DashboardKpiCard from '../shared/DashboardKpiCard.vue'
import BusinessPerformanceTrendCard from './BusinessPerformanceTrendCard.vue'
import PortfolioStatusCard from './PortfolioStatusCard.vue'
import RevenuePipelineCard from './RevenuePipelineCard.vue'
import RoiByCategoryCard from './RoiByCategoryCard.vue'
import TopCategoriesCard from './TopCategoriesCard.vue'
import FeaturedPortfolioCard from './FeaturedPortfolioCard.vue'

import {
  activeProjectsTotal,
  averageRoi,
  executiveKpis,
  featuredProjects,
  openPipelineValue,
  portfolioStatus,
  revenuePipeline,
  topCategories
} from '../../data/executive.data'

const { visibleTrend } = useDashboardRange()
</script>

<template>
  <div class="flex flex-col gap-2">
    <!-- KPI Cards -->
    <div class="grid shrink-0 grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-4">
      <DashboardKpiCard
        v-for="kpi in executiveKpis"
        :key="kpi.label"
        v-bind="kpi"
      />
    </div>

    <!-- Performance Trend + Portfolio Status -->
    <div class="grid shrink-0 grid-cols-1 gap-2 lg:grid-cols-3">
      <BusinessPerformanceTrendCard
        :points="visibleTrend"
        class="lg:col-span-2"
      />
      <PortfolioStatusCard :slices="portfolioStatus" />
    </div>

    <!-- Revenue Pipeline + ROI by Category + Top Categories -->
    <div class="grid shrink-0 grid-cols-1 gap-2 md:grid-cols-2 lg:grid-cols-3">
      <RevenuePipelineCard
        :stages="revenuePipeline"
        :open-value="openPipelineValue"
      />
      <RoiByCategoryCard
        :categories="topCategories"
        :average="averageRoi"
      />
      <TopCategoriesCard
        :categories="topCategories"
        :total="activeProjectsTotal"
        class="md:col-span-2 lg:col-span-1"
      />
    </div>

    <!-- Featured Portfolio -->
    <FeaturedPortfolioCard
      :projects="featuredProjects"
      class="shrink-0"
    />
  </div>
</template>
