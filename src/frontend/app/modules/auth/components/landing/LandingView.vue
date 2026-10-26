<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

// Import aset gambar dari assets
import heroBg from '~/assets/hero-bg.png'
import heroMockup from '~/assets/hero-dashboard-mockup.png'
import portoCard from '~/assets/porto-card.png'
import partnerCard from '~/assets/partner-card.png'
import collabCard from '~/assets/collab-card.png'
import reportCard from '~/assets/report-card.png'
import requestIllustration from '~/assets/request-role-illustration.png'

import { useAuthStore } from '~/modules/auth/stores/auth.store'
import { useRoleStore } from '~/modules/roles/stores/role.store'
import { useDivisionStore } from '~/modules/divisions/stores/division.store'

const authStore = useAuthStore()
const roleStore = useRoleStore()
const divisionStore = useDivisionStore()

// State Dropdown Profil di Header
const isProfileDropdownOpen = ref(false)
const profileDropdownRef = ref<HTMLElement | null>(null)

const toggleProfileDropdown = () => {
  isProfileDropdownOpen.value = !isProfileDropdownOpen.value
}

const handleLogout = async () => {
  isProfileDropdownOpen.value = false
  await authStore.logout()
}

// Menutup dropdown saat user klik di luar area
const onDocumentClick = (event: MouseEvent) => {
  if (profileDropdownRef.value && !profileDropdownRef.value.contains(event.target as Node)) {
    isProfileDropdownOpen.value = false
  }
}

const toast = useToast()
const isScrolled = ref(false)

const currentUser = computed(() => {
  const u = authStore.user
  const fullName = u?.full_name || 'User'
  const initials =
    fullName
      .split(' ')
      .filter(Boolean)
      .slice(0, 2)
      .map((word: string) => word[0].toUpperCase())
      .join('') || 'U'
  return {
    fullName,
    initials,
    email: u?.email || '',
    roleId: u?.role_id || null
  }
})

// State Section Aktif
const activeSection = ref('home')

// State Form Request Role
const form = ref({
  fullName: '',
  email: '',
  division: '',
  requestedRole: '',
  reason: ''
})

const isSubmitting = ref(false)

const getRoleTheme = (index: number) => {
  const themes = [
    {
      border: 'border-emerald-200/90',
      bgGradient: 'background: linear-gradient(145deg, #ffffff 60%, #e6fbf0 100%)',
      badge: 'bg-emerald-100 text-emerald-700 ring-emerald-200'
    },
    {
      border: 'border-blue-200/90',
      bgGradient: 'background: linear-gradient(145deg, #ffffff 60%, #e8f4fd 100%)',
      badge: 'bg-blue-100 text-blue-700 ring-blue-200'
    },
    {
      border: 'border-purple-200/90',
      bgGradient: 'background: linear-gradient(145deg, #ffffff 60%, #f5f0ff 100%)',
      badge: 'bg-purple-100 text-purple-700 ring-purple-200'
    }
  ]
  return themes[index % themes.length]
}
// =========================================================================
// SMOOTH SCROLL MENGGUNAKAN REQUEST-ANIMATION-FRAME (DIJAMIN MULUS)
// =========================================================================
let animationFrameId: number | null = null

const smoothScrollToPosition = (targetPosition: number, duration = 650) => {
  if (animationFrameId !== null) {
    cancelAnimationFrame(animationFrameId)
  }

  const startPosition = window.scrollY || window.pageYOffset || document.documentElement.scrollTop
  const distance = targetPosition - startPosition

  if (Math.abs(distance) < 2) return

  let startTime: number | null = null

  // Easing easeInOutCubic yang halus dan presisi
  const easeInOutCubic = (t: number) => {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2
  }

  const step = (currentTime: number) => {
    if (startTime === null) startTime = currentTime
    const timeElapsed = currentTime - startTime
    const progress = Math.min(timeElapsed / duration, 1)
    const ease = easeInOutCubic(progress)

    window.scrollTo(0, startPosition + distance * ease)

    if (timeElapsed < duration) {
      animationFrameId = window.requestAnimationFrame(step)
    } else {
      animationFrameId = null
    }
  }

  animationFrameId = window.requestAnimationFrame(step)
}

const scrollToSection = (id: string) => {
  const el = document.getElementById(id)
  if (!el) return

  const navbarHeight = 70
  const elementPosition = el.getBoundingClientRect().top
  const offsetPosition = elementPosition + (window.scrollY || window.pageYOffset) - navbarHeight

  smoothScrollToPosition(offsetPosition, 650)
}

// Scroll Spy: Deteksi section yang sedang aktif
const handleScrollSpy = () => {
  const sections = ['home', 'features', 'role-guide', 'request-role']
  const scrollPosition = window.scrollY + 120

  for (const id of sections) {
    const el = document.getElementById(id)
    if (el) {
      const top = el.offsetTop
      const height = el.offsetHeight
      if (scrollPosition >= top && scrollPosition < top + height) {
        activeSection.value = id
        break
      }
    }
  }
}

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
  handleScrollSpy()
}

