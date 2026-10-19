<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch, watchEffect } from 'vue'

type DocumentStatus = 'Valid' | 'Expiring Soon' | 'Expired'

type DocumentType = 'Partnership Agreement'
  | 'Non-Disclosure Agreement'
  | 'Data Processing Agreement'
  | 'Business License'
  | 'Tax Document'
  | 'Certification'
  | 'Insurance'
  | 'Policy Document'

type FileType = 'pdf' | 'docx'

interface LegalDocument {
  id: string
  name: string
  fileName: string
  fileType: FileType
  documentType: DocumentType
  version: string
  issueDate: string
  expiryDate: string
  fileAvailable: boolean
}

interface DocumentWithStatus extends LegalDocument {
  status: DocumentStatus
}

interface DocumentTypeMeta {
  type: DocumentType
  icon: string
  toneClass: string
}

interface RowMenuItem {
  label: string
  icon: string
  color?: 'error'
  disabled?: boolean
  onSelect: () => void
}

type NoticeTone = 'info' | 'warning'

interface ActionNotice {
  tone: NoticeTone
  message: string
}

const EXPIRING_SOON_DAYS = 30
const MS_PER_DAY = 86_400_000
const PAGE_SIZE = 8

const today = new Date()
today.setHours(0, 0, 0, 0)

// 1. Mock legal documents (backend belum tersedia)
const documents = ref<LegalDocument[]>([
  {
    id: 'DOC-001',
    name: 'Master Partnership Agreement',
    fileName: 'mpa_google_2024.pdf',
    fileType: 'pdf',
    documentType: 'Partnership Agreement',
    version: 'v2.0',
    issueDate: '2024-01-15',
    expiryDate: '2027-12-31',
    fileAvailable: true
  },
  {
    id: 'DOC-002',
    name: 'NDA Agreement',
    fileName: 'nda_google_2024.pdf',
    fileType: 'pdf',
    documentType: 'Non-Disclosure Agreement',
    version: 'v1.3',
    issueDate: '2024-01-15',
    expiryDate: '2026-12-31',
    fileAvailable: true
  },
  {
    id: 'DOC-003',
    name: 'Data Processing Agreement',
    fileName: 'dpa_google_2024.docx',
    fileType: 'docx',
    documentType: 'Data Processing Agreement',
    version: 'v1.0',
    issueDate: '2024-02-10',
    expiryDate: '2026-02-10',
    fileAvailable: true
  },
  {
    id: 'DOC-004',
    name: 'Business License',
    fileName: 'business_license.pdf',
    fileType: 'pdf',
    documentType: 'Business License',
    version: 'v1.0',
    issueDate: '2024-01-01',
    expiryDate: '2026-12-31',
    fileAvailable: true
  },
  {
    id: 'DOC-005',
    name: 'Tax Registration Certificate',
    fileName: 'tax_certificate.pdf',
    fileType: 'pdf',
    documentType: 'Tax Document',
    version: 'v1.0',
    issueDate: '2024-01-01',
    expiryDate: '2025-12-31',
    fileAvailable: true
  },
  {
    id: 'DOC-006',
    name: 'Compliance Certification',
    fileName: 'compliance_cert.docx',
    fileType: 'docx',
    documentType: 'Certification',
    version: 'v1.2',
    issueDate: '2024-03-01',
    expiryDate: '2026-12-31',
    fileAvailable: true
  },
  {
    id: 'DOC-007',
    name: 'Insurance Certificate',
    fileName: 'insurance_cert.pdf',
    fileType: 'pdf',
    documentType: 'Insurance',
    version: 'v1.0',
    issueDate: '2023-01-01',
    expiryDate: '2024-12-31',
    fileAvailable: false
  },
  {
    id: 'DOC-008',
    name: 'Code of Conduct',
    fileName: 'code_of_conduct.docx',
    fileType: 'docx',
    documentType: 'Policy Document',
    version: 'v1.0',
    issueDate: '2024-01-15',
    expiryDate: '2026-12-31',
    fileAvailable: true
  }
])

