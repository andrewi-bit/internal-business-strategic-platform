<script setup lang="ts">
import { computed, ref, watch } from 'vue'

interface SummaryCard {
  label: string
  value: number
  description: string
  icon: string
  iconClass: string
}

interface ProjectCollaboration {
  id: string
  name: string
  code: string
  description: string
  contribution: string
  startDate: string
  endDate: string
  status: 'Completed' | 'Ongoing'
  year: string
}

interface HistoryActivity {
  id: string
  name: string
  type: 'Enablement' | 'Co-Marketing'
  description: string
  date: string
  status: 'Completed' | 'Ongoing'
  year: string
}

interface RowMenuItem {
  label: string
  icon: string
  color?: 'error'
  onSelect: () => void
}

// 1. Summary Cards
const summaryCards: SummaryCard[] = [
  {
    label: 'Total Collaborations',
    value: 12,
    description: 'All recorded joint activities',
    icon: 'i-lucide-handshake',
    iconClass: 'bg-blue-50 text-blue-600'
  },
  {
    label: 'Related Projects',
    value: 5,
    description: 'Joint projects with this partner',
    icon: 'i-lucide-briefcase',
    iconClass: 'bg-purple-50 text-purple-600'
  },
  {
    label: 'Enablement Activities',
    value: 4,
    description: 'Training & capability building',
    icon: 'i-lucide-graduation-cap',
    iconClass: 'bg-emerald-50 text-emerald-600'
  },
  {
    label: 'Co-Marketing Activities',
    value: 3,
    description: 'Joint marketing initiatives',
    icon: 'i-lucide-megaphone',
    iconClass: 'bg-amber-50 text-amber-600'
  }
]

// 2. Project Collaboration History Data (Dummy Lokal)
const projects: ProjectCollaboration[] = [
  {
    id: 'PRJ-2026-001',
    name: 'Cloud Infrastructure Migration',
    code: 'PRJ-2026-001',
    description: 'Migrate on-premise workloads to Google Cloud infrastructure.',
    contribution: 'Cloud Infrastructure',
    startDate: 'Jan 15, 2026',
    endDate: 'Dec 31, 2026',
    status: 'Ongoing',
    year: '2026'
  },
  {
    id: 'PRJ-2025-008',
    name: 'Data Analytics Platform',
    code: 'PRJ-2025-008',
    description: 'Build a unified data analytics and BI platform on BigQuery.',
    contribution: 'Data Analytics',
    startDate: 'Mar 1, 2025',
    endDate: 'Nov 30, 2025',
    status: 'Completed',
    year: '2025'
  },
  {
    id: 'PRJ-2025-014',
    name: 'Security Assessment',
    code: 'PRJ-2025-014',
    description: 'Security audit and hardening of cloud workloads.',
    contribution: 'Security Audit',
    startDate: 'Jun 10, 2025',
    endDate: 'Aug 20, 2025',
    status: 'Completed',
    year: '2025'
  },
  {
    id: 'PRJ-2024-012',
    name: 'Industry Solution Development',
    code: 'PRJ-2024-012',
    description: 'Co-develop an industry-specific cloud solution blueprint.',
    contribution: 'Solution Co-Development',
    startDate: 'May 10, 2024',
    endDate: 'Dec 20, 2024',
    status: 'Completed',
    year: '2024'
  },
  {
    id: 'PRJ-2024-006',
    name: 'Developer Workshop',
    code: 'PRJ-2024-006',
    description: 'Hands-on cloud development workshop for engineering teams.',
    contribution: 'Training & Enablement',
    startDate: 'Feb 5, 2024',
    endDate: 'Apr 15, 2024',
    status: 'Completed',
    year: '2024'
  }
]

