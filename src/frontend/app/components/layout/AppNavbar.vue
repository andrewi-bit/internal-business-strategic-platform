<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const isDropdownOpen = ref(false)
const dropdownContainer = ref<HTMLElement | null>(null)

// Data profil dummy (dapat disambungkan ke Pinia store nanti)
const userData = ref({
  fullName: 'Roland Brilianto',
  roleTitle: 'Super Admin',
  initials: 'RB',
  unreadCount: 3
})

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value
}

const handleLogout = () => {
  isDropdownOpen.value = false
  navigateTo('/login')
}

// Menutup popup saat klik di luar area dropdown
const onDocumentClick = (event: MouseEvent) => {
  if (dropdownContainer.value && !dropdownContainer.value.contains(event.target as Node)) {
    isDropdownOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', onDocumentClick)
})

onUnmounted(() => {
  document.removeEventListener('click', onDocumentClick)
})
</script>

<template>
  <header
    class="flex h-16 w-full items-center justify-between border-b border-slate-200 bg-white px-6 shadow-xs"
  >
    <!-- Sisi Kiri (Dibiarkan bersih tanpa search bar) -->
    <div class="flex items-center" />

    <!-- Sisi Kanan (Notifikasi & Profil User) -->
    <div class="flex items-center gap-5">
      <!-- Tombol Lonceng Notifikasi -->
      <button
        type="button"
        class="relative flex h-10 w-10 items-center justify-center rounded-full text-slate-600 transition-colors hover:bg-slate-100 cursor-pointer"
        aria-label="Notifications"
      >
        <UIcon name="i-lucide-bell" class="h-5 w-5" />

        <!-- Badge Angka Notifikasi Merah -->
        <span
          v-if="userData.unreadCount > 0"
          class="absolute top-1.5 right-1.5 flex h-4 min-w-4 items-center justify-center rounded-full bg-rose-500 px-1 text-[10px] font-bold text-white ring-2 ring-white"
        >
          {{ userData.unreadCount }}
        </span>
      </button>

      <!-- Divider Vertikal -->
      <div class="h-6 w-px bg-slate-200" />

      <!-- Area Profil & Dropdown Menu -->
      <div ref="dropdownContainer" class="relative">
        <button
          type="button"
          class="flex items-center gap-3 rounded-lg p-1.5 text-left transition-colors hover:bg-slate-50 cursor-pointer"
          @click="toggleDropdown"
        >
          <!-- Avatar Inisial Bulat -->
          <div
            class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-blue-600 text-xs font-bold text-white shadow-xs"
          >
            {{ userData.initials }}
          </div>

          <!-- Nama & Role -->
          <div class="hidden flex-col text-left md:flex">
            <span class="text-sm font-semibold text-slate-800 leading-tight">
              {{ userData.fullName }}
            </span>
            <span class="text-xs text-slate-500 font-medium">
              {{ userData.roleTitle }}
            </span>
          </div>

          <!-- Chevron Icon -->
          <UIcon
            name="i-lucide-chevron-down"
            class="h-4 w-4 text-slate-400 transition-transform duration-200"
            :class="{ 'rotate-180': isDropdownOpen }"
          />
        </button>

        <!-- Menu Dropdown Popup -->
        <div
          v-show="isDropdownOpen"
          class="absolute right-0 mt-2 w-56 rounded-xl border border-slate-200 bg-white p-2 shadow-lg ring-1 ring-black/5 z-50 transition-all"
        >
          <!-- Info Ringkas Mobile -->
          <div class="px-3 py-2 border-b border-slate-100 mb-1 md:hidden">
            <p class="text-sm font-semibold text-slate-800">{{ userData.fullName }}</p>
            <p class="text-xs text-slate-500">{{ userData.roleTitle }}</p>
          </div>

          <!-- Pilihan Menu -->
          <div class="space-y-0.5">
            <NuxtLink
              to="/profile"
              class="flex w-full items-center gap-2.5 rounded-lg px-3 py-2 text-sm font-medium text-slate-700 transition-colors hover:bg-slate-100 cursor-pointer"
              @click="isDropdownOpen = false"
            >
              <UIcon name="i-lucide-user" class="h-4 w-4 text-slate-500" />
              <span>Profile</span>
            </NuxtLink>

            <NuxtLink
              to="/admin/settings"
              class="flex w-full items-center gap-2.5 rounded-lg px-3 py-2 text-sm font-medium text-slate-700 transition-colors hover:bg-slate-100 cursor-pointer"
              @click="isDropdownOpen = false"
            >
              <UIcon name="i-lucide-settings" class="h-4 w-4 text-slate-500" />
              <span>Settings</span>
            </NuxtLink>
          </div>

          <div class="my-1.5 border-t border-slate-100" />

          <!-- Tombol Logout dengan Aksen Merah Tegas -->
          <button
            type="button"
            class="flex w-full items-center gap-2.5 rounded-lg px-3 py-2 text-sm font-semibold text-rose-600 transition-colors hover:bg-rose-50 hover:text-rose-700 cursor-pointer"
            @click="handleLogout"
          >
            <UIcon name="i-lucide-log-out" class="h-4 w-4 text-rose-600" />
            <span>Sign Out</span>
          </button>
        </div>
      </div>
    </div>
  </header>
</template>
