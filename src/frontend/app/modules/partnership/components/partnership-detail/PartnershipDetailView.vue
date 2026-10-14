<script setup lang="ts">
import { ref } from 'vue'
import type { PartnerDetailItem } from '../../types/detail.types'
import type { TabKey } from './PartnershipDetailTabs.vue'

import PartnershipDetailHeader from './PartnershipDetailHeader.vue'
import PartnershipDetailTabs from './PartnershipDetailTabs.vue'

import PartnershipOverviewTab from './tabs/PartnershipOverviewTab.vue'
import PartnershipCompanyProfileTab from './tabs/PartnershipCompanyProfileTab.vue'
import PartnershipDetailsTab from './tabs/PartnershipDetailsTab.vue'
import PartnershipLegalDocumentsTab from './tabs/PartnershipLegalDocumentsTab.vue'
import PartnershipCollaborationHistoryTab from './tabs/PartnershipCollaborationHistoryTab.vue'
import PartnershipEvaluationTab from './tabs/PartnershipEvaluationTab.vue'
import PartnershipRelatedPortofolioTab from './tabs/PartnershipRelatedPortofolioTab.vue'
import PartnershipNotesActivityTab from './tabs/PartnershipNotesActivityTab.vue'

// Tab Aktif (Default: 'overview')
const activeTab = ref<TabKey>('overview')

// 100% Mock Data Lokal Lengkap Google Cloud sesuai Gambar
const partnerData = ref<PartnerDetailItem>({
  id: 'PTN-2026-001',
  code: 'PTN-2026-001',
  name: 'Google Cloud',
  legalName: 'Google LLC',
  logo: 'https://www.gstatic.com/images/branding/product/2x/google_cloud_64dp.png',
  status: 'Active',
  partnershipSince: 'Jan 15, 2024',
  category: 'Technology Partner',
  tags: ['Cloud Platform', 'Data Analytics', 'AI & Machine Learning'],
  contract: {
    status: 'Active',
    validUntil: 'Dec 31, 2027',
    remainingTime: '1 year 2 months'
  },
  companyOverview: {
    website: 'https://cloud.google.com',
    headquarters: '1600 Amphitheatre Parkway, Mountain View, California, 94043, USA',
    industry: 'Cloud & Infrastructure',
    businessFocus: 'Cloud Platform, Data Analytics, AI & Machine Learning, Security',
    keyMarkets: ['Global', 'Asia Pacific', 'North America', 'Europe'],
    description:
      'Google Cloud provides a comprehensive suite of cloud computing services including infrastructure, data analytics, AI/ML, and collaboration tools to help organizations build, scale, and transform their business.'
  },
  keyExpertise: [
    { name: 'Cloud Platform', icon: 'i-lucide-cloud' },
    { name: 'Data Analytics', icon: 'i-lucide-bar-chart-2' },
    { name: 'AI & Machine Learning', icon: 'i-lucide-cpu' },
    { name: 'Security', icon: 'i-lucide-shield-check' },
    { name: 'DevOps', icon: 'i-lucide-settings' }
  ],
  keyContacts: [
    {
      id: '1',
      name: 'John Doe',
      initials: 'JD',
      position: 'Partner Manager',
      email: 'john.doe@google.com',
      phone: '+1 650 253 0000',
      type: 'Primary'
    },
    {
      id: '2',
      name: 'Sarah Lim',
      initials: 'SL',
      position: 'Partnership Lead',
      email: 'sarah.lim@google.com',
      phone: '+1 650 253 0001',
      type: 'Technical'
    },
    {
      id: '3',
      name: 'Michael Chen',
      initials: 'MC',
      position: 'Business Development',
      email: 'michael.chen@google.com',
      phone: '+1 650 253 0002',
      type: 'Commercial'
    }
  ],
  quickInfo: {
    partnerType: 'Strategic Partner',
    hasActiveProject: true,
    activeProjectsCount: 3,
    lastEvaluation: 'Aug 28, 2026',
    nextEvaluation: 'Aug 28, 2027'
  },
  recentCollaborations: [
    {
      id: '1',
      name: 'Smart Manufacturing Platform',
      code: 'PRJ-2026-001',
      contribution: 'Cloud Infrastructure',
      status: 'In Progress',
      startDate: 'Jan 15, 2026',
      endDate: 'Dec 31, 2026'
    },
    {
      id: '2',
      name: 'Data Analytics Modernization',
      code: 'PRJ-2025-008',
      contribution: 'Data Analytics',
      status: 'Completed',
      startDate: 'Mar 1, 2025',
      endDate: 'Nov 30, 2025'
    },
    {
      id: '3',
      name: 'AI Assistant Implementation',
      code: 'PRJ-2024-012',
      contribution: 'AI & Machine Learning',
      status: 'Completed',
      startDate: 'May 10, 2024',
      endDate: 'Dec 20, 2024'
    }
  ],
  latestEvaluation: {
    overallScore: 85,
    ratingLabel: 'Good',
    evaluationDate: 'Aug 28, 2026',
    evaluator: 'Partnership Management Team',
    recommendation: 'Continue Partnership',
    nextEvaluation: 'Aug 28, 2027',
    remarks:
      'Strong technical expertise and good collaboration throughout the project. Delivery quality meets expectations and the partner has shown proactive support.'
  }
})

const handleEditPartner = () => {
  alert(`Edit Partner: ${partnerData.value.name}`)
}
</script>

<template>
  <div class="space-y-3.5">
    <!-- 1. Header Identitas Partner -->
    <PartnershipDetailHeader :partner="partnerData" @edit="handleEditPartner" />

    <!-- 2. Navigasi 8 Tab -->
    <PartnershipDetailTabs v-model:active-tab="activeTab" />

    <!-- 3. Dynamic Tab Content Switching -->
    <div class="transition-all duration-150">
      <PartnershipOverviewTab v-if="activeTab === 'overview'" :partner="partnerData" />

      <PartnershipCompanyProfileTab
        v-else-if="activeTab === 'company-profile'"
        :partner="partnerData"
      />

      <PartnershipDetailsTab v-else-if="activeTab === 'partnership-details'" />

      <PartnershipLegalDocumentsTab v-else-if="activeTab === 'legal-documents'" />

      <PartnershipCollaborationHistoryTab v-else-if="activeTab === 'collaboration-history'" />

      <PartnershipEvaluationTab v-else-if="activeTab === 'evaluation'" />

      <PartnershipRelatedPortofolioTab v-else-if="activeTab === 'related-portfolios'" />

      <PartnershipNotesActivityTab v-else-if="activeTab === 'notes-activities'" />
    </div>
  </div>
</template>