// 2. Kategori Document Type (panel kanan)
const documentTypes: DocumentTypeMeta[] = [
  { type: 'Partnership Agreement', icon: 'i-lucide-handshake', toneClass: 'bg-blue-50 text-blue-600' },
  {
    type: 'Non-Disclosure Agreement',
    icon: 'i-lucide-file-lock',
    toneClass: 'bg-violet-50 text-violet-600'
  },
  {
    type: 'Data Processing Agreement',
    icon: 'i-lucide-database',
    toneClass: 'bg-cyan-50 text-cyan-600'
  },
  { type: 'Business License', icon: 'i-lucide-badge-check', toneClass: 'bg-emerald-50 text-emerald-600' },
  { type: 'Tax Document', icon: 'i-lucide-receipt', toneClass: 'bg-amber-50 text-amber-600' },
  { type: 'Certification', icon: 'i-lucide-award', toneClass: 'bg-orange-50 text-orange-600' },
  { type: 'Insurance', icon: 'i-lucide-shield-check', toneClass: 'bg-teal-50 text-teal-600' },
  { type: 'Policy Document', icon: 'i-lucide-book-open', toneClass: 'bg-slate-100 text-slate-600' }
]

// 3. Aturan status mengikuti aturan kedaluwarsa aplikasi (<= 30 hari = Expiring Soon)
const daysUntil = (iso: string) => {
  const target = new Date(`${iso}T00:00:00`)
  return Math.round((target.getTime() - today.getTime()) / MS_PER_DAY)
}

const getStatus = (doc: LegalDocument): DocumentStatus => {
  const days = daysUntil(doc.expiryDate)
  if (days < 0) return 'Expired'
  if (days <= EXPIRING_SOON_DAYS) return 'Expiring Soon'
  return 'Valid'
}

const docsWithStatus = computed<DocumentWithStatus[]>(() =>
  documents.value.map(doc => ({ ...doc, status: getStatus(doc) }))
)

// 4. Stat Cards (dihitung dari data agar konsisten dengan status sebenarnya)
const statCards = computed(() => [
  {
    label: 'Total Documents',
    value: documents.value.length,
    description: 'All legal documents',
    icon: 'i-lucide-file-text',
    toneClass: 'bg-blue-50 text-blue-600'
  },
  {
    label: 'Valid Documents',
    value: docsWithStatus.value.filter(doc => doc.status === 'Valid').length,
    description: 'Currently valid',
    icon: 'i-lucide-circle-check-big',
    toneClass: 'bg-emerald-50 text-emerald-600'
  },
  {
    label: 'Expiring Soon',
    value: docsWithStatus.value.filter(doc => doc.status === 'Expiring Soon').length,
    description: 'Within next 30 days',
    icon: 'i-lucide-clock',
    toneClass: 'bg-orange-50 text-orange-600'
  },
  {
    label: 'Expired Documents',
    value: docsWithStatus.value.filter(doc => doc.status === 'Expired').length,
    description: 'Requires renewal',
    icon: 'i-lucide-circle-x',
    toneClass: 'bg-rose-50 text-rose-600'
  }
])

// 5. Filter state
const search = ref('')
const typeFilter = ref('')
const statusFilter = ref('')
const expiryFilter = ref('')

const statusOptions: DocumentStatus[] = ['Valid', 'Expiring Soon', 'Expired']

const expiryOptions: { label: string, value: string }[] = [
  { label: 'All Expiry Date', value: '' },
  { label: 'Expiring in 30 days', value: 'next-30' },
  { label: 'Expiring in 90 days', value: 'next-90' },
  { label: 'Expired', value: 'expired' }
]

const matchesExpiry = (doc: DocumentWithStatus) => {
  if (!expiryFilter.value) return true
  const days = daysUntil(doc.expiryDate)
  if (expiryFilter.value === 'expired') return days < 0
  if (expiryFilter.value === 'next-30') return days >= 0 && days <= 30
  if (expiryFilter.value === 'next-90') return days >= 0 && days <= 90
  return true
}

const filteredDocuments = computed(() => {
  const keyword = search.value.trim().toLowerCase()
  return docsWithStatus.value.filter((doc) => {
    const matchSearch
      = !keyword
        || doc.name.toLowerCase().includes(keyword)
        || doc.fileName.toLowerCase().includes(keyword)
    const matchType = !typeFilter.value || doc.documentType === typeFilter.value
    const matchStatus = !statusFilter.value || doc.status === statusFilter.value
    const matchExpiry = matchesExpiry(doc)
    return matchSearch && matchType && matchStatus && matchExpiry
  })
})