// 3. Enablement & Co-Marketing History Data (Dummy Lokal)
const activities: HistoryActivity[] = [
  {
    id: 'ENB-2026-004',
    name: 'Google Cloud Fundamentals Training',
    type: 'Enablement',
    description: 'Technical training for the internal engineering team on GCP core services.',
    date: 'Mar 12, 2026',
    status: 'Completed',
    year: '2026'
  },
  {
    id: 'ENB-2025-011',
    name: 'Security Best Practices Workshop',
    type: 'Enablement',
    description: 'Hands-on workshop on IAM, VPC controls, and cloud threat detection.',
    date: 'Aug 5, 2025',
    status: 'Completed',
    year: '2025'
  },
  {
    id: 'ENB-2024-007',
    name: 'AI/ML Enablement Bootcamp',
    type: 'Enablement',
    description: 'Intensive program on Vertex AI and generative AI solutions.',
    date: 'Nov 18, 2024',
    status: 'Completed',
    year: '2024'
  },
  {
    id: 'ENB-2024-003',
    name: 'Partner Certification Program',
    type: 'Enablement',
    description: 'Certification track for partner solution architects and engineers.',
    date: 'Jun 22, 2024',
    status: 'Ongoing',
    year: '2024'
  },
  {
    id: 'CMK-2026-002',
    name: 'Google Cloud Summit Jakarta',
    type: 'Co-Marketing',
    description: 'Joint showcase of cloud solutions at the regional summit.',
    date: 'May 20, 2026',
    status: 'Completed',
    year: '2026'
  },
  {
    id: 'CMK-2025-005',
    name: 'Cloud Transformation Webinar',
    type: 'Co-Marketing',
    description: 'Co-hosted webinar on cloud migration best practices.',
    date: 'Feb 14, 2025',
    status: 'Completed',
    year: '2025'
  },
  {
    id: 'CMK-2024-001',
    name: 'Joint Customer Success Story',
    type: 'Co-Marketing',
    description: 'Published a joint case study highlighting customer outcomes.',
    date: 'Sep 30, 2024',
    status: 'Completed',
    year: '2024'
  }
]

// 4. Filter State
const projectSearch = ref('')
const projectStatus = ref('')
const projectYear = ref('')

const activitySearch = ref('')
const activityType = ref('')
const activityYear = ref('')

const projectYears = computed(() =>
  [...new Set(projects.map(project => project.year))].sort((a, b) => b.localeCompare(a))
)

const activityYears = computed(() =>
  [...new Set(activities.map(activity => activity.year))].sort((a, b) => b.localeCompare(a))
)

// 5. Filtered Data
const filteredProjects = computed(() =>
  projects.filter((project) => {
    const keyword = projectSearch.value.toLowerCase()
    const matchSearch
      = !keyword
        || project.name.toLowerCase().includes(keyword)
        || project.description.toLowerCase().includes(keyword)
    const matchStatus = !projectStatus.value || project.status === projectStatus.value
    const matchYear = !projectYear.value || project.year === projectYear.value

    return matchSearch && matchStatus && matchYear
  })
)

const filteredActivities = computed(() =>
  activities.filter((activity) => {
    const keyword = activitySearch.value.toLowerCase()
    const matchSearch
      = !keyword
        || activity.name.toLowerCase().includes(keyword)
        || activity.description.toLowerCase().includes(keyword)
    const matchType = !activityType.value || activity.type === activityType.value
    const matchYear = !activityYear.value || activity.year === activityYear.value

    return matchSearch && matchType && matchYear
  })
)

// 6. Pagination
const projectPageSize = 4
const activityPageSize = 4

const projectPage = ref(1)
const activityPage = ref(1)

watch([projectSearch, projectStatus, projectYear], () => {
  projectPage.value = 1
})

watch([activitySearch, activityType, activityYear], () => {
  activityPage.value = 1
})

const totalProjectPages = computed(() =>
  Math.max(1, Math.ceil(filteredProjects.value.length / projectPageSize))
)

const totalActivityPages = computed(() =>
  Math.max(1, Math.ceil(filteredActivities.value.length / activityPageSize))
)

