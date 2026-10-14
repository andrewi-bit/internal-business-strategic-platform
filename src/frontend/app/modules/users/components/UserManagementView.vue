<script setup lang="ts">
import { ref } from 'vue'
import type { UserStats, PendingUserRequest, ActiveUser, UserRole } from '../types/types'

import UsersStatsCards from './UsersStatsCards.vue'
import PendingRequestsTable from './PendingRequestsTable.vue'
import ActiveUsersTable from './ActiveUsersTable.vue'
import AssignRoleModal from './AssignRoleModal.vue'

// State Modal Assign Role
const isAssignModalOpen = ref(false)
const selectedUserForAssign = ref<PendingUserRequest | null>(null)

// 1. Saat tombol Assign Role diklik di tabel Pending
const handleAssignRole = (user: PendingUserRequest) => {
  selectedUserForAssign.value = user
  isAssignModalOpen.value = true
}

// 2. Saat form modal disubmit (Role berhasil di-assign)
const handleRoleAssigned = ({ user, role }: { user: PendingUserRequest; role: UserRole }) => {
  // A. Hapus user dari list pending
  pendingRequests.value = pendingRequests.value.filter((u) => u.id !== user.id)

  // B. Masukkan ke list Active Users paling atas
  activeUsers.value.unshift({
    id: user.id,
    name: user.name,
    email: user.email,
    role: role,
    status: 'Active',
    assignedDate: 'Just now'
  })

  // C. Update counter angka KPI
  statsData.value.pendingRequests--
  statsData.value.activeUsers++
}

// Data Statistik (4 KPI Cards)
const statsData = ref<UserStats>({
  pendingRequests: 8,
  totalUsers: 24,
  activeUsers: 16,
  inactiveUsers: 0
})

// Data Pending Access Requests (8 Data)
const pendingRequests = ref<PendingUserRequest[]>([
  {
    id: '1',
    name: 'Andi Pratama',
    email: 'andi.pratama@company.com',
    requestDate: 'Oct 10, 2026 09:15',
    status: 'Pending'
  },
  {
    id: '2',
    name: 'Sarah Wijaya',
    email: 'sarah.wijaya@company.com',
    requestDate: 'Oct 11, 2026 14:22',
    status: 'Pending'
  },
  {
    id: '3',
    name: 'Budi Santoso',
    email: 'budi.santoso@company.com',
    requestDate: 'Oct 12, 2026 10:37',
    status: 'Pending'
  },
  {
    id: '4',
    name: 'Maya Putri',
    email: 'maya.putri@company.com',
    requestDate: 'Oct 12, 2026 16:05',
    status: 'Pending'
  },
  {
    id: '5',
    name: 'Daniel Kurniawan',
    email: 'daniel.kurniawan@company.com',
    requestDate: 'Oct 13, 2026 08:21',
    status: 'Pending'
  },
  {
    id: '6',
    name: 'Fajar Nugraha',
    email: 'fajar.nugraha@company.com',
    requestDate: 'Oct 13, 2026 10:11',
    status: 'Pending'
  },
  {
    id: '7',
    name: 'Rina Marlina',
    email: 'rina.marlina@company.com',
    requestDate: 'Oct 13, 2026 11:45',
    status: 'Pending'
  },
  {
    id: '8',
    name: 'Hendra Setiawan',
    email: 'hendra.setiawan@company.com',
    requestDate: 'Oct 13, 2026 13:20',
    status: 'Pending'
  }
])

// Data Users Internal (16 Data dengan Role)
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
    <PendingRequestsTable :requests="pendingRequests" @assign-role="handleAssignRole" />

    <!-- 3. Active Users Table -->
    <ActiveUsersTable :users="activeUsers" @manage-user="handleManageUser" @export="handleExport" />

    <!-- 4. Modal Popup Assign Role -->
    <AssignRoleModal
      :is-open="isAssignModalOpen"
      :user="selectedUserForAssign"
      @close="isAssignModalOpen = false"
      @submit="handleRoleAssigned"
    />
  </div>
</template>
