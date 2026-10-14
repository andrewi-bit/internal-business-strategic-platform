<script setup lang="ts">
import { ref, computed } from 'vue'
import type { ProjectItem, ViewMode, PortfolioFilterState } from '../../types/types.ts'

import PortofolioHeader from './PortofolioHeader.vue'
import PortofolioFilter from './PortofolioFilter.vue'
import PortofolioToolbar from './PortofolioToolbar.vue'
import PortofolioGrid from './PortofolioGrid.vue'
import PortofolioTable from './PortofolioTable.vue'
import PortofolioPagination from './PortofolioPagination.vue'

// State Interaktif
const viewMode = ref<ViewMode>('grid')
const sortBy = ref<string>('latest')
const currentPage = ref<number>(1)
const pageSize = 12
const totalProjectsCount = 128

// State Filter
const activeFilters = ref<PortfolioFilterState>({
  search: '',
  industry: '',
  technology: '',
  year: '',
  status: ''
})

// 12 Mock Data Portofolio
const dummyProjects = ref<ProjectItem[]>([
  {
    id: '1',
    title: 'Digital Banking Transformation',
    client: 'ABC Bank',
    description: 'End-to-end digital banking platform for improved customer experience.',
    industry: 'Banking',
    technologies: ['Web', 'Fintech'],
    status: 'Completed',
    image:
      'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=600&auto=format&fit=crop',
    updatedAt: '2 days ago'
  },
  {
    id: '2',
    title: 'Smart Manufacturing Platform',
    client: 'PT. Manufaktur Indonesia',
    description: 'IoT-based manufacturing monitoring and predictive maintenance platform.',
    industry: 'Manufacturing',
    technologies: ['IoT', 'Analytics'],
    status: 'Active',
    image:
      'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?q=80&w=600&auto=format&fit=crop',
    updatedAt: '5 days ago'
  },
  {
    id: '3',
    title: 'Retail Analytics Platform',
    client: 'Retail Group',
    description: 'Analytics platform for retail business intelligence and sales optimization.',
    industry: 'Retail',
    technologies: ['Data Analytics', 'BI'],
    status: 'On Going',
    image:
      'https://images.unsplash.com/photo-1555421689-491a97ff2040?q=80&w=600&auto=format&fit=crop',
    updatedAt: '1 week ago'
  },
  {
    id: '4',
    title: 'Healthcare Management System',
    client: 'MediCare Hospital',
    description: 'Patient management and resource allocation system for healthcare providers.',
    industry: 'Healthcare',
    technologies: ['IoT', 'Mobile', 'SaaS'],
    status: 'Completed',
    image:
      'https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?q=80&w=600&auto=format&fit=crop',
    updatedAt: '2 weeks ago'
  },
  {
    id: '5',
    title: 'Logistics Tracking Platform',
    client: 'LogiTrans Indonesia',
    description: 'Real-time shipment tracking and supply chain visibility platform.',
    industry: 'Logistics',
    technologies: ['Tracking', 'Cloud'],
    status: 'Active',
    image:
      'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?q=80&w=600&auto=format&fit=crop',
    updatedAt: '2 weeks ago'
  },
  {
    id: '6',
    title: 'Government Service Portal',
    client: 'Kementerian Dalam Negeri',
    description: 'Digital service portal for government administration and citizen engagement.',
    industry: 'Government',
    technologies: ['Web', 'Citizen'],
    status: 'On Going',
    image:
      'https://images.unsplash.com/photo-1541872703-74c5e44368f9?q=80&w=600&auto=format&fit=crop',
    updatedAt: '3 weeks ago'
  },
  {
    id: '7',
    title: 'Internal ERP System',
    client: 'Internal Use',
    description: 'Integrated enterprise resource planning system for internal operations.',
    industry: 'Enterprise',
    technologies: ['ERP', 'Management'],
    status: 'Planned',
    image:
      'https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=600&auto=format&fit=crop',
    updatedAt: '1 month ago'
  },
  {
    id: '8',
    title: 'Renewable Energy Dashboard',
    client: 'Green Energy Corp',
    description: 'Monitoring and analytics platform for renewable energy assets.',
    industry: 'Energy',
    technologies: ['Sustainability', 'Dashboard'],
    status: 'Active',
    image:
      'https://images.unsplash.com/photo-1466611653911-95081537e5b7?q=80&w=600&auto=format&fit=crop',
    updatedAt: '1 month ago'
  },
  {
    id: '9',
    title: 'Property Management System',
    client: 'Properti Sejahtera',
    description: 'Property asset management and tenant service platform.',
    industry: 'Property',
    technologies: ['Management', 'Web'],
    status: 'Completed',
    image:
      'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=600&auto=format&fit=crop',
    updatedAt: '1 month ago'
  },
  {
    id: '10',
    title: 'Education Learning Platform',
    client: 'EduTech Indonesia',
    description: 'Online learning platform with interactive content and assessment.',
    industry: 'Education',
    technologies: ['E-Learning', 'Mobile'],
    status: 'Active',
    image:
      'https://images.unsplash.com/photo-1509062522246-3755977927d7?q=80&w=600&auto=format&fit=crop',
    updatedAt: '1 month ago'
  },
  {
    id: '11',
    title: 'Inventory Management System',
    client: 'Supply Chain Co.',
    description: 'Inventory tracking and warehouse operations solution.',
    industry: 'Inventory',
    technologies: ['Warehouse', 'ERP'],
    status: 'On Going',
    image:
      'https://images.unsplash.com/photo-1553413077-190dd305871c?q=80&w=600&auto=format&fit=crop',
    updatedAt: '1 month ago'
  },
  {
    id: '12',
    title: 'Legacy System Migration',
    client: 'Internal Use',
    description: 'Migration of legacy systems to modern cloud infrastructure.',
    industry: 'Migration',
    technologies: ['Infrastructure', 'Cloud'],
    status: 'Cancelled',
    image:
      'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?q=80&w=600&auto=format&fit=crop',
    updatedAt: '2 months ago'
  }
])

