<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import type { ProjectDetailItem } from '../../types/types'

import PortofolioHeroCarousel from './PortofolioHeroCarousel.vue'
import PortofolioProjectOverview from './PortofolioProjectOverview.vue'
import PortofolioBackgroundChallanges from './PortofolioBackgroundChallanges.vue'
import PortofolioImplementedSolution from './PortofolioImplementedSolution.vue'
import PortofolioSuccessMetrics from './PortofolioSuccessMetrics.vue'
import PortofolioMediaGallery from './PortofolioMediaGallery.vue'
import PortofolioCaseStudyDownload from './PortofolioCaseStudyDownload.vue'

import ProjectStatusCard from './ProjectStatusCard.vue'
import ProjectTechStackCard from './ProjectTechStackCard.vue'
import ProjectLocationCard from './ProjectLocationCard.vue'
import ProjectDocumentCard from './ProjectDocumentCard.vue'
import ProjectPartnersCard from './ProjectPartnersCard.vue'

const route = useRoute()
const projectId = route.params.id || '1'

// Mock Data Detail Proyek sesuai gambar referensi
const project = ref<ProjectDetailItem>({
  id: String(projectId),
  title: 'Digital Banking Transformation',
  client: 'PT ABC Bank',
  period: 'Jan 2024 – Dec 2024 (12 months)',
  projectValue: 'Confidential',
  location: 'Jakarta, Indonesia',
  teamSize: '12 members',
  lastUpdated: '2 days ago',
  updatedAt: '2 days ago',
  status: 'Completed',
  industry: 'Banking',
  technologies: ['Vue.js', 'Node.js', 'PostgreSQL', 'AWS'],
  serviceType: 'System Development',
  projectType: 'Digital Transformation',
  description: 'End-to-end digital banking platform for improved customer experience.',
  image:
    'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=800&auto=format&fit=crop',
  heroImages: [
    'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1551836022-d5d88e9218df?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1556742049-0a67c5574f73?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=1200&auto=format&fit=crop'
  ],
  overview:
    'Digital Banking Transformation is an end-to-end platform designed to modernize PT ABC Bank’s digital services. The project focused on building a secure, scalable, and user-friendly banking platform to enhance customer experience and operational efficiency.',
  background:
    'PT ABC Bank needed to modernize their legacy banking system to meet increasing customer expectations for digital services and to remain competitive in the financial industry.',
  challenges: [
    'Legacy system with limited scalability',
    'High maintenance cost',
    'Lack of seamless digital customer experience',
    'Integration with multiple internal systems',
    'Need for strict compliance and security requirements'
  ],
  solutions: [
    'Modern web and mobile banking platform',
    'Integration with core banking system and third-party services',
    'Enhanced security with multi-factor authentication',
    'Scalable cloud infrastructure using AWS',
    'User-centric design based on customer research and feedback'
  ],
  metrics: [
    { label: 'Increase in Digital Users', value: '+60%', sublabel: '' },
    { label: 'Reduction in Operational Cost', value: '-40%', sublabel: '' },
    { label: 'Faster Transaction Processing', value: '+35%', sublabel: '' },
    { label: 'Customer Satisfaction Rate', value: '95%', sublabel: '' }
  ],
  mediaGallery: [
    {
      type: 'image',
      url: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=600&auto=format&fit=crop',
      title: 'Building Exterior'
    },
    {
      type: 'image',
      url: 'https://images.unsplash.com/photo-1556742049-0a67c5574f73?q=80&w=600&auto=format&fit=crop',
      title: 'Mobile Banking App'
    },
    {
      type: 'image',
      url: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=600&auto=format&fit=crop',
      title: 'Dashboard Platform'
    },
    {
      type: 'image',
      url: 'https://images.unsplash.com/photo-1551836022-d5d88e9218df?q=80&w=600&auto=format&fit=crop',
      title: 'Team Collaboration'
    },
    {
      type: 'video',
      url: 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?q=80&w=600&auto=format&fit=crop',
      title: 'Product Walkthrough'
    }
  ],
  documents: [
    { name: 'Project Proposal.pdf', size: '2.4 MB', date: '12 Jan 2024' },
    { name: 'Technical Architecture.pdf', size: '3.1 MB', date: '20 Feb 2024' },
    { name: 'UAT Report.pdf', size: '1.8 MB', date: '10 Nov 2024' },
    { name: 'Handover Document.pdf', size: '2.6 MB', date: '15 Dec 2024' }
  ],
  partners: [
    {
      name: 'PT Fintech Solution',
      role: 'Technology Partner',
      tag: 'Core System Development'
    },
    {
      name: 'PT Cloud Indonesia',
      role: 'Infrastructure Partner',
      tag: 'Cloud Services'
    },
    {
      name: 'PT SecureTech',
      role: 'Security Partner',
      tag: 'Security Implementation'
    },
    {
      name: 'PT Consultindo',
      role: 'Consulting Partner',
      tag: 'Business Process Consulting'
    }
  ]
})

