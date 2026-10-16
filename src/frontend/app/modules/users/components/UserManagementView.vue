<script setup lang="ts">
import { ref } from 'vue'
import type { UserStats, PendingUserRequest, ActiveUser, UserRole } from '../types/types'

import UsersStatsCards from './UsersStatsCards.vue'
import PendingRequestsTable from './PendingRequestsTable.vue'
import ActiveUsersTable from './ActiveUsersTable.vue'
import AssignRoleModal from './AssignRoleModal.vue'

const toast = useToast()

// State Modal Review & Assign Role
const isAssignModalOpen = ref(false)
const selectedUserForAssign = ref<PendingUserRequest | null>(null)

// 1. Saat tombol Review diklik di tabel Pending
const handleReviewUser = (user: PendingUserRequest) => {
  selectedUserForAssign.value = user
  isAssignModalOpen.value = true
}

// 2. Saat Admin klik "Approve" pada Modal Review
const handleApproveUser = (user: PendingUserRequest) => {
  // Mapping role request ke UserRole sistem untuk tabel Active Users
  let mappedRole: UserRole = 'Engineer'
  const reqRole = String(user.requestedRole).toLowerCase()
  if (reqRole.includes('commercial')) {
    mappedRole = 'Commercial'
  } else if (reqRole.includes('executive')) {
    mappedRole = 'Executive'
  }

  // A. Hapus user dari list pending
  pendingRequests.value = pendingRequests.value.filter((u) => u.id !== user.id)

  // B. Masukkan ke list Active Users paling atas
  activeUsers.value.unshift({
    id: user.id,
    name: user.name,
    email: user.email,
    role: mappedRole,
    status: 'Active',
    assignedDate: 'Just now'
  })

  // C. Update counter angka KPI
  statsData.value.pendingRequests--
  statsData.value.activeUsers++

  toast.add({
    title: 'Request Approved',
    description: `${user.name} has been approved as ${mappedRole}.`,
    color: 'success'
  })
}

// 3. Saat Admin klik "Reject" pada Modal Review
const handleRejectUser = (user: PendingUserRequest) => {
  // Hapus dari pending requests
  pendingRequests.value = pendingRequests.value.filter((u) => u.id !== user.id)
  statsData.value.pendingRequests--

  toast.add({
    title: 'Request Rejected',
    description: `Request for ${user.name} has been rejected.`,
    color: 'error'
  })
}

// Data Statistik (4 Top KPI Cards)
const statsData = ref<UserStats>({
  pendingRequests: 8,
  totalUsers: 24,
  activeUsers: 16,
  inactiveUsers: 0
})

// Data Pending Access Requests (Persis sesuai gambar referensi)
const pendingRequests = ref<PendingUserRequest[]>([
  {
    id: '1',
    name: 'Andi Pratama',
    email: 'andi.pratama@company.com',
    division: 'Technology',
    requestedRole: 'Engineer / Project Lead',
    requestDate: 'Oct 10, 2026 09:15',
    status: 'Pending',
    requestReason:
      'I need access to manage technical portfolio data and review partner capabilities for ongoing projects. This role is required to support my current responsibilities in the technology division.'
  },
  {
    id: '2',
    name: 'Sarah Wijaya',
    email: 'sarah.wijaya@company.com',
    division: 'Commercial',
    requestedRole: 'Commercial / Partnership Officer',
    requestDate: 'Oct 11, 2026 14:22',
    status: 'Pending',
    requestReason:
      'Need access to manage partner accounts, partnership documents, and monitor collaboration pipelines.'
  },
  {
    id: '3',
    name: 'Budi Santoso',
    email: 'budi.santoso@company.com',
    division: 'Technology',
    requestedRole: 'Engineer / Project Lead',
    requestDate: 'Oct 12, 2026 10:37',
    status: 'Pending',
    requestReason:
      'Require platform access to update system architecture records and engineering project metrics.'
  },
  {
    id: '4',
    name: 'Maya Putri',
    email: 'maya.putri@company.com',
    division: 'Operations',
    requestedRole: 'Commercial / Partnership Officer',
    requestDate: 'Oct 12, 2026 16:05',
    status: 'Pending',
    requestReason:
      'Responsible for coordinating strategic partner vendor relationships and SLAs across operating units.'
  },
  {
    id: '5',
    name: 'Daniel Kurniawan',
    email: 'daniel.kurniawan@company.com',
    division: 'Technology',
    requestedRole: 'Engineer / Project Lead',
    requestDate: 'Oct 13, 2026 08:21',
    status: 'Pending',
    requestReason:
      'Need access to upload technical documentation and perform project milestone evaluations.'
  },
  {
    id: '6',
    name: 'Fajar Nugraha',
    email: 'fajar.nugraha@company.com',
    division: 'Technology',
    requestedRole: 'Engineer / Project Lead',
    requestDate: 'Oct 13, 2026 10:11',
    status: 'Pending',
    requestReason:
      'Reviewing technology integrations and code deliverables from registered technology partners.'
  },
  {
    id: '7',
    name: 'Rina Marlina',
    email: 'rina.marlina@company.com',
    division: 'Commercial',
    requestedRole: 'Commercial / Partnership Officer',
    requestDate: 'Oct 13, 2026 11:45',
    status: 'Pending',
    requestReason: 'Managing ongoing commercial partner contract reviews and renewal schedules.'
  },
  {
    id: '8',
    name: 'Hendra Setiawan',
    email: 'hendra.setiawan@company.com',
    division: 'Operations',
    requestedRole: 'Commercial / Partnership Officer',
    requestDate: 'Oct 13, 2026 13:20',
    status: 'Pending',
    requestReason: 'Tracking operational synergy and partner deliverables for enterprise clients.'
  }
])

