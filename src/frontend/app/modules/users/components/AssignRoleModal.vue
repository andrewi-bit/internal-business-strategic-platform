<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { PendingUserRequest, UserRole } from '../types/types'

interface Props {
  isOpen: boolean
  user: PendingUserRequest | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'submit', payload: { user: PendingUserRequest; role: UserRole }): void
}>()

// State pilihan role & dropdown
const selectedRole = ref<UserRole | null>(null)
const isDropdownOpen = ref(false) // Default tertutup saat awal dimuat

// Reset pilihan & pastikan dropdown selalu tertutup setiap kali modal dibuka / ditutup
watch(
  () => props.isOpen,
  (newVal) => {
    if (newVal) {
      selectedRole.value = null
      isDropdownOpen.value = false
    }
  }
)

// Ambil inisial nama untuk avatar bulat (misal: "Andi Pratama" -> "AP")
const userInitials = computed(() => {
  if (!props.user?.name) return 'U'
  return props.user.name
    .split(' ')
    .map((n) => n[0])
    .join('')
    .substring(0, 2)
    .toUpperCase()
})

// Opsi role lengkap sesuai BRD dan gambar referensi
const roleOptions: {
  role: UserRole
  title: string
  description: string
  icon: string
  iconBg: string
  iconColor: string
}[] = [
  {
    role: 'Commercial',
    title: 'Commercial / Partnership Officer',
    description: 'Manage partner data and collaboration activities',
    icon: 'i-lucide-users',
    iconBg: 'bg-purple-50',
    iconColor: 'text-purple-600'
  },
  {
    role: 'Engineer',
    title: 'Engineer / Project Lead',
    description: 'Manage technical portfolio and review partner capabilities',
    icon: 'i-lucide-settings',
    iconBg: 'bg-blue-50',
    iconColor: 'text-blue-600'
  },
  {
    role: 'Executive',
    title: 'Executive',
    description: 'Access to executive dashboard and reports',
    icon: 'i-lucide-crown',
    iconBg: 'bg-amber-50',
    iconColor: 'text-amber-600'
  }
]

// Saat user memilih opsi role, simpan role dan tutup kembali dropdown
const handleSelectRole = (role: UserRole) => {
  selectedRole.value = role
  isDropdownOpen.value = false
}

const handleSubmit = () => {
  if (props.user && selectedRole.value) {
    emit('submit', { user: props.user, role: selectedRole.value })
    selectedRole.value = null
    isDropdownOpen.value = false
    emit('close')
  }
}

const handleClose = () => {
  selectedRole.value = null
  isDropdownOpen.value = false
  emit('close')
}
</script>

