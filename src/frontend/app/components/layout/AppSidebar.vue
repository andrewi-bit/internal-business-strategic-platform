<script setup lang="ts">
import { ref, computed, watchEffect } from 'vue'

interface SubMenuItem {
  label: string
  to: string
}

interface MenuItem {
  key?: string
  label: string
  icon: string
  to?: string
  badge?: string | number
  children?: SubMenuItem[]
}

interface NavigationSection {
  title?: string
  items: MenuItem[]
}

const route = useRoute()

// 1. Data Navigation Schema (Single Source of Truth)
const navigationSections: NavigationSection[] = [
  {
    items: [
      {
        label: 'Dashboard',
        icon: 'i-lucide-layout-dashboard',
        to: '/dashboard'
      },
      {
        key: 'portfolio',
        label: 'Portfolio',
        icon: 'i-lucide-briefcase',
        children: [
          { label: 'Portfolio Directory', to: '/portofolio' },
          { label: 'My Projects', to: '/portofolio/my-projects' }
        ]
      },
      {
        key: 'partnership',
        label: 'Partnership',
        icon: 'i-lucide-handshake',
        children: [
          { label: 'Partner Directory', to: '/partnership' },
          { label: 'Verification', to: '/partnership/verification' },
          { label: 'Evaluation', to: '/partnership/evaluation' }
        ]
      },
      {
        label: 'Analytics',
        icon: 'i-lucide-line-chart',
        to: '/analytics'
      },
      {
        label: 'Notifications',
        icon: 'i-lucide-bell',
        to: '/notifications',
        badge: 3
      }
    ]
  },
  {
    title: 'Administration',
    items: [
      {
        label: 'Content Management',
        icon: 'i-lucide-file-text',
        to: '/admin/content'
      },
      {
        label: 'User Management',
        icon: 'i-lucide-users',
        to: '/admin/users'
      },
      {
        label: 'Audit Log',
        icon: 'i-lucide-history',
        to: '/admin/audit-log'
      },
      {
        label: 'Settings',
        icon: 'i-lucide-settings',
        to: '/admin/settings'
      }
    ]
  }
]

// 2. Generic Helper: Cek apakah route saat ini adalah child dari sebuah menu
const isChildActive = (children?: SubMenuItem[]): boolean => {
  if (!children) return false
  return children.some((child) => route.path === child.to || route.path.startsWith(`${child.to}/`))
}

// 3. State Menu Terbuka (Dikelola Dinamis)
const openMenus = ref<Record<string, boolean>>({})

const toggleMenu = (key: string) => {
  openMenus.value[key] = !openMenus.value[key]
}

// 4. Auto-sync State: Buka dropdown secara reaktif jika salah satu child aktif
watchEffect(() => {
  navigationSections.forEach((section) => {
    section.items.forEach((item) => {
      if (item.key && item.children && isChildActive(item.children)) {
        openMenus.value[item.key] = true
      }
    })
  })
})
</script>

<template>
  <aside
    class="flex h-screen w-64 shrink-0 flex-col border-r border-slate-800 bg-[#0B132B] text-slate-300 select-none"
  >
    <!-- Header / Brand Logo -->
    <div class="flex h-16 items-center gap-3 px-6 border-b border-slate-800/80">
      <div
        class="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-600 text-white shadow-lg shadow-blue-500/30"
      >
        <UIcon name="i-lucide-box" class="h-5 w-5" />
      </div>
      <span class="text-base font-semibold text-white tracking-wide">Company</span>
    </div>

    <!-- Navigation List (Scrollable Area) -->
    <div class="flex-1 overflow-y-auto px-3 py-4 space-y-6 custom-scrollbar">
      <div v-for="(section, secIdx) in navigationSections" :key="secIdx" class="space-y-2">
        <!-- Section Header (Optional) -->
        <p
          v-if="section.title"
          class="px-3 text-[11px] font-semibold uppercase tracking-wider text-slate-400"
        >
          {{ section.title }}
        </p>

        <!-- Menu Items Loop -->
        <nav class="space-y-1">
          <template v-for="item in section.items" :key="item.label">
            <!-- 1. Menu dengan Dropdown (Accordion) -->
            <div v-if="item.children" class="space-y-1">
              <button
                type="button"
                class="flex w-full items-center justify-between rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-150 cursor-pointer hover:bg-slate-800/60 hover:text-white"
                :class="[
                  isChildActive(item.children)
                    ? 'bg-blue-600/15 text-blue-400 font-semibold'
                    : 'text-slate-400'
                ]"
                @click="item.key && toggleMenu(item.key)"
              >
                <div class="flex items-center gap-3">
                  <UIcon :name="item.icon" class="h-5 w-5 shrink-0" />
                  <span>{{ item.label }}</span>
                </div>
                <UIcon
                  name="i-lucide-chevron-down"
                  class="h-4 w-4 transition-transform duration-200"
                  :class="{ 'rotate-180': item.key && openMenus[item.key] }"
                />
              </button>

              <!-- Sub-menu Items -->
              <div
                v-show="item.key && openMenus[item.key]"
                class="pl-9 pr-1 py-1 space-y-1 border-l border-slate-800 ml-5"
              >
                <NuxtLink
                  v-for="sub in item.children"
                  :key="sub.to"
                  :to="sub.to"
                  exact-active-class="bg-blue-600 text-white font-semibold shadow-xs"
                  class="flex items-center rounded-md px-3 py-2 text-xs font-medium text-slate-400 transition-all cursor-pointer hover:bg-slate-800/80 hover:text-white"
                >
                  {{ sub.label }}
                </NuxtLink>
              </div>
            </div>

            <!-- 2. Single Menu Link -->
            <NuxtLink
              v-else
              :to="item.to!"
              exact-active-class="bg-blue-600 text-white font-semibold shadow-xs"
              class="flex items-center justify-between rounded-lg px-3 py-2.5 text-sm font-medium text-slate-400 transition-all duration-150 cursor-pointer hover:bg-slate-800/60 hover:text-white"
            >
              <div class="flex items-center gap-3">
                <UIcon :name="item.icon" class="h-5 w-5 shrink-0" />
                <span>{{ item.label }}</span>
              </div>

              <!-- Badge -->
              <span
                v-if="item.badge"
                class="flex h-5 min-w-5 items-center justify-center rounded-full bg-rose-500 px-1.5 text-[10px] font-bold text-white shadow-xs"
              >
                {{ item.badge }}
              </span>
            </NuxtLink>
          </template>
        </nav>
      </div>
    </div>
  </aside>
</template>