const pagedProjects = computed(() => {
  const start = (projectPage.value - 1) * projectPageSize
  return filteredProjects.value.slice(start, start + projectPageSize)
})

const pagedActivities = computed(() => {
  const start = (activityPage.value - 1) * activityPageSize
  return filteredActivities.value.slice(start, start + activityPageSize)
})

const projectRangeStart = computed(() =>
  filteredProjects.value.length === 0 ? 0 : (projectPage.value - 1) * projectPageSize + 1
)

const projectRangeEnd = computed(() =>
  Math.min(projectPage.value * projectPageSize, filteredProjects.value.length)
)

const activityRangeStart = computed(() =>
  filteredActivities.value.length === 0 ? 0 : (activityPage.value - 1) * activityPageSize + 1
)

const activityRangeEnd = computed(() =>
  Math.min(activityPage.value * activityPageSize, filteredActivities.value.length)
)

// 7. Badge Helpers
const getStatusClass = (status: ProjectCollaboration['status']) =>
  status === 'Completed'
    ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
    : 'bg-blue-50 text-blue-700 border-blue-200'

const getTypeClass = (type: HistoryActivity['type']) =>
  type === 'Enablement'
    ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
    : 'bg-amber-50 text-amber-700 border-amber-200'

// 8. Actions
const handleExport = (label: string) => {
  alert(`Exporting ${label} to CSV / Excel...`)
}

const handleAction = (action: string, name: string) => {
  alert(`${action}: ${name}`)
}

const projectMenuItems = (project: ProjectCollaboration): RowMenuItem[][] => [
  [
    {
      label: 'View Details',
      icon: 'i-lucide-eye',
      onSelect: () => handleAction('View Details', project.name)
    },
    {
      label: 'Edit Project',
      icon: 'i-lucide-pencil',
      onSelect: () => handleAction('Edit Project', project.name)
    }
  ],
  [
    {
      label: 'Delete',
      icon: 'i-lucide-trash-2',
      color: 'error',
      onSelect: () => handleAction('Delete', project.name)
    }
  ]
]

const activityMenuItems = (activity: HistoryActivity): RowMenuItem[][] => [
  [
    {
      label: 'View Details',
      icon: 'i-lucide-eye',
      onSelect: () => handleAction('View Details', activity.name)
    },
    {
      label: 'Edit Activity',
      icon: 'i-lucide-pencil',
      onSelect: () => handleAction('Edit Activity', activity.name)
    }
  ],
  [
    {
      label: 'Delete',
      icon: 'i-lucide-trash-2',
      color: 'error',
      onSelect: () => handleAction('Delete', activity.name)
    }
  ]
]
</script>