// 6. Selection
const selectedIds = ref<string[]>([])
const headerCheckbox = ref<HTMLInputElement | null>(null)

const filteredIds = computed(() => filteredDocuments.value.map(doc => doc.id))
const allSelected = computed(
  () => filteredIds.value.length > 0 && filteredIds.value.every(id => selectedIds.value.includes(id))
)
const someSelected = computed(
  () => filteredIds.value.some(id => selectedIds.value.includes(id)) && !allSelected.value
)

watchEffect(() => {
  if (headerCheckbox.value) {
    headerCheckbox.value.indeterminate = someSelected.value
  }
})

const toggleRow = (id: string) => {
  selectedIds.value = selectedIds.value.includes(id)
    ? selectedIds.value.filter(selected => selected !== id)
    : [...selectedIds.value, id]
}

const toggleAll = () => {
  if (allSelected.value) {
    selectedIds.value = selectedIds.value.filter(id => !filteredIds.value.includes(id))
  } else {
    selectedIds.value = [...new Set([...selectedIds.value, ...filteredIds.value])]
  }
}

const selectedDocuments = computed(() =>
  documents.value.filter(doc => selectedIds.value.includes(doc.id))
)

const downloadableSelected = computed(() =>
  selectedDocuments.value.filter(doc => doc.fileAvailable)
)

// 7. Pagination
const page = ref(1)

watch([search, typeFilter, statusFilter, expiryFilter], () => {
  page.value = 1
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredDocuments.value.length / PAGE_SIZE)))

watch(totalPages, (value) => {
  if (page.value > value) page.value = value
})

const pagedDocuments = computed(() => {
  const start = (page.value - 1) * PAGE_SIZE
  return filteredDocuments.value.slice(start, start + PAGE_SIZE)
})

const rangeStart = computed(() =>
  filteredDocuments.value.length === 0 ? 0 : (page.value - 1) * PAGE_SIZE + 1
)
const rangeEnd = computed(() => Math.min(page.value * PAGE_SIZE, filteredDocuments.value.length))

// 8. Notifikasi aksi (tidak mengklaim upload/download backend berhasil)
const notice = ref<ActionNotice | null>(null)
let noticeTimer: ReturnType<typeof setTimeout> | null = null

const showNotice = (message: string, tone: NoticeTone = 'info') => {
  notice.value = { message, tone }
  if (noticeTimer) clearTimeout(noticeTimer)
  noticeTimer = setTimeout(() => {
    notice.value = null
  }, 4000)
}

onBeforeUnmount(() => {
  if (noticeTimer) clearTimeout(noticeTimer)
})

// 9. Upload modal (mock)
const uploadOpen = ref(false)
const uploadForm = ref({
  name: '',
  documentType: 'Partnership Agreement' as DocumentType,
  version: 'v1.0',
  issueDate: '',
  expiryDate: '',
  fileName: ''
})

const resetUploadForm = () => {
  uploadForm.value = {
    name: '',
    documentType: 'Partnership Agreement',
    version: 'v1.0',
    issueDate: '',
    expiryDate: '',
    fileName: ''
  }
}

const openUpload = () => {
  resetUploadForm()
  uploadOpen.value = true
}

const closeUpload = () => {
  uploadOpen.value = false
}

const handleUploadSubmit = () => {
  const name = uploadForm.value.name.trim()
  if (!name) {
    showNotice('Document name is required.', 'warning')
    return
  }
  if (!uploadForm.value.expiryDate) {
    showNotice('Expiry date is required.', 'warning')
    return
  }

  const fileName = uploadForm.value.fileName.trim()
  const isDocx = fileName.toLowerCase().endsWith('.docx')

  documents.value = [
    ...documents.value,
    {
      id: `DOC-${Date.now()}`,
      name,
      fileName: fileName || `${name.toLowerCase().replace(/[^a-z0-9]+/g, '_')}.pdf`,
      fileType: isDocx ? 'docx' : 'pdf',
      documentType: uploadForm.value.documentType,
      version: uploadForm.value.version.trim() || 'v1.0',
      issueDate: uploadForm.value.issueDate || new Date().toISOString().slice(0, 10),
      expiryDate: uploadForm.value.expiryDate,
      fileAvailable: true
    }
  ]

  uploadOpen.value = false
  showNotice(
    'Document added to this view. File upload is a mock and is not persisted to a backend.',
    'warning'
  )
}