// Komputasi filter pencarian interaktif
const filteredProjects = computed(() => {
  return dummyProjects.value.filter((project) => {
    const matchSearch =
      !activeFilters.value.search ||
      project.title.toLowerCase().includes(activeFilters.value.search.toLowerCase()) ||
      project.client.toLowerCase().includes(activeFilters.value.search.toLowerCase()) ||
      project.description.toLowerCase().includes(activeFilters.value.search.toLowerCase())

    const matchIndustry =
      !activeFilters.value.industry || project.industry === activeFilters.value.industry

    const matchTech =
      !activeFilters.value.technology ||
      project.technologies.includes(activeFilters.value.technology)

    const matchStatus = !activeFilters.value.status || project.status === activeFilters.value.status

    return matchSearch && matchIndustry && matchTech && matchStatus
  })
})

// Event Handlers
const handleFilterChange = (newFilters: PortfolioFilterState) => {
  activeFilters.value = newFilters
}

const handleResetFilter = () => {
  activeFilters.value = {
    search: '',
    industry: '',
    technology: '',
    year: '',
    status: ''
  }
}

const handleAddProject = () => {
  alert('Modal / Page Add Project akan dibuka!')
}

// Di dalam <script setup> PortofolioView.vue:
const handleViewDetail = (project: ProjectItem) => {
  // Langsung arahkan ke URL /portofolio/1, /portofolio/2, dst
  navigateTo(`/portofolio/${project.id}`)
}
</script>

<template>
  <div class="space-y-6">
    <!-- 1. Header Area (Title & Add Button) -->
    <PortofolioHeader @add-project="handleAddProject" />

    <!-- 2. Search & Filters Bar -->
    <PortofolioFilter @filter-change="handleFilterChange" @reset="handleResetFilter" />

    <!-- 3. Toolbar (Counter, Grid/Table Toggle, Sort By) -->
    <PortofolioToolbar
      v-model:current-view="viewMode"
      v-model:sort-by="sortBy"
      :total-count="totalProjectsCount"
    />

    <!-- 4. Dynamic Content Area (Grid vs Table) -->
    <div class="transition-all duration-200">
      <!-- Grid View -->
      <PortofolioGrid
        v-if="viewMode === 'grid'"
        :projects="filteredProjects"
        @view-detail="handleViewDetail"
      />

      <!-- Table View -->
      <PortofolioTable v-else :projects="filteredProjects" @view-detail="handleViewDetail" />
    </div>

    <!-- 5. Bottom Pagination -->
    <div class="pt-4">
      <PortofolioPagination
        v-model:current-page="currentPage"
        :total-items="totalProjectsCount"
        :page-size="pageSize"
      />
    </div>
  </div>
</template>
