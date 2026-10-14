<script setup lang="ts">
import EngineeringHeader from './EngineeringHeader.vue'
import TechnicalProjectMetrics from './TechnicalProjectMetrics.vue'
import PortfolioExecutionStatus from './PortfolioExecutionStatus.vue'
import PortfolioCategoryOverview from './PortfolioCategoryOverview.vue'
import InternalResourceUtilization from './InternalResourceUtilization.vue'
import FeaturedPortfolioSection from './FeaturedPortfolioSection.vue'
</script>

<template>
  <div class="space-y-4">
    <!-- 1. Header Area (Title, Subtitle, Date Range) -->
    <EngineeringHeader />

    <!-- 2. Technical Project Metrics (4 KPI Cards) -->
    <TechnicalProjectMetrics />

    <!-- 3. Middle Section: 2 Charts Grid (Donut & Horizontal Bar) -->
    <div class="grid grid-cols-1 gap-3.5 lg:grid-cols-2">
      <PortfolioExecutionStatus />
      <PortfolioCategoryOverview />
    </div>

    <!-- 4. Internal Resource Utilization (4 Teams: Frontend, Backend, QA, DevOps) -->
    <InternalResourceUtilization />

    <!-- 5. Featured Portfolio (4 Quick Project Cards with Clickable Navigation) -->
    <FeaturedPortfolioSection />
  </div>
</template>