<template>
  <!-- Backdrop Overlay -->
  <div
    v-if="isOpen && user"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4 backdrop-blur-2xs transition-all animate-fade-in"
    @click.self="handleClose"
  >
    <!-- Modal Card Container -->
    <div
      class="w-full max-w-lg overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-2xl transition-all"
    >
      <!-- 1. Header Modal -->
      <div class="flex items-start justify-between border-b border-slate-100 p-5 pb-4">
        <div>
          <h3 class="text-base font-bold text-slate-900 tracking-tight">Assign Role</h3>
          <p class="text-xs text-slate-500 mt-0.5">Assign an access role to this user.</p>
        </div>

        <!-- Close Button (X) -->
        <button
          type="button"
          class="rounded-lg p-1.5 text-slate-400 transition-colors hover:bg-slate-100 hover:text-slate-700 cursor-pointer"
          aria-label="Close"
          @click="handleClose"
        >
          <UIcon name="i-lucide-x" class="h-4 w-4" />
        </button>
      </div>

      <!-- 2. Modal Body Content -->
      <div class="space-y-4 p-5">
        <!-- User Info Card -->
        <div class="rounded-xl border border-slate-100 bg-slate-50/50 p-3.5 space-y-3">
          <!-- User Details -->
          <div class="flex items-center gap-3">
            <div
              class="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-blue-100 font-bold text-blue-700 text-xs shadow-2xs"
            >
              {{ userInitials }}
            </div>
            <div class="min-w-0">
              <p class="text-xs font-bold text-slate-900 truncate">
                {{ user.name }}
              </p>
              <p class="text-[11px] text-slate-500 truncate">
                {{ user.email }}
              </p>
            </div>
          </div>

          <!-- Request Date & Status Pills Box -->
          <div
            class="flex flex-wrap items-center justify-between gap-2 border-t border-slate-100 pt-2.5 text-xs"
          >
            <div class="flex items-center gap-2">
              <div
                class="flex h-7 w-7 items-center justify-center rounded-lg bg-blue-50 text-blue-600"
              >
                <UIcon name="i-lucide-calendar" class="h-4 w-4" />
              </div>
              <div>
                <p class="text-[10px] text-slate-400 leading-tight">Requested access on</p>
                <p class="text-[11px] font-bold text-slate-800">{{ user.requestDate }}</p>
              </div>
            </div>

            <div class="flex items-center gap-2">
              <div
                class="flex h-7 w-7 items-center justify-center rounded-lg bg-amber-50 text-amber-600"
              >
                <UIcon name="i-lucide-clock" class="h-4 w-4" />
              </div>
              <div>
                <p class="text-[10px] text-slate-400 leading-tight">Current Status</p>
                <span
                  class="inline-flex items-center rounded-full border border-amber-200 bg-amber-50 px-2 py-0.2 text-[10px] font-bold text-amber-700"
                >
                  {{ user.status }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Role Selector Form Field -->
        <div class="space-y-2">
          <label class="text-xs font-bold text-slate-800">
            Select Role <span class="text-rose-500">*</span>
          </label>

          <!-- Input Trigger / Dropdown List Box -->
          <div class="space-y-1.5">
            <!-- Trigger Button -->
            <button
              type="button"
              class="flex w-full items-center justify-between rounded-xl border border-slate-200 bg-white px-3.5 py-2.5 text-xs text-left shadow-2xs hover:border-slate-300 transition-colors cursor-pointer"
              @click="isDropdownOpen = !isDropdownOpen"
            >
              <span :class="selectedRole ? 'font-bold text-slate-900' : 'text-slate-400'">
                {{
                  selectedRole
                    ? roleOptions.find((r) => r.role === selectedRole)?.title
                    : 'Select a role'
                }}
              </span>
              <UIcon
                name="i-lucide-chevron-down"
                class="h-4 w-4 text-slate-400 transition-transform duration-200"
                :class="{ 'rotate-180': isDropdownOpen }"
              />
            </button>

            <!-- Role Options Box (Sesuai Desain) -->
            <div
              v-show="isDropdownOpen"
              class="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-xs divide-y divide-slate-100"
            >
              <button
                v-for="opt in roleOptions"
                :key="opt.role"
                type="button"
                class="flex w-full items-center gap-3.5 p-3 text-left transition-colors cursor-pointer hover:bg-slate-50"
                :class="{ 'bg-blue-50/40': selectedRole === opt.role }"
                @click="handleSelectRole(opt.role)"
              >
                <!-- Icon Box -->
                <div
                  class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl font-bold"
                  :class="[opt.iconBg, opt.iconColor]"
                >
                  <UIcon :name="opt.icon" class="h-4.5 w-4.5" />
                </div>

                <!-- Text Detail -->
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between">
                    <p class="text-xs font-bold text-slate-900">
                      {{ opt.title }}
                    </p>
                    <UIcon
                      v-if="selectedRole === opt.role"
                      name="i-lucide-check"
                      class="h-4 w-4 text-blue-600 font-bold"
                    />
                  </div>
                  <p class="text-[11px] text-slate-500 truncate mt-0.5">
                    {{ opt.description }}
                  </p>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 3. Footer Action Buttons -->
      <div
        class="flex items-center justify-end gap-2.5 border-t border-slate-100 bg-slate-50/50 p-4"
      >
        <button
          type="button"
          class="rounded-xl border border-slate-200 bg-white px-4 py-2 text-xs font-semibold text-slate-700 shadow-2xs hover:bg-slate-50 cursor-pointer transition-colors"
          @click="handleClose"
        >
          Cancel
        </button>

        <button
          type="button"
          class="rounded-xl bg-blue-600 px-5 py-2 text-xs font-semibold text-white shadow-xs hover:bg-blue-700 active:scale-95 disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer transition-all"
          :disabled="!selectedRole"
          @click="handleSubmit"
        >
          Assign Role
        </button>
      </div>
    </div>
  </div>
</template>