// Data Users Internal (16 Active Users)
const activeUsers = ref<ActiveUser[]>([
  {
    id: '1',
    name: 'Rizky Hidayat',
    email: 'rizky.hidayat@company.com',
    role: 'Commercial',
    status: 'Active',
    assignedDate: 'Jan 15, 2026'
  },
  {
    id: '2',
    name: 'Jessica Tan',
    email: 'jessica.tan@company.com',
    role: 'Engineer',
    status: 'Active',
    assignedDate: 'Jan 12, 2026'
  },
  {
    id: '3',
    name: 'Arief Nugroho',
    email: 'arief.nugroho@company.com',
    role: 'Executive',
    status: 'Active',
    assignedDate: 'Jan 10, 2026'
  },
  {
    id: '4',
    name: 'Putri Anggraini',
    email: 'putri.anggraini@company.com',
    role: 'Commercial',
    status: 'Active',
    assignedDate: 'Jan 8, 2026'
  },
  {
    id: '5',
    name: 'Dimas Setiawan',
    email: 'dimas.setiawan@company.com',
    role: 'Engineer',
    status: 'Active',
    assignedDate: 'Jan 5, 2026'
  },
  {
    id: '6',
    name: 'Bayu Pratama',
    email: 'bayu.pratama@company.com',
    role: 'Commercial',
    status: 'Active',
    assignedDate: 'Dec 28, 2025'
  },
  {
    id: '7',
    name: 'Cindy Aurelia',
    email: 'cindy.aurelia@company.com',
    role: 'Engineer',
    status: 'Active',
    assignedDate: 'Dec 20, 2025'
  },
  {
    id: '8',
    name: 'Farhan Ramadhan',
    email: 'farhan.ramadhan@company.com',
    role: 'Engineer',
    status: 'Active',
    assignedDate: 'Dec 15, 2025'
  },
  {
    id: '9',
    name: 'Gita Permata',
    email: 'gita.permata@company.com',
    role: 'Executive',
    status: 'Active',
    assignedDate: 'Dec 10, 2025'
  },
  {
    id: '10',
    name: 'Kevin Sanjaya',
    email: 'kevin.sanjaya@company.com',
    role: 'Commercial',
    status: 'Active',
    assignedDate: 'Dec 05, 2025'
  },
  {
    id: '11',
    name: 'Laila Rahmawati',
    email: 'laila.rahmawati@company.com',
    role: 'Engineer',
    status: 'Active',
    assignedDate: 'Nov 30, 2025'
  },
  {
    id: '12',
    name: 'Mega Utami',
    email: 'mega.utami@company.com',
    role: 'Commercial',
    status: 'Active',
    assignedDate: 'Nov 25, 2025'
  },
  {
    id: '13',
    name: 'Nadia Safitri',
    email: 'nadia.safitri@company.com',
    role: 'Engineer',
    status: 'Active',
    assignedDate: 'Nov 20, 2025'
  },
  {
    id: '14',
    name: 'Oki Pratama',
    email: 'oki.pratama@company.com',
    role: 'Engineer',
    status: 'Active',
    assignedDate: 'Nov 15, 2025'
  },
  {
    id: '15',
    name: 'Pandu Wicaksono',
    email: 'pandu.wicaksono@company.com',
    role: 'Commercial',
    status: 'Active',
    assignedDate: 'Nov 10, 2025'
  },
  {
    id: '16',
    name: 'Roland Brilianto',
    email: 'roland.brilianto@company.com',
    role: 'Executive',
    status: 'Active',
    assignedDate: 'Nov 01, 2025'
  }
])

const handleManageUser = (user: ActiveUser) => {
  alert(`Manage user: ${user.name} (${user.role})`)
}

const handleExport = () => {
  alert('Exporting data users to CSV / Excel...')
}
</script>

<template>
  <div class="space-y-4 pb-10">
    <!-- Breadcrumb & Header Title -->
    <div class="space-y-1">
      <nav class="flex items-center gap-2 text-xs font-medium text-slate-500">
        <span>Administration</span>
        <UIcon name="i-lucide-chevron-right" class="h-3 w-3 text-slate-400" />
        <span class="font-semibold text-slate-800">User Management</span>
      </nav>

      <div class="pt-1">
        <h1 class="text-xl font-bold tracking-tight text-slate-900 leading-tight">
          User Management
        </h1>
        <p class="text-xs text-slate-500">Manage internal users and their access roles.</p>
      </div>
    </div>

    <!-- 1. Top 4 KPI Cards -->
    <UsersStatsCards :stats="statsData" />

    <!-- 2. Pending Access Requests Table -->
    <PendingRequestsTable :requests="pendingRequests" @review="handleReviewUser" />

    <!-- 3. Active Users Table -->
    <ActiveUsersTable :users="activeUsers" @manage-user="handleManageUser" @export="handleExport" />

    <!-- 4. Modal Popup Review Role Request (Approve & Reject) -->
    <AssignRoleModal
      :is-open="isAssignModalOpen"
      :user="selectedUserForAssign"
      @close="isAssignModalOpen = false"
      @approve="handleApproveUser"
      @reject="handleRejectUser"
    />
  </div>
</template>