const handleEditProject = () => {
  alert(`Buka Modal Edit untuk: ${project.value.title}`)
}
</script>

<template>
  <div class="space-y-6 pb-12">
    <!-- 1. Top Action Bar & Breadcrumbs -->
    <div
      class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between border-b border-slate-200 pb-4"
    >
      <!-- Breadcrumb Navigasi Kiri -->
      <nav class="flex items-center gap-2 text-xs font-medium text-slate-500">
        <NuxtLink to="/portofolio" class="hover:text-blue-600 transition-colors">
          Portfolio
        </NuxtLink>
        <UIcon name="i-lucide-chevron-right" class="h-3.5 w-3.5 text-slate-400" />
        <NuxtLink to="/portofolio" class="hover:text-blue-600 transition-colors">
          Portfolio Directory
        </NuxtLink>
        <UIcon name="i-lucide-chevron-right" class="h-3.5 w-3.5 text-slate-400" />
        <span class="font-semibold text-slate-800 truncate max-w-[200px] sm:max-w-xs">
          {{ project.title }}
        </span>
      </nav>

      <!-- Tombol Aksi Kanan -->
      <div class="flex items-center gap-2.5">
        <NuxtLink
          to="/portofolio"
          class="inline-flex items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700 shadow-2xs transition-colors hover:bg-slate-50 cursor-pointer"
        >
          <UIcon name="i-lucide-arrow-left" class="h-3.5 w-3.5" />
          <span>Back to Portfolio Directory</span>
        </NuxtLink>

        <button
          type="button"
          class="inline-flex items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700 shadow-2xs transition-colors hover:bg-slate-50 cursor-pointer"
          @click="handleEditProject"
        >
          <UIcon name="i-lucide-edit" class="h-3.5 w-3.5 text-slate-500" />
          <span>Edit Project</span>
        </button>

        <button
          type="button"
          class="inline-flex h-7.5 w-7.5 items-center justify-center rounded-lg border border-slate-200 bg-white text-slate-500 shadow-2xs transition-colors hover:bg-slate-50 cursor-pointer"
          aria-label="More actions"
        >
          <UIcon name="i-lucide-more-vertical" class="h-4 w-4" />
        </button>
      </div>
    </div>

    <!-- 2. Main 2-Column Asymmetric Grid -->
    <div class="grid grid-cols-1 gap-6 lg:grid-cols-12 items-start">
      <!-- Left Column (Main Content - 8 Kolom) -->
      <div class="space-y-6 lg:col-span-8">
        <!-- Hero Carousel & Title Section -->
        <PortofolioHeroCarousel
          :title="project.title"
          :subtitle="project.description"
          :status="project.status"
          :images="project.heroImages"
          :tags="[project.industry, ...project.technologies, 'Enterprise']"
        />

        <!-- Project Overview -->
        <PortofolioProjectOverview :overview-text="project.overview" />

        <!-- Background & Challenges (2-Col Comparison) -->
        <PortofolioBackgroundChallanges
          :background="project.background"
          :challenges="project.challenges"
        />

        <!-- Implemented Solution -->
        <PortofolioImplementedSolution :solutions="project.solutions" />

        <!-- Success Metrics & Impact (4 Highlight Cards) -->
        <PortofolioSuccessMetrics :metrics="project.metrics" />

        <!-- Media Gallery (Tabs + 5 Thumbnails) -->
        <PortofolioMediaGallery :media="project.mediaGallery" />

        <!-- Case Study Download Banner -->
        <PortofolioCaseStudyDownload :title="project.title" />
      </div>

      <!-- Right Column (Metadata Sidebar - 4 Kolom) -->
      <div class="space-y-6 lg:col-span-4">
        <!-- Project Status Card -->
        <ProjectStatusCard
          :status="project.status"
          :client="project.client"
          :period="project.period"
          :project-value="project.projectValue"
          :location="project.location"
          :team-size="project.teamSize"
          :last-updated="project.updatedAt"
        />

        <!-- Industry & Technology Card -->
        <ProjectTechStackCard
          :industry="project.industry"
          :technologies="project.technologies"
          :service-type="project.serviceType"
          :project-type="project.projectType"
        />

        <!-- Project Location Card -->
        <ProjectLocationCard :location-name="project.location" />

        <!-- Internal Documentation Card -->
        <ProjectDocumentCard :documents="project.documents" />

        <!-- Related Partners Card (Project-Partner Mapping) -->
        <ProjectPartnersCard :partners="project.partners" />
      </div>
    </div>
  </div>
</template>