<template>
  <div class="flex flex-col gap-3">
    <!-- 1. Summary Cards -->
    <div class="grid shrink-0 grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">
      <div
        v-for="card in summaryCards"
        :key="card.label"
        class="flex items-center gap-3 rounded-xl border border-slate-200/80 bg-white p-3 shadow-2xs"
      >
        <div
          class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg"
          :class="card.iconClass"
        >
          <UIcon
            :name="card.icon"
            class="h-4.5 w-4.5"
          />
        </div>
        <div class="min-w-0">
          <p class="text-[11px] font-semibold tracking-wide text-slate-500 uppercase">
            {{ card.label }}
          </p>
          <p class="mt-1 text-xl leading-none font-bold text-slate-900">
            {{ card.value }}
          </p>
          <p class="mt-1 text-[11px] leading-tight text-slate-400">
            {{ card.description }}
          </p>
        </div>
      </div>
    </div>

    <!-- 2. Project Collaboration History -->
    <div class="rounded-xl border border-slate-200/80 bg-white p-3 shadow-2xs">
      <div
        class="flex flex-col gap-3 border-b border-slate-100 pb-3 lg:flex-row lg:items-center lg:justify-between"
      >
        <div class="min-w-0">
          <h2 class="text-sm font-semibold tracking-tight text-slate-900">
            Project Collaboration History
          </h2>
          <p class="mt-0.5 text-xs text-slate-500">
            All joint projects and initiatives delivered together with this partner.
          </p>
        </div>

        <!-- Controls: Search, Status Filter, Year Filter, Export -->
        <div class="flex flex-wrap items-center gap-2 lg:flex-nowrap">
          <div class="relative w-full min-w-0 sm:w-52 lg:w-64">
            <div
              class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400"
            >
              <UIcon
                name="i-lucide-search"
                class="h-4 w-4"
              />
            </div>
            <input
              v-model="projectSearch"
              type="text"
              placeholder="Search project name or description..."
              class="h-9 w-full rounded-lg border border-slate-200 bg-white pr-3 pl-9 text-xs text-slate-800 placeholder-slate-400 transition-colors focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
            >
          </div>

          <select
            v-model="projectStatus"
            class="h-9 min-w-0 shrink-0 rounded-lg border border-slate-200 bg-white px-2 text-xs font-medium text-slate-700 shadow-2xs focus:border-blue-500 focus:outline-none cursor-pointer"
          >
            <option value="">
              All Status
            </option>
            <option value="Completed">
              Completed
            </option>
            <option value="Ongoing">
              Ongoing
            </option>
          </select>

          <select
            v-model="projectYear"
            class="h-9 min-w-0 shrink-0 rounded-lg border border-slate-200 bg-white px-2 text-xs font-medium text-slate-700 shadow-2xs focus:border-blue-500 focus:outline-none cursor-pointer"
          >
            <option value="">
              All Years
            </option>
            <option
              v-for="year in projectYears"
              :key="year"
              :value="year"
            >
              {{ year }}
            </option>
          </select>

          <button
            type="button"
            class="inline-flex h-9 shrink-0 items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-3 text-xs font-semibold text-slate-700 shadow-2xs hover:bg-slate-50 cursor-pointer"
            @click="handleExport('Project Collaboration History')"
          >
            <UIcon
              name="i-lucide-download"
              class="h-4 w-4 text-slate-500"
            />
            <span>Export</span>
            <UIcon
              name="i-lucide-chevron-down"
              class="h-3 w-3 text-slate-400"
            />
          </button>
        </div>
      </div>

      <div class="mt-3 min-w-0 overflow-x-auto">
        <table class="w-full table-fixed text-left text-xs">
          <thead class="border-b border-slate-100 text-[11px] font-semibold tracking-wide text-slate-500">
            <tr>
              <th class="w-[34%] px-1.5 py-2">
                Project / Initiative
              </th>
              <th class="w-[20%] px-1.5 py-2">
                Partner Contribution
              </th>
              <th class="w-[13%] px-1.5 py-2">
                Start Date
              </th>
              <th class="w-[13%] px-1.5 py-2">
                End Date
              </th>
              <th class="w-[12%] px-1.5 py-2">
                Status
              </th>
              <th class="w-[8%] px-1.5 py-2 text-right">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr
              v-for="project in pagedProjects"
              :key="project.id"
              class="transition-colors hover:bg-slate-50/60"
            >
              <td class="px-1.5 py-1">
                <div class="flex items-center gap-2.5">
                  <div
                    class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-blue-50 text-blue-600"
                  >
                    <UIcon
                      name="i-lucide-briefcase"
                      class="h-4 w-4"
                    />
                  </div>
                  <div class="min-w-0">
                    <p
                      class="truncate text-xs font-semibold text-slate-800"
                      :title="project.name"
                    >
                      {{ project.name }}
                    </p>
                    <p
                      class="truncate text-[11px] text-slate-400"
                      :title="project.description"
                    >
                      {{ project.description }}
                    </p>
                  </div>
                </div>
              </td>

              <td class="px-1.5 py-1 text-slate-600">
                <span class="line-clamp-2">{{ project.contribution }}</span>
              </td>

              <td class="px-1.5 py-1 text-[11px] whitespace-nowrap text-slate-500">
                {{ project.startDate }}
              </td>

              <td class="px-1.5 py-1 text-[11px] whitespace-nowrap text-slate-500">
                {{ project.endDate }}
              </td>

              <td class="px-1.5 py-1 whitespace-nowrap">
                <span
                  class="inline-flex items-center rounded-full border px-2 py-0.5 text-[10px] font-semibold"
                  :class="getStatusClass(project.status)"
                >
                  {{ project.status }}
                </span>
              </td>

              <td class="py-1 pl-1.5 text-right">
                <UDropdownMenu
                  :items="projectMenuItems(project)"
                  :content="{ align: 'end' }"
                >
                  <button
                    type="button"
                    class="inline-flex h-7 w-7 items-center justify-center rounded-md text-slate-400 transition-colors hover:bg-slate-100 hover:text-slate-700 cursor-pointer"
                    aria-label="Project actions"
                  >
                    <UIcon
                      name="i-lucide-ellipsis-vertical"
                      class="h-4 w-4"
                    />
                  </button>
                </UDropdownMenu>
              </td>
            </tr>

            <tr v-if="filteredProjects.length === 0">
              <td
                colspan="6"
                class="px-4 py-6 text-center"
              >
                <div class="flex flex-col items-center gap-1.5">
                  <UIcon
                    name="i-lucide-search-x"
                    class="h-6 w-6 text-slate-300"
                  />
                  <p class="text-xs font-semibold text-slate-600">
                    No projects found
                  </p>
                  <p class="text-[11px] text-slate-400">
                    Try adjusting your search or filters.
                  </p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Project Pagination -->
      <div class="flex shrink-0 items-center justify-between gap-2 border-t border-slate-100 pt-2.5">
        <p class="text-xs text-slate-500">
          Showing
          <span class="font-semibold text-slate-700">{{ projectRangeStart }}</span>
          to
          <span class="font-semibold text-slate-700">{{ projectRangeEnd }}</span>
          of
          <span class="font-semibold text-slate-700">{{ filteredProjects.length }}</span>
        </p>

        <div class="flex items-center gap-1">
          <button
            type="button"
            class="inline-flex h-7 w-7 items-center justify-center rounded-md border border-slate-200 bg-white text-slate-600 transition-colors hover:bg-slate-50 disabled:opacity-40 cursor-pointer"
            :disabled="projectPage <= 1"
            aria-label="Previous page"
            @click="projectPage--"
          >
            <UIcon
              name="i-lucide-chevron-left"
              class="h-3.5 w-3.5"
            />
          </button>

          <button
            v-for="page in totalProjectPages"
            :key="page"
            type="button"
            class="inline-flex h-7 w-7 items-center justify-center rounded-md text-[11px] font-semibold cursor-pointer"
            :class="[
              projectPage === page
                ? 'bg-blue-600 text-white shadow-2xs'
                : 'border border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
            ]"
            @click="projectPage = page"
          >
            {{ page }}
          </button>

          <button
            type="button"
            class="inline-flex h-7 w-7 items-center justify-center rounded-md border border-slate-200 bg-white text-slate-600 transition-colors hover:bg-slate-50 disabled:opacity-40 cursor-pointer"
            :disabled="projectPage >= totalProjectPages"
            aria-label="Next page"
            @click="projectPage++"
          >
            <UIcon
              name="i-lucide-chevron-right"
              class="h-3.5 w-3.5"
            />
          </button>
        </div>
      </div>
    </div>

    <!-- 3. Enablement & Co-Marketing History -->
    <div class="rounded-xl border border-slate-200/80 bg-white p-3 shadow-2xs">
      <div
        class="flex flex-col gap-3 border-b border-slate-100 pb-3 lg:flex-row lg:items-center lg:justify-between"
      >
        <div class="min-w-0">
          <h2 class="text-sm font-semibold tracking-tight text-slate-900">
            Enablement & Co-Marketing History
          </h2>
          <p class="mt-0.5 text-xs text-slate-500">
            Training, enablement programs, and joint marketing activities with this partner.
          </p>
        </div>

        <!-- Controls: Search, Type Filter, Year Filter, Export -->
        <div class="flex flex-wrap items-center gap-2 lg:flex-nowrap">
          <div class="relative w-full min-w-0 sm:w-52 lg:w-64">
            <div
              class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400"
            >
              <UIcon
                name="i-lucide-search"
                class="h-4 w-4"
              />
            </div>
            <input
              v-model="activitySearch"
              type="text"
              placeholder="Search activity name or description..."
              class="h-9 w-full rounded-lg border border-slate-200 bg-white pr-3 pl-9 text-xs text-slate-800 placeholder-slate-400 transition-colors focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
            >
          </div>

          <select
            v-model="activityType"
            class="h-9 min-w-0 shrink-0 rounded-lg border border-slate-200 bg-white px-2 text-xs font-medium text-slate-700 shadow-2xs focus:border-blue-500 focus:outline-none cursor-pointer"
          >
            <option value="">
              All Types
            </option>
            <option value="Enablement">
              Enablement
            </option>
            <option value="Co-Marketing">
              Co-Marketing
            </option>
          </select>

          <select
            v-model="activityYear"
            class="h-9 min-w-0 shrink-0 rounded-lg border border-slate-200 bg-white px-2 text-xs font-medium text-slate-700 shadow-2xs focus:border-blue-500 focus:outline-none cursor-pointer"
          >
            <option value="">
              All Years
            </option>
            <option
              v-for="year in activityYears"
              :key="year"
              :value="year"
            >
              {{ year }}
            </option>
          </select>

          <button
            type="button"
            class="inline-flex h-9 shrink-0 items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-3 text-xs font-semibold text-slate-700 shadow-2xs hover:bg-slate-50 cursor-pointer"
            @click="handleExport('Enablement & Co-Marketing History')"
          >
            <UIcon
              name="i-lucide-download"
              class="h-4 w-4 text-slate-500"
            />
            <span>Export</span>
            <UIcon
              name="i-lucide-chevron-down"
              class="h-3 w-3 text-slate-400"
            />
          </button>
        </div>
      </div>

      <div class="mt-3 min-w-0 overflow-x-auto">
        <table class="w-full table-fixed text-left text-xs">
          <thead class="border-b border-slate-100 text-[11px] font-semibold tracking-wide text-slate-500">
            <tr>
              <th class="w-[22%] px-1.5 py-2">
                Activity Name
              </th>
              <th class="w-[14%] px-1.5 py-2">
                Type
              </th>
              <th class="w-[31%] px-1.5 py-2">
                Description
              </th>
              <th class="w-[12%] px-1.5 py-2">
                Date
              </th>
              <th class="w-[14%] px-1.5 py-2">
                Status
              </th>
              <th class="w-[7%] px-1.5 py-2 text-right">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr
              v-for="activity in pagedActivities"
              :key="activity.id"
              class="transition-colors hover:bg-slate-50/60"
            >
              <td class="px-1.5 py-1">
                <div class="flex items-center gap-2.5">
                  <div
                    class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg"
                    :class="
                      activity.type === 'Enablement'
                        ? 'bg-emerald-50 text-emerald-600'
                        : 'bg-amber-50 text-amber-600'
                    "
                  >
                    <UIcon
                      :name="
                        activity.type === 'Enablement'
                          ? 'i-lucide-graduation-cap'
                          : 'i-lucide-megaphone'
                      "
                      class="h-4 w-4"
                    />
                  </div>
                  <span
                    class="min-w-0 truncate text-xs font-semibold text-slate-800"
                    :title="activity.name"
                  >
                    {{ activity.name }}
                  </span>
                </div>
              </td>

              <td class="px-1.5 py-1 whitespace-nowrap">
                <span
                  class="inline-flex items-center rounded-md border px-1.5 py-0.5 text-[10px] font-semibold"
                  :class="getTypeClass(activity.type)"
                >
                  {{ activity.type }}
                </span>
              </td>

              <td class="px-1.5 py-1 text-slate-600">
                <span class="line-clamp-2">{{ activity.description }}</span>
              </td>

              <td class="px-1.5 py-1 text-[11px] whitespace-nowrap text-slate-500">
                {{ activity.date }}
              </td>

              <td class="px-1.5 py-1 whitespace-nowrap">
                <span
                  class="inline-flex items-center rounded-full border px-2 py-0.5 text-[10px] font-semibold"
                  :class="getStatusClass(activity.status)"
                >
                  {{ activity.status }}
                </span>
              </td>

              <td class="py-1 pl-1.5 text-right">
                <UDropdownMenu
                  :items="activityMenuItems(activity)"
                  :content="{ align: 'end' }"
                >
                  <button
                    type="button"
                    class="inline-flex h-7 w-7 items-center justify-center rounded-md text-slate-400 transition-colors hover:bg-slate-100 hover:text-slate-700 cursor-pointer"
                    aria-label="Activity actions"
                  >
                    <UIcon
                      name="i-lucide-ellipsis-vertical"
                      class="h-4 w-4"
                    />
                  </button>
                </UDropdownMenu>
              </td>
            </tr>

            <tr v-if="filteredActivities.length === 0">
              <td
                colspan="6"
                class="px-4 py-6 text-center"
              >
                <div class="flex flex-col items-center gap-1.5">
                  <UIcon
                    name="i-lucide-search-x"
                    class="h-6 w-6 text-slate-300"
                  />
                  <p class="text-xs font-semibold text-slate-600">
                    No activities found
                  </p>
                  <p class="text-[11px] text-slate-400">
                    Try adjusting your search or filters.
                  </p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Activity Pagination -->
      <div class="flex shrink-0 items-center justify-between gap-2 border-t border-slate-100 pt-2.5">
        <p class="text-xs text-slate-500">
          Showing
          <span class="font-semibold text-slate-700">{{ activityRangeStart }}</span>
          to
          <span class="font-semibold text-slate-700">{{ activityRangeEnd }}</span>
          of
          <span class="font-semibold text-slate-700">{{ filteredActivities.length }}</span>
        </p>

        <div class="flex items-center gap-1">
          <button
            type="button"
            class="inline-flex h-7 w-7 items-center justify-center rounded-md border border-slate-200 bg-white text-slate-600 transition-colors hover:bg-slate-50 disabled:opacity-40 cursor-pointer"
            :disabled="activityPage <= 1"
            aria-label="Previous page"
            @click="activityPage--"
          >
            <UIcon
              name="i-lucide-chevron-left"
              class="h-3.5 w-3.5"
            />
          </button>

          <button
            v-for="page in totalActivityPages"
            :key="page"
            type="button"
            class="inline-flex h-7 w-7 items-center justify-center rounded-md text-[11px] font-semibold cursor-pointer"
            :class="[
              activityPage === page
                ? 'bg-blue-600 text-white shadow-2xs'
                : 'border border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
            ]"
            @click="activityPage = page"
          >
            {{ page }}
          </button>

          <button
            type="button"
            class="inline-flex h-7 w-7 items-center justify-center rounded-md border border-slate-200 bg-white text-slate-600 transition-colors hover:bg-slate-50 disabled:opacity-40 cursor-pointer"
            :disabled="activityPage >= totalActivityPages"
            aria-label="Next page"
            @click="activityPage++"
          >
            <UIcon
              name="i-lucide-chevron-right"
              class="h-3.5 w-3.5"
            />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