onMounted(async () => {
  window.addEventListener('scroll', handleScroll, { passive: true })
  document.addEventListener('click', onDocumentClick)
  handleScroll()

  const userData = await authStore.fetchCurrentUser()
  if (userData) {
    form.value.fullName = userData.full_name
    form.value.email = userData.email
  }
  await Promise.all([roleStore.fetchRoles(), divisionStore.fetchDivisions()])
})

onUnmounted(() => {
  if (animationFrameId !== null) {
    cancelAnimationFrame(animationFrameId)
  }
  window.removeEventListener('scroll', handleScroll)
  document.removeEventListener('click', onDocumentClick)
})

const handleSubmitRequest = () => {
  if (!form.value.division || !form.value.requestedRole || !form.value.reason) {
    toast.add({
      title: 'Incomplete Form',
      description: 'Please fill in all required fields.',
      color: 'error'
    })
    return
  }

  isSubmitting.value = true
  setTimeout(() => {
    isSubmitting.value = false
    toast.add({
      title: 'Request Submitted',
      description: 'Your role request has been submitted to the Super Admin.',
      color: 'success'
    })
    form.value.division = ''
    form.value.requestedRole = ''
    form.value.reason = ''
  }, 700)
}
</script>

<template>
  <div
    class="relative min-h-screen bg-white font-sans text-slate-800 antialiased selection:bg-blue-600 selection:text-white"
  >
    <!-- ========================================================================= -->
    <!-- 1. ROOT LEVEL FIXED NAVBAR (Z-INDEX 100 - SELALU MUNCUL SAAT DI-SCROLL)  -->
    <!-- ========================================================================= -->
    <header
      class="fixed top-0 left-0 right-0 z-[100] w-full transition-all duration-300 ease-in-out"
      :class="[
        isScrolled
          ? 'h-16 shadow-lg shadow-black/15 border-b border-white/10 backdrop-blur-md'
          : 'h-20 bg-transparent border-b border-transparent'
      ]"
      :style="isScrolled ? { backgroundColor: 'rgba(7, 19, 48, 0.92)' } : {}"
    >
      <div class="mx-auto flex h-full max-w-[1140px] items-center justify-between px-6 text-white">
        <!-- Logo B Company -->
        <div class="flex items-center gap-3 cursor-pointer" @click="scrollToSection('home')">
          <div
            class="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-600 font-extrabold text-white text-base shadow-md ring-1 ring-white/20"
          >
            B
          </div>
          <span class="text-lg font-bold tracking-tight text-white">IBSP</span>
        </div>

        <!-- Navigation Links Tengah -->
        <nav class="hidden md:flex items-center gap-8 text-[13px] font-medium">
          <!-- Home -->
          <button
            type="button"
            class="relative py-2 transition-colors cursor-pointer"
            :class="
              activeSection === 'home'
                ? 'text-white font-semibold'
                : 'text-blue-100/80 hover:text-white'
            "
            @click="scrollToSection('home')"
          >
            Home
            <span
              v-if="activeSection === 'home'"
              class="absolute bottom-0 left-0 right-0 h-0.5 bg-white rounded-full transition-all"
            />
          </button>

          <!-- Features -->
          <button
            type="button"
            class="relative py-2 transition-colors cursor-pointer"
            :class="
              activeSection === 'features'
                ? 'text-white font-semibold'
                : 'text-blue-100/80 hover:text-white'
            "
            @click="scrollToSection('features')"
          >
            Features
            <span
              v-if="activeSection === 'features'"
              class="absolute bottom-0 left-0 right-0 h-0.5 bg-white rounded-full transition-all"
            />
          </button>

          <!-- Role Guide -->
          <button
            type="button"
            class="relative py-2 transition-colors cursor-pointer"
            :class="
              activeSection === 'role-guide'
                ? 'text-white font-semibold'
                : 'text-blue-100/80 hover:text-white'
            "
            @click="scrollToSection('role-guide')"
          >
            Role Guide
            <span
              v-if="activeSection === 'role-guide'"
              class="absolute bottom-0 left-0 right-0 h-0.5 bg-white rounded-full transition-all"
            />
          </button>

          <!-- Request Role -->
          <button
            type="button"
            class="relative py-2 transition-colors cursor-pointer"
            :class="
              activeSection === 'request-role'
                ? 'text-white font-semibold'
                : 'text-blue-100/80 hover:text-white'
            "
            @click="scrollToSection('request-role')"
          >
            Request Role
            <span
              v-if="activeSection === 'request-role'"
              class="absolute bottom-0 left-0 right-0 h-0.5 bg-white rounded-full transition-all"
            />
          </button>
        </nav>

        <!-- Right Action: Profile User & Dropdown -->
        <div ref="profileDropdownRef" class="relative">
          <button
            type="button"
            class="flex items-center gap-2.5 rounded-full p-1 sm:px-2.5 sm:py-1 transition-all cursor-pointer hover:bg-white/10"
            @click="toggleProfileDropdown"
          >
            <div
              class="flex h-8.5 w-8.5 items-center justify-center rounded-full bg-blue-600 text-xs font-bold text-white ring-2 ring-white/20 shadow-xs"
            >
              {{ currentUser.initials }}
            </div>
            <div class="hidden sm:flex flex-col text-left">
              <span class="text-[13px] font-semibold text-white leading-tight">
                {{ currentUser.fullName }}
              </span>
              <span class="text-[11px] text-blue-200 font-medium"> Tidak Ada Role </span>
            </div>
            <UIcon
              name="i-lucide-chevron-down"
              class="h-3.5 w-3.5 text-blue-200 transition-transform duration-200 ml-0.5"
              :class="{ 'rotate-180': isProfileDropdownOpen }"
            />
          </button>

          <!-- Dropdown Menu Popup -->
          <div
            v-show="isProfileDropdownOpen"
            class="absolute right-0 mt-2.5 w-56 rounded-2xl border border-slate-100 bg-white p-2 text-slate-800 shadow-xl ring-1 ring-black/5 z-50 transition-all duration-150"
          >
            <!-- Header Profil di dalam Dropdown -->
            <div class="px-3 py-2.5 border-b border-slate-100">
              <p class="text-xs font-semibold text-slate-900 leading-snug">
                {{ currentUser.fullName }}
              </p>
              <p class="text-[11px] text-slate-500 truncate">
                {{ currentUser.email }}
              </p>
              <div class="mt-1 flex items-center gap-1.5">
                <span
                  class="inline-flex items-center rounded-full bg-blue-50 px-2 py-0.5 text-[10px] font-semibold text-blue-700 ring-1 ring-blue-700/10"
                >
                  Tidak ada Role
                </span>
              </div>
            </div>

            <div class="my-1 border-t border-slate-100" />

            <!-- Tombol Logout -->
            <button
              type="button"
              class="flex w-full items-center gap-2.5 rounded-xl px-3 py-2 text-xs font-semibold text-rose-600 transition-colors hover:bg-rose-50 hover:text-rose-700 cursor-pointer"
              @click="handleLogout"
            >
              <UIcon name="i-lucide-log-out" class="h-4 w-4 text-rose-500" />
              <span>Log out</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- ============================================================ -->
    <!-- 2. HERO SECTION                                              -->
    <!-- ============================================================ -->
    <div
      id="home"
      class="relative w-full bg-cover bg-center overflow-hidden"
      :style="{ backgroundImage: `url(${heroBg})`, backgroundColor: '#0B4FD8' }"
    >
      <section class="pt-28 pb-16 lg:pt-32 lg:pb-24 px-6 mx-auto max-w-[1140px]">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          <!-- Left Hero Text -->
          <div class="lg:col-span-5 space-y-5 text-white z-10">
            <p class="text-[11px] font-extrabold tracking-[0.2em] text-blue-200 uppercase">
              INTERNAL PLATFORM
            </p>

            <h1
              class="text-3xl font-extrabold tracking-tight sm:text-4xl lg:text-[42px] leading-[1.15] text-white"
            >
              Drive Strategic Partnerships,<br />
              Create Greater Impact
            </h1>

            <p class="max-w-md text-xs sm:text-[13px] text-blue-100/90 leading-relaxed font-normal">
              Explore our portfolio, manage strategic partnerships, and collaborate across the
              organization — all in one platform.
            </p>

            <div class="pt-2">
              <button
                type="button"
                class="inline-flex items-center gap-2.5 rounded-xl bg-white px-5 py-2.5 text-[13px] font-bold text-[#155EEF] shadow-xl shadow-blue-900/30 transition-all hover:bg-blue-50 active:scale-95 cursor-pointer"
                @click="scrollToSection('request-role')"
              >
                <span>Request Access</span>
                <UIcon name="i-lucide-arrow-right" class="h-4 w-4 stroke-[2.5]" />
              </button>
            </div>
          </div>

          <!-- Right Hero Mockup -->
          <div class="lg:col-span-7 flex justify-center lg:justify-end">
            <img
              :src="heroMockup"
              alt="Dashboard Preview Mockup"
              class="w-full max-w-[620px] drop-shadow-[0_25px_50px_rgba(0,18,70,0.5)] transition-transform duration-300 hover:scale-[1.01]"
            />
          </div>
        </div>
      </section>
    </div>

    <!-- ========================================================================= -->
    <!-- 3. KEY FEATURES (BACKGROUND & AURA ORIGINAL TETAP DIPERTAHANKAN)          -->
    <!-- ========================================================================= -->
    <section id="features" class="relative overflow-hidden py-20 px-6 bg-[#FAFBFD]">
      <!-- Background Aurora Mesh yang Berani dan Ketara (z-0 agar tidak tenggelam) -->
      <div aria-hidden="true" class="pointer-events-none absolute inset-0 z-0 overflow-hidden">
        <!-- Blueprint Grid Interaktif Halus -->
        <div
          class="absolute inset-0 opacity-[0.25]"
          style="
            background-image:
              linear-gradient(to right, #94a3b8 1px, transparent 1px),
              linear-gradient(to bottom, #94a3b8 1px, transparent 1px);
            background-size: 40px 40px;
            mask-image: radial-gradient(ellipse 75% 65% at 50% 50%, #000 50%, transparent 100%);
          "
        />

        <!-- Bola Cahaya 1: UNGU NEON Menyala di Kiri Atas -->
        <div
          class="absolute -top-32 -left-20 h-[36rem] w-[36rem] rounded-full bg-violet-500/20 blur-[130px]"
        />

        <!-- Bola Cahaya 2: HIJAU ZAMRUD Menyala di Kanan Tengah -->
        <div
          class="absolute top-1/4 -right-24 h-[32rem] w-[32rem] rounded-full bg-emerald-400/25 blur-[120px]"
        />

        <!-- Bola Cahaya 3: BIRU CYAN Elektrik di Bawah Tengah -->
        <div
          class="absolute -bottom-28 left-1/3 h-[30rem] w-[30rem] rounded-full bg-cyan-400/25 blur-[110px]"
        />
      </div>

      <div class="mx-auto max-w-[1140px] space-y-10 relative z-10">
        <!-- Header Key Features -->
        <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div class="space-y-2">
            <div
              class="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-emerald-500/10 px-3 py-1 text-[11px] font-extrabold tracking-wider text-[#1570EF] uppercase ring-1 ring-blue-500/20 backdrop-blur-xs"
            >
              <span
                class="size-2 rounded-full bg-gradient-to-r from-blue-600 to-violet-600 animate-pulse"
              />
              <span>KEY FEATURES</span>
            </div>
            <h2
              class="text-2xl sm:text-[28px] font-extrabold tracking-tight text-slate-900 leading-tight"
            >
              Everything you need to manage<br />
              <span
                class="bg-gradient-to-r from-blue-600 via-indigo-600 to-violet-600 bg-clip-text text-transparent"
              >
                portfolio and partnerships
              </span>
            </h2>
            <p class="text-xs sm:text-[13px] text-slate-600 max-w-xl leading-relaxed font-normal">
              A centralized platform designed to improve collaboration, visibility, and strategic
              decision-making across the organization.
            </p>
          </div>
        </div>

        <!-- 4 Cards Grid dengan Glow Ambient Card Berwarna -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5.5">
          <!-- Card 1: Portfolio Management (Aksen Biru Elektrik) -->
          <div
            class="group flex flex-col justify-between rounded-2xl border border-blue-100 bg-white/90 backdrop-blur-md p-5 shadow-[0_8px_25px_-6px_rgba(37,99,235,0.08)] hover:shadow-[0_16px_35px_-8px_rgba(37,99,235,0.2)] hover:border-blue-400 transition-all duration-300"
          >
            <div class="space-y-3.5">
              <div
                class="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-blue-600 ring-1 ring-blue-200 group-hover:scale-110 group-hover:bg-blue-600 group-hover:text-white transition-all shadow-xs"
              >
                <UIcon name="i-lucide-folder" class="h-5 w-5" />
              </div>
              <div>
                <h3
                  class="text-sm font-bold text-slate-900 group-hover:text-blue-600 transition-colors"
                >
                  Portfolio Management
                </h3>
                <p class="mt-1 text-[11px] text-slate-500 leading-relaxed">
                  View and explore ongoing and completed projects across the company.
                </p>
              </div>
            </div>
            <div
              class="mt-4 overflow-hidden rounded-xl border border-slate-100 bg-white shadow-2xs group-hover:border-blue-200 transition-colors"
            >
              <img
                :src="portoCard"
                alt="Portfolio Management Preview"
                class="w-full object-cover group-hover:scale-[1.02] transition-transform duration-300"
              />
            </div>
          </div>

          <!-- Card 2: Partnership Directory (Aksen Ungu Lilac Neon) -->
          <div
            class="group flex flex-col justify-between rounded-2xl border border-purple-100 bg-white/90 backdrop-blur-md p-5 shadow-[0_8px_25px_-6px_rgba(147,51,234,0.08)] hover:shadow-[0_16px_35px_-8px_rgba(147,51,234,0.2)] hover:border-purple-400 transition-all duration-300"
          >
            <div class="space-y-3.5">
              <div
                class="flex h-10 w-10 items-center justify-center rounded-xl bg-purple-50 text-purple-600 ring-1 ring-purple-200 group-hover:scale-110 group-hover:bg-purple-600 group-hover:text-white transition-all shadow-xs"
              >
                <UIcon name="i-lucide-handshake" class="h-5 w-5" />
              </div>
              <div>
                <h3
                  class="text-sm font-bold text-slate-900 group-hover:text-purple-600 transition-colors"
                >
                  Partnership Directory
                </h3>
                <p class="mt-1 text-[11px] text-slate-500 leading-relaxed">
                  Discover strategic partners and their key information in one place.
                </p>
              </div>
            </div>
            <div
              class="mt-4 overflow-hidden rounded-xl border border-slate-100 bg-white shadow-2xs group-hover:border-purple-200 transition-colors"
            >
              <img
                :src="partnerCard"
                alt="Partnership Directory Preview"
                class="w-full object-cover group-hover:scale-[1.02] transition-transform duration-300"
              />
            </div>
          </div>

          <!-- Card 3: Collaboration History (Aksen Hijau Zamrud) -->
          <div
            class="group flex flex-col justify-between rounded-2xl border border-emerald-100 bg-white/90 backdrop-blur-md p-5 shadow-[0_8px_25px_-6px_rgba(16,185,129,0.08)] hover:shadow-[0_16px_35px_-8px_rgba(16,185,129,0.2)] hover:border-emerald-400 transition-all duration-300"
          >
            <div class="space-y-3.5">
              <div
                class="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600 ring-1 ring-emerald-200 group-hover:scale-110 group-hover:bg-emerald-600 group-hover:text-white transition-all shadow-xs"
              >
                <UIcon name="i-lucide-git-commit-horizontal" class="h-5 w-5" />
              </div>
              <div>
                <h3
                  class="text-sm font-bold text-slate-900 group-hover:text-emerald-600 transition-colors"
                >
                  Collaboration History
                </h3>
                <p class="mt-1 text-[11px] text-slate-500 leading-relaxed">
                  Track partnership activities, milestones, and co-marketing enablement.
                </p>
              </div>
            </div>
            <div
              class="mt-4 overflow-hidden rounded-xl border border-slate-100 bg-white shadow-2xs group-hover:border-emerald-200 transition-colors"
            >
              <img
                :src="collabCard"
                alt="Collaboration History Preview"
                class="w-full object-cover group-hover:scale-[1.02] transition-transform duration-300"
              />
            </div>
          </div>

          <!-- Card 4: Insightful Reporting (Aksen Amber Warm) -->
          <div
            class="group flex flex-col justify-between rounded-2xl border border-amber-100 bg-white/90 backdrop-blur-md p-5 shadow-[0_8px_25px_-6px_rgba(245,158,11,0.08)] hover:shadow-[0_16px_35px_-8px_rgba(245,158,11,0.2)] hover:border-amber-400 transition-all duration-300"
          >
            <div class="space-y-3.5">
              <div
                class="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-50 text-amber-600 ring-1 ring-amber-200 group-hover:scale-110 group-hover:bg-amber-600 group-hover:text-white transition-all shadow-xs"
              >
                <UIcon name="i-lucide-bar-chart-3" class="h-5 w-5" />
              </div>
              <div>
                <h3
                  class="text-sm font-bold text-slate-900 group-hover:text-amber-600 transition-colors"
                >
                  Insightful Reporting
                </h3>
                <p class="mt-1 text-[11px] text-slate-500 leading-relaxed">
                  Access key data and visualizations to support strategic decisions.
                </p>
              </div>
            </div>
            <div
              class="mt-4 overflow-hidden rounded-xl border border-slate-100 bg-white shadow-2xs group-hover:border-amber-200 transition-colors"
            >
              <img
                :src="reportCard"
                alt="Insightful Reporting Preview"
                class="w-full object-cover group-hover:scale-[1.02] transition-transform duration-300"
              />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ============================================================ -->
    <!-- 4. ROLE OVERVIEW SECTION                                     -->
    <!-- ============================================================ -->
    <section
      id="role-guide"
      class="relative overflow-hidden py-16 px-6 bg-[#F8FAFC] border-y border-slate-200/60"
    >
      <div class="mx-auto max-w-[1140px] space-y-8 relative z-10">
        <div>
          <div
            class="inline-flex items-center gap-2 rounded-full bg-blue-50/80 px-2.5 py-1 text-[11px] font-extrabold tracking-wider text-[#1570EF] uppercase ring-1 ring-blue-100"
          >
            <span class="size-1.5 rounded-full bg-[#1570EF]" />
            <span>ROLE OVERVIEW</span>
          </div>
          <h2
            class="text-2xl sm:text-[26px] font-bold tracking-tight text-slate-900 leading-tight mt-2"
          >
            Choose the right role for your needs
          </h2>
          <p class="text-xs sm:text-[13px] text-slate-500 max-w-xl mt-1.5 leading-relaxed">
            Each role provides different access and capabilities to support your work in the
            platform. Select the role that best fits your responsibilities.
          </p>
        </div>

        <!-- Dynamic Role Cards Grid -->
        <!-- Skeleton saat loading -->
        <div v-if="roleStore.isLoading" class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div
            v-for="n in 3"
            :key="n"
            class="h-44 rounded-2xl border border-slate-200 bg-slate-50/60 p-6 animate-pulse"
          />
        </div>

        <!-- Render data dari API -->
        <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div
            v-for="(role, index) in roleStore.roles"
            :key="role.id"
            class="relative overflow-hidden rounded-2xl border p-6 shadow-sm space-y-3.5 bg-white transition-all hover:shadow-md hover:-translate-y-0.5"
            :class="getRoleTheme(index).border"
            :style="getRoleTheme(index).bgGradient"
          >
            <div class="flex items-center gap-3">
              <div
                class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl ring-1"
                :class="getRoleTheme(index).badge"
              >
                <UIcon name="i-lucide-user" class="h-5 w-5" />
              </div>
              <h3 class="text-sm font-bold text-slate-900 leading-snug">
                {{ role.name }}
              </h3>
            </div>
            <p class="text-xs text-slate-600 leading-relaxed font-normal">
              {{ role.description }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- ========================================================================= -->
    <!-- 5. REQUEST ACCESS (BACKGROUND & AURA ORIGINAL TETAP DIPERTAHANKAN)        -->
    <!-- ========================================================================= -->
    <section
      id="request-role"
      class="relative overflow-hidden py-20 px-6 bg-gradient-to-b from-white via-[#F8FBFF] to-white"
    >
      <!-- Background Ambient Aura Menyala: Ungu, Hijau, Biru (z-0 agar tidak tertutup) -->
      <div aria-hidden="true" class="pointer-events-none absolute inset-0 z-0 overflow-hidden">
        <!-- Dot Texture yang tegas -->
        <div
          class="absolute inset-0 opacity-[0.3]"
          style="
            background-image: radial-gradient(#64748b 1px, transparent 1px);
            background-size: 28px 28px;
            mask-image: radial-gradient(ellipse 65% 55% at 50% 50%, #000 60%, transparent 100%);
          "
        />

        <!-- Orb 1: UNGU VIOLET Menyala di Balik Ilustrasi Kiri -->
        <div
          class="absolute top-1/2 left-1/4 -translate-x-1/2 -translate-y-1/2 h-[32rem] w-[32rem] rounded-full bg-gradient-to-tr from-violet-500/25 to-blue-500/25 blur-[120px]"
        />

        <!-- Orb 2: HIJAU MINT Menyala di Kanan Atas Form -->
        <div
          class="absolute top-10 right-10 h-[28rem] w-[28rem] rounded-full bg-emerald-400/25 blur-[120px]"
        />

        <!-- Orb 3: BIRU ROYAL Menyala di Kanan Bawah Form -->
        <div
          class="absolute -bottom-10 right-1/4 h-[26rem] w-[26rem] rounded-full bg-blue-500/20 blur-[110px]"
        />

        <!-- SVG Concentric Radar Rings Berwarna Cyan Tipis -->
        <svg
          viewBox="0 0 500 500"
          fill="none"
          class="absolute -right-20 -bottom-20 size-[32rem] text-cyan-500/15"
        >
          <circle cx="250" cy="250" r="230" stroke="currentColor" stroke-width="1.5" />
          <circle cx="250" cy="250" r="170" stroke="currentColor" stroke-width="1.5" />
          <circle cx="250" cy="250" r="110" stroke="currentColor" stroke-width="1.5" />
          <circle cx="250" cy="250" r="50" stroke="currentColor" stroke-width="1.5" />
        </svg>
      </div>

      <div class="mx-auto max-w-[1020px] space-y-8 relative z-10">
        <div>
          <div
            class="inline-flex items-center gap-2 rounded-full bg-linear-to-r from-blue-500/10 via-purple-500/10 to-emerald-500/10 px-3 py-1 text-[11px] font-extrabold tracking-wider text-[#1570EF] uppercase ring-1 ring-blue-500/20 backdrop-blur-xs"
          >
            <span
              class="size-2 rounded-full bg-gradient-to-r from-emerald-500 to-blue-500 animate-pulse"
            />
            <span>REQUEST ACCESS</span>
          </div>
          <h2
            class="text-2xl sm:text-[28px] font-extrabold tracking-tight text-slate-900 leading-tight mt-2"
          >
            Request a Role
          </h2>
          <p class="text-xs sm:text-[13px] text-slate-600 mt-1 leading-relaxed">
            Fill in the form below to request access to the platform. Your request will be reviewed
            by the Super Admin.
          </p>
        </div>

        <!-- 2 Kolom Padat & Kompak Berdampingan -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          <!-- Sisi Kiri: Ilustrasi Form + Teks Pendamping -->
          <div
            class="lg:col-span-5 flex flex-col items-center justify-center text-center px-4 space-y-4"
          >
            <div class="relative">
              <div
                class="absolute -inset-4 rounded-full bg-gradient-to-r from-violet-500/30 to-blue-500/30 blur-2xl"
              />
              <img
                :src="requestIllustration"
                alt="Request Role Document Illustration"
                class="relative w-full max-w-[270px] drop-shadow-xl transition-transform duration-300 hover:scale-[1.03]"
              />
            </div>
            <p class="text-xs font-semibold text-slate-600 max-w-[250px] leading-relaxed">
              Gain access to the right resources and start contributing to strategic initiatives.
            </p>
          </div>

          <!-- Sisi Kanan: Form Card Kompak -->
          <div
            class="lg:col-span-7 rounded-2xl border border-white/80 bg-white/95 backdrop-blur-md p-6.5 sm:p-7.5 shadow-[0_12px_40px_-10px_rgba(37,99,235,0.12)] ring-1 ring-slate-200/80"
          >
            <form class="space-y-4.5" @submit.prevent="handleSubmitRequest">
              <!-- Section: Your Information -->
              <div class="space-y-2.5">
                <div class="flex items-center gap-2 text-xs font-bold text-slate-900">
                  <UIcon name="i-lucide-user" class="h-4 w-4 text-[#155EEF]" />
                  <span>Your Information</span>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <!-- Full Name (Readonly) -->
                  <div>
                    <label class="block text-[11px] font-semibold text-slate-700 mb-1"
                      >Full Name</label
                    >
                    <input
                      v-model="form.fullName"
                      type="text"
                      readonly
                      class="h-9 w-full rounded-lg border border-slate-200 bg-[#F9FAFB] px-3 text-xs font-medium text-slate-600 outline-none cursor-not-allowed"
                    />
                  </div>

                  <!-- Email (Readonly) -->
                  <div>
                    <label class="block text-[11px] font-semibold text-slate-700 mb-1">Email</label>
                    <input
                      v-model="form.email"
                      type="email"
                      readonly
                      class="h-9 w-full rounded-lg border border-slate-200 bg-[#F9FAFB] px-3 text-xs font-medium text-slate-600 outline-none cursor-not-allowed"
                    />
                  </div>
                </div>

                <!-- Division Select -->
                <div>
                  <label class="block text-[11px] font-semibold text-slate-700 mb-1"
                    >Division</label
                  >
                  <select
                    v-model="form.division"
                    class="h-9 w-full rounded-lg border border-slate-200 bg-white px-3 text-xs text-slate-800 shadow-2xs outline-none focus:border-[#155EEF] focus:ring-1 focus:ring-[#155EEF] cursor-pointer disabled:bg-slate-50 disabled:opacity-70"
                    :disabled="divisionStore.isLoading"
                  >
                    <option value="" disabled selected>
                      {{
                        divisionStore.isLoading ? 'Loading divisions...' : 'Select your division'
                      }}
                    </option>
                    <option v-for="div in divisionStore.divisions" :key="div.id" :value="div.id">
                      {{ div.name }}
                    </option>
                  </select>
                </div>
              </div>

              <!-- Section: Role Request -->
              <div class="space-y-2.5 border-t border-slate-100 pt-3.5">
                <div class="flex items-center gap-2 text-xs font-bold text-slate-900">
                  <UIcon name="i-lucide-briefcase" class="h-4 w-4 text-[#155EEF]" />
                  <span>Role Request</span>
                </div>

                <div>
                  <label class="block text-[11px] font-semibold text-slate-700 mb-1"
                    >Requested Role</label
                  >
                  <select
                    v-model="form.requestedRole"
                    class="h-9 w-full rounded-lg border border-slate-200 bg-white px-3 text-xs text-slate-800 shadow-2xs outline-none focus:border-[#155EEF] focus:ring-1 focus:ring-[#155EEF] cursor-pointer"
                  >
                    <option value="" disabled selected>Select the role you want to request</option>
                    <option v-for="role in roleStore.roles" :key="role.id" :value="role.id">
                      {{ role.name }}
                    </option>
                  </select>
                </div>
              </div>

              <!-- Section: Request Reason -->
              <div class="space-y-2 border-t border-slate-100 pt-3.5">
                <div class="flex items-center gap-2 text-xs font-bold text-slate-900">
                  <UIcon name="i-lucide-message-square" class="h-4 w-4 text-[#155EEF]" />
                  <span>Request Reason</span>
                </div>

                <p class="text-[11px] text-slate-400">
                  Please provide a clear reason for requesting this role.
                </p>

                <textarea
                  v-model="form.reason"
                  rows="3"
                  maxlength="500"
                  placeholder="Type your reason here..."
                  class="w-full rounded-xl border border-slate-200 bg-white p-3 text-xs text-slate-800 placeholder-slate-400 outline-none focus:border-[#155EEF] focus:ring-1 focus:ring-[#155EEF]"
                />

                <div class="flex justify-end text-[10px] text-slate-400">
                  {{ form.reason.length }}/500
                </div>
              </div>

              <!-- Submit Button -->
              <div class="flex justify-end pt-1">
                <button
                  type="submit"
                  :disabled="isSubmitting"
                  class="inline-flex h-9.5 items-center gap-2 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 px-6 text-xs font-bold text-white shadow-lg shadow-blue-500/30 transition-all hover:from-blue-700 hover:to-indigo-700 active:scale-95 disabled:opacity-50 cursor-pointer"
                >
                  <UIcon
                    v-if="isSubmitting"
                    name="i-lucide-loader-circle"
                    class="h-3.5 w-3.5 animate-spin"
                  />
                  <UIcon v-else name="i-lucide-send" class="h-3.5 w-3.5" />
                  <span>Submit Request</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </section>

    <!-- ============================================================ -->
    <!-- 6. FOOTER                                                    -->
    <!-- ============================================================ -->
    <footer class="py-14 px-6 text-white" style="background-color: #071330">
      <div class="mx-auto max-w-[1140px] grid grid-cols-1 md:grid-cols-12 gap-10">
        <!-- Brand Info -->
        <div class="md:col-span-5 space-y-3.5">
          <div class="flex items-center gap-3">
            <div
              class="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-600 font-extrabold text-white text-base shadow-md ring-1 ring-white/20"
            >
              B
            </div>
            <span class="text-lg font-bold tracking-tight text-white">IBSP</span>
          </div>
          <p class="text-xs text-slate-400 max-w-sm leading-relaxed">
            Internal Portfolio &amp; Partnership Management Platform.<br />
            Driving collaboration for a stronger, more connected future.
          </p>
        </div>

        <!-- Quick Links -->
        <div class="md:col-span-3 space-y-3 text-xs">
          <p class="font-bold text-white tracking-wide text-sm">Quick Links</p>
          <ul class="space-y-2.5 text-slate-400">
            <li>
              <button
                type="button"
                class="hover:text-white transition-colors cursor-pointer"
                @click="scrollToSection('home')"
              >
                Home
              </button>
            </li>
            <li>
              <button
                type="button"
                class="hover:text-white transition-colors cursor-pointer"
                @click="scrollToSection('features')"
              >
                Features
              </button>
            </li>
            <li>
              <button
                type="button"
                class="hover:text-white transition-colors cursor-pointer"
                @click="scrollToSection('role-guide')"
              >
                Role Guide
              </button>
            </li>
            <li>
              <button
                type="button"
                class="hover:text-white transition-colors cursor-pointer"
                @click="scrollToSection('request-role')"
              >
                Request Role
              </button>
            </li>
          </ul>
        </div>

        <!-- Support Info -->
        <div class="md:col-span-4 space-y-3 text-xs">
          <p class="font-bold text-white tracking-wide text-sm">Support</p>
          <ul class="space-y-2.5 text-slate-400">
            <li class="flex items-center gap-2.5">
              <UIcon name="i-lucide-life-buoy" class="h-4 w-4 text-[#2E90FA]" />
              <a href="#" class="hover:text-white transition-colors">Help Center</a>
            </li>
            <li class="flex items-center gap-2.5">
              <UIcon name="i-lucide-headset" class="h-4 w-4 text-[#2E90FA]" />
              <a href="#" class="hover:text-white transition-colors">Contact Support</a>
            </li>
            <li class="flex items-center gap-2.5">
              <UIcon name="i-lucide-mail" class="h-4 w-4 text-[#2E90FA]" />
              <span class="text-slate-300">it-support@company.com</span>
            </li>
            <li class="flex items-center gap-2.5">
              <UIcon name="i-lucide-file-text" class="h-4 w-4 text-[#2E90FA]" />
              <a href="#" class="hover:text-white transition-colors">Terms of Use</a>
            </li>
            <li class="flex items-center gap-2.5">
              <UIcon name="i-lucide-shield-alert" class="h-4 w-4 text-[#2E90FA]" />
              <a href="#" class="hover:text-white transition-colors">Privacy Policy</a>
            </li>
          </ul>
        </div>
      </div>

      <div
        class="mx-auto max-w-[1140px] border-t border-white/10 mt-10 pt-6 text-xs text-slate-500"
      >
        &copy; 2026 Bangunindo. All rights reserved.
      </div>
    </footer>
  </div>
</template>