// 10. Actions
const fileIcon = (fileType: FileType) =>
  fileType === 'pdf' ? 'i-lucide-file-text' : 'i-lucide-file-type'

const fileIconClass = (fileType: FileType) =>
  fileType === 'pdf' ? 'bg-rose-50 text-rose-600' : 'bg-blue-50 text-blue-600'

const statusBadgeClass = (status: DocumentStatus) => {
  switch (status) {
    case 'Valid':
      return 'bg-emerald-50 text-emerald-700 border-emerald-200'
    case 'Expiring Soon':
      return 'bg-orange-50 text-orange-700 border-orange-200'
    case 'Expired':
      return 'bg-rose-50 text-rose-700 border-rose-200'
    default:
      return 'bg-slate-100 text-slate-600 border-slate-200'
  }
}

const formatDate = (iso: string) => {
  if (!iso) return '—'
  return new Date(`${iso}T00:00:00`).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const typeCount = (type: DocumentType) => documents.value.filter(doc => doc.documentType === type).length

const toggleTypeFilter = (type: DocumentType) => {
  typeFilter.value = typeFilter.value === type ? '' : type
}

const handleDownload = (doc: DocumentWithStatus) => {
  if (!doc.fileAvailable) {
    showNotice(`No file available for ${doc.name}.`, 'warning')
    return
  }
  showNotice(`Download for "${doc.fileName}" requested. File storage is not connected yet.`)
}

const handleDownloadSelected = () => {
  const count = downloadableSelected.value.length
  if (count === 0) {
    showNotice('No downloadable files for the selected documents.', 'warning')
    return
  }
  showNotice(`Download requested for ${count} document(s). File storage is not connected yet.`)
}

const handleDelete = (doc: DocumentWithStatus) => {
  documents.value = documents.value.filter(item => item.id !== doc.id)
  selectedIds.value = selectedIds.value.filter(id => id !== doc.id)
  showNotice(`"${doc.name}" removed from this view (changes are not persisted).`, 'warning')
}

const rowMenuItems = (doc: DocumentWithStatus): RowMenuItem[][] => [
  [
    {
      label: 'View Details',
      icon: 'i-lucide-eye',
      onSelect: () => showNotice(`Detail view for "${doc.name}" is not connected to a backend yet.`)
    },
    {
      label: 'Download',
      icon: 'i-lucide-download',
      disabled: !doc.fileAvailable,
      onSelect: () => handleDownload(doc)
    }
  ],
  [
    {
      label: 'Replace File',
      icon: 'i-lucide-refresh-cw',
      onSelect: () => showNotice(`Replacing the file for "${doc.name}" is not connected yet.`)
    },
    {
      label: 'Delete',
      icon: 'i-lucide-trash-2',
      color: 'error' as const,
      onSelect: () => handleDelete(doc)
    }
  ]
]
</script>

<template>
  <div class="flex flex-col gap-3">
    <!-- A. Empat kartu statistik -->
    <div class="grid shrink-0 grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">
      <div
        v-for="card in statCards"
        :key="card.label"
        class="flex items-center gap-3 rounded-xl border border-slate-200/80 bg-white p-3 shadow-2xs"
      >
        <div
          class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg"
          :class="card.toneClass"
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

    <!-- B/C/D. Panel utama + panel kanan -->
    <div class="grid min-w-0 grid-cols-1 gap-3 lg:grid-cols-[minmax(0,7fr)_minmax(0,3fr)]">
      <!-- Left: Legal Documents panel -->
      <div
        class="flex min-w-0 flex-col gap-3 rounded-xl border border-slate-200/80 bg-white p-3 shadow-2xs"
      >
        <!-- Judul + Upload -->
        <div
          class="flex shrink-0 flex-col gap-2.5 border-b border-slate-100 pb-2.5 sm:flex-row sm:items-start sm:justify-between"
        >
          <div class="min-w-0">
            <h2 class="text-base font-semibold tracking-tight text-slate-900">
              Legal Documents
            </h2>
            <p class="mt-1 text-xs text-slate-500">
              Manage and track all legal documents associated with this partnership.
            </p>
          </div>
          <button
            type="button"
            class="inline-flex shrink-0 items-center gap-1.5 rounded-lg bg-blue-600 px-3.5 py-2 text-xs font-semibold text-white shadow-2xs transition-colors hover:bg-blue-700 cursor-pointer"
            @click="openUpload"
          >
            <UIcon
              name="i-lucide-upload"
              class="h-3.5 w-3.5"
            />
            <span>Upload Document</span>
          </button>
        </div>

        <!-- Search + Filter -->
        <div
          class="grid shrink-0 grid-cols-1 gap-2.5 sm:grid-cols-2 lg:grid-cols-[minmax(0,1.6fr)_minmax(0,1.4fr)_minmax(0,0.85fr)_minmax(0,1.05fr)] lg:items-center"
        >
          <div class="relative w-full min-w-0">
            <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400">
              <UIcon
                name="i-lucide-search"
                class="h-4 w-4"
              />
            </div>
            <input
              v-model="search"
              type="text"
              placeholder="Search document name..."
              class="h-9 w-full rounded-lg border border-slate-200 bg-white pr-3 pl-9 text-xs text-slate-800 placeholder-slate-400 transition-colors focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
            >
          </div>

          <select
            v-model="typeFilter"
            class="h-9 min-w-0 w-full rounded-lg border border-slate-200 bg-white px-2 text-xs font-medium text-slate-700 shadow-2xs focus:border-blue-500 focus:outline-none cursor-pointer"
          >
            <option value="">
              All Document Types
            </option>
            <option
              v-for="docType in documentTypes"
              :key="docType.type"
              :value="docType.type"
            >
              {{ docType.type }}
            </option>
          </select>

          <select
            v-model="statusFilter"
            class="h-9 min-w-0 w-full rounded-lg border border-slate-200 bg-white px-2 text-xs font-medium text-slate-700 shadow-2xs focus:border-blue-500 focus:outline-none cursor-pointer"
          >
            <option value="">
              All Status
            </option>
            <option
              v-for="status in statusOptions"
              :key="status"
              :value="status"
            >
              {{ status }}
            </option>
          </select>

          <select
            v-model="expiryFilter"
            class="h-9 min-w-0 w-full rounded-lg border border-slate-200 bg-white px-2 text-xs font-medium text-slate-700 shadow-2xs focus:border-blue-500 focus:outline-none cursor-pointer"
          >
            <option
              v-for="option in expiryOptions"
              :key="option.value"
              :value="option.value"
            >
              {{ option.label }}
            </option>
          </select>
        </div>

        <!-- Selection bar -->
        <div
          v-if="selectedIds.length > 0"
          class="flex shrink-0 flex-wrap items-center justify-between gap-2 rounded-lg border border-blue-100 bg-blue-50/60 px-3 py-1.5"
        >
          <p class="text-xs font-semibold text-blue-700">
            {{ selectedIds.length }} document(s) selected
          </p>
          <button
            type="button"
            class="inline-flex items-center gap-1.5 rounded-lg border border-blue-200 bg-white px-2.5 py-1 text-xs font-semibold text-blue-700 shadow-2xs transition-colors hover:bg-blue-50 cursor-pointer"
            @click="handleDownloadSelected"
          >
            <UIcon
              name="i-lucide-download"
              class="h-3.5 w-3.5"
            />
            <span>Download ({{ downloadableSelected.length }})</span>
          </button>
        </div>

        <!-- Tabel dokumen -->
        <div class="min-w-0">
          <table class="w-full table-fixed text-left text-xs">
            <thead class="border-b border-slate-100 text-[11px] font-semibold tracking-wide text-slate-500">
              <tr>
                <th class="w-[4%] py-2 pr-2">
                  <input
                    ref="headerCheckbox"
                    type="checkbox"
                    class="h-3.5 w-3.5 cursor-pointer accent-blue-600"
                    :checked="allSelected"
                    aria-label="Select all documents"
                    @change="toggleAll"
                  >
                </th>
                <th class="w-[24%] px-1.5 py-2">
                  Document Name
                </th>
                <th class="w-[19%] px-1.5 py-2">
                  Document Type
                </th>
                <th class="w-[8%] px-1.5 py-2">
                  Version
                </th>
                <th class="w-[12%] px-1.5 py-2">
                  Issue Date
                </th>
                <th class="w-[12%] px-1.5 py-2">
                  Expiry Date
                </th>
                <th class="w-[13%] px-1.5 py-2">
                  Status
                </th>
                <th class="w-[8%] py-2 pl-1.5 text-right">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr
                v-for="doc in pagedDocuments"
                :key="doc.id"
                class="transition-colors hover:bg-slate-50/60"
              >
                <td class="py-1 pr-2">
                  <input
                    type="checkbox"
                    class="h-3.5 w-3.5 cursor-pointer accent-blue-600"
                    :checked="selectedIds.includes(doc.id)"
                    :aria-label="`Select ${doc.name}`"
                    @change="toggleRow(doc.id)"
                  >
                </td>

                <td class="px-1.5 py-1">
                  <div class="flex items-center gap-2.5">
                    <div
                      class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg"
                      :class="fileIconClass(doc.fileType)"
                    >
                      <UIcon
                        :name="fileIcon(doc.fileType)"
                        class="h-4 w-4"
                      />
                    </div>
                    <div class="min-w-0">
                      <p
                        class="truncate text-xs font-semibold text-slate-800"
                        :title="doc.name"
                      >
                        {{ doc.name }}
                      </p>
                      <p
                        class="truncate text-[11px] text-slate-400"
                        :title="doc.fileName"
                      >
                        {{ doc.fileName }}
                      </p>
                    </div>
                  </div>
                </td>

                <td class="px-1.5 py-1 text-slate-600">
                  {{ doc.documentType }}
                </td>

                <td class="px-1.5 py-1 whitespace-nowrap">
                  <span class="rounded-md bg-slate-100 px-1.5 py-0.5 text-[11px] font-semibold text-slate-600">
                    {{ doc.version }}
                  </span>
                </td>

                <td class="px-1.5 py-1 text-[11px] whitespace-nowrap text-slate-500">
                  {{ formatDate(doc.issueDate) }}
                </td>

                <td class="px-1.5 py-1 text-[11px] whitespace-nowrap text-slate-500">
                  {{ formatDate(doc.expiryDate) }}
                </td>

                <td class="px-1.5 py-1 whitespace-nowrap">
                  <span
                    class="inline-flex items-center rounded-full border px-2 py-0.5 text-[10px] font-semibold"
                    :class="statusBadgeClass(doc.status)"
                  >
                    {{ doc.status }}
                  </span>
                </td>

                <td class="py-1 pl-1.5 text-right">
                  <UDropdownMenu
                    :items="rowMenuItems(doc)"
                    :content="{ align: 'end' }"
                  >
                    <button
                      type="button"
                      class="inline-flex h-7 w-7 items-center justify-center rounded-md text-slate-400 transition-colors hover:bg-slate-100 hover:text-slate-700 cursor-pointer"
                      aria-label="Document actions"
                    >
                      <UIcon
                        name="i-lucide-ellipsis-vertical"
                        class="h-4 w-4"
                      />
                    </button>
                  </UDropdownMenu>
                </td>
              </tr>

              <tr v-if="filteredDocuments.length === 0">
                <td
                  colspan="8"
                  class="px-4 py-6 text-center"
                >
                  <div class="flex flex-col items-center gap-1.5">
                    <UIcon
                      name="i-lucide-search-x"
                      class="h-6 w-6 text-slate-300"
                    />
                    <p class="text-xs font-semibold text-slate-600">
                      No documents found
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

        <!-- Pagination -->
        <div class="flex shrink-0 items-center justify-between gap-2 border-t border-slate-100 pt-2.5">
          <p class="text-xs text-slate-500">
            Showing
            <span class="font-semibold text-slate-700">{{ rangeStart }}</span>
            to
            <span class="font-semibold text-slate-700">{{ rangeEnd }}</span>
            of
            <span class="font-semibold text-slate-700">{{ filteredDocuments.length }}</span>
          </p>

          <div class="flex items-center gap-1">
            <button
              type="button"
              class="inline-flex h-7 w-7 items-center justify-center rounded-md border border-slate-200 bg-white text-slate-600 transition-colors hover:bg-slate-50 disabled:opacity-40 cursor-pointer"
              :disabled="page <= 1"
              aria-label="Previous page"
              @click="page--"
            >
              <UIcon
                name="i-lucide-chevron-left"
                class="h-3.5 w-3.5"
              />
            </button>

            <button
              v-for="pageNumber in totalPages"
              :key="pageNumber"
              type="button"
              class="inline-flex h-7 w-7 items-center justify-center rounded-md text-[11px] font-semibold cursor-pointer"
              :class="[
                page === pageNumber
                  ? 'bg-blue-600 text-white shadow-2xs'
                  : 'border border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
              ]"
              @click="page = pageNumber"
            >
              {{ pageNumber }}
            </button>

            <button
              type="button"
              class="inline-flex h-7 w-7 items-center justify-center rounded-md border border-slate-200 bg-white text-slate-600 transition-colors hover:bg-slate-50 disabled:opacity-40 cursor-pointer"
              :disabled="page >= totalPages"
              aria-label="Next page"
              @click="page++"
            >
              <UIcon
                name="i-lucide-chevron-right"
                class="h-3.5 w-3.5"
              />
            </button>
          </div>
        </div>
      </div>

      <!-- Right: Document Type + About -->
      <div class="flex min-w-0 flex-col gap-2.5">
        <!-- Document Type -->
        <div class="space-y-1.5 rounded-xl border border-slate-200/80 bg-white p-2.5 shadow-2xs">
          <div class="border-b border-slate-100 pb-1.5">
            <h2 class="text-sm font-semibold text-slate-900">
              Document Type
            </h2>
          </div>

          <div class="space-y-0.5">
            <button
              v-for="docType in documentTypes"
              :key="docType.type"
              type="button"
              class="flex w-full items-center justify-between gap-2 rounded-lg px-2 py-1 text-left transition-colors hover:bg-slate-50 cursor-pointer"
              :class="{ 'bg-blue-50/60': typeFilter === docType.type }"
              @click="toggleTypeFilter(docType.type)"
            >
              <div class="flex min-w-0 items-center gap-2.5">
                <div
                  class="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg"
                  :class="docType.toneClass"
                >
                  <UIcon
                    :name="docType.icon"
                    class="h-3.5 w-3.5"
                  />
                </div>
                <span class="truncate text-xs font-semibold text-slate-700">
                  {{ docType.type }}
                </span>
              </div>
              <span class="shrink-0 rounded-full bg-slate-100 px-2 py-0.5 text-[10px] font-bold text-slate-600">
                {{ typeCount(docType.type) }}
              </span>
            </button>
          </div>
        </div>

        <!-- About Legal Documents -->
        <div class="space-y-1.5 rounded-xl border border-slate-200/80 bg-white p-2.5 shadow-2xs">
          <div class="flex items-center gap-2 border-b border-slate-100 pb-1.5">
            <UIcon
              name="i-lucide-info"
              class="h-4 w-4 text-blue-600"
            />
            <h2 class="text-sm font-semibold text-slate-900">
              About Legal Documents
            </h2>
          </div>

          <p class="text-xs leading-relaxed text-slate-600">
            Legal documents must always be kept up to date. Ensure all agreements, licenses, and
            certificates remain valid throughout the partnership.
          </p>

          <div class="flex items-start gap-2 rounded-lg border border-amber-100 bg-amber-50/60 p-2.5">
            <UIcon
              name="i-lucide-bell-ring"
              class="mt-0.5 h-4 w-4 shrink-0 text-amber-600"
            />
            <p class="text-[11px] leading-relaxed text-amber-800">
              You will be reminded 30 days before any document expires.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Upload Document Modal (mock) -->
    <div
      v-if="uploadOpen"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4 backdrop-blur-sm"
      @click.self="closeUpload"
    >
      <div class="w-full max-w-lg overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-2xl">
        <div class="flex items-start justify-between border-b border-slate-100 p-5 pb-4">
          <div>
            <h3 class="text-base font-bold tracking-tight text-slate-900">
              Upload Document
            </h3>
            <p class="mt-0.5 text-xs text-slate-500">
              Add a new legal document to this partnership.
            </p>
          </div>
          <button
            type="button"
            class="rounded-lg p-1.5 text-slate-400 transition-colors hover:bg-slate-100 hover:text-slate-700 cursor-pointer"
            aria-label="Close"
            @click="closeUpload"
          >
            <UIcon
              name="i-lucide-x"
              class="h-4 w-4"
            />
          </button>
        </div>

        <div class="grid grid-cols-1 gap-4 p-5 sm:grid-cols-2">
          <div class="space-y-1.5 sm:col-span-2">
            <label class="text-xs font-bold text-slate-800">
              Document Name <span class="text-rose-500">*</span>
            </label>
            <input
              v-model="uploadForm.name"
              type="text"
              placeholder="e.g. Master Service Agreement"
              class="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-xs text-slate-800 placeholder-slate-400 shadow-2xs transition-colors focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
            >
          </div>

          <div class="space-y-1.5">
            <label class="text-xs font-bold text-slate-800">Document Type</label>
            <select
              v-model="uploadForm.documentType"
              class="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-xs font-medium text-slate-700 shadow-2xs focus:border-blue-500 focus:outline-none cursor-pointer"
            >
              <option
                v-for="docType in documentTypes"
                :key="docType.type"
                :value="docType.type"
              >
                {{ docType.type }}
              </option>
            </select>
          </div>

          <div class="space-y-1.5">
            <label class="text-xs font-bold text-slate-800">Version</label>
            <input
              v-model="uploadForm.version"
              type="text"
              placeholder="v1.0"
              class="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-xs text-slate-800 placeholder-slate-400 shadow-2xs transition-colors focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
            >
          </div>

          <div class="space-y-1.5">
            <label class="text-xs font-bold text-slate-800">Issue Date</label>
            <input
              v-model="uploadForm.issueDate"
              type="date"
              class="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-xs text-slate-700 shadow-2xs focus:border-blue-500 focus:outline-none cursor-pointer"
            >
          </div>

          <div class="space-y-1.5">
            <label class="text-xs font-bold text-slate-800">
              Expiry Date <span class="text-rose-500">*</span>
            </label>
            <input
              v-model="uploadForm.expiryDate"
              type="date"
              class="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-xs text-slate-700 shadow-2xs focus:border-blue-500 focus:outline-none cursor-pointer"
            >
          </div>

          <div class="space-y-1.5 sm:col-span-2">
            <label class="text-xs font-bold text-slate-800">File Name</label>
            <input
              v-model="uploadForm.fileName"
              type="text"
              placeholder="document_name.pdf"
              class="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-xs text-slate-800 placeholder-slate-400 shadow-2xs transition-colors focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
            >
          </div>

          <div class="flex items-start gap-2 rounded-xl border border-blue-100 bg-blue-50/60 p-3 text-[11px] text-blue-800 sm:col-span-2">
            <UIcon
              name="i-lucide-info"
              class="mt-0.5 h-3.5 w-3.5 shrink-0 text-blue-600"
            />
            <span>File upload is not connected to a backend yet. Submitting adds the document to this
              view only.</span>
          </div>
        </div>

        <div class="flex items-center justify-end gap-2.5 border-t border-slate-100 bg-slate-50/50 p-4">
          <button
            type="button"
            class="rounded-xl border border-slate-200 bg-white px-4 py-2 text-xs font-semibold text-slate-700 shadow-2xs transition-colors hover:bg-slate-50 cursor-pointer"
            @click="closeUpload"
          >
            Cancel
          </button>
          <button
            type="button"
            class="rounded-xl bg-blue-600 px-5 py-2 text-xs font-semibold text-white shadow-xs transition-all hover:bg-blue-700 active:scale-95 cursor-pointer"
            @click="handleUploadSubmit"
          >
            Add Document
          </button>
        </div>
      </div>
    </div>

    <!-- Toast notifikasi aksi -->
    <div
      v-if="notice"
      class="fixed right-5 bottom-5 z-50 flex max-w-xs items-start gap-2 rounded-xl border p-3 shadow-lg"
      :class="
        notice.tone === 'warning'
          ? 'border-amber-200 bg-amber-50 text-amber-800'
          : 'border-blue-200 bg-blue-50 text-blue-800'
      "
    >
      <UIcon
        :name="notice.tone === 'warning' ? 'i-lucide-triangle-alert' : 'i-lucide-info'"
        class="mt-0.5 h-4 w-4 shrink-0"
      />
      <p class="text-[11px] leading-relaxed">
        {{ notice.message }}
      </p>
    </div>
  </div>
</template>
