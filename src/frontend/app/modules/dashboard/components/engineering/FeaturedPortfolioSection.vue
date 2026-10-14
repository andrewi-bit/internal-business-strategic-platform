<script setup lang="ts">
const featuredProjects = [
  {
    id: 1,
    title: 'Digital Banking Transformation',
    category: 'Banking',
    status: 'Completed',
    statusClass: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    duration: '12 months',
    roi: '32% ROI',
    client: 'PT ABC',
    image:
      'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=400&auto=format&fit=crop'
  },
  {
    id: 2,
    title: 'Smart Manufacturing Platform',
    category: 'Manufacturing',
    status: 'On Going',
    statusClass: 'bg-amber-50 text-amber-700 border-amber-200',
    duration: '18 months',
    roi: '24% ROI',
    client: 'PT XYZ',
    image:
      'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?q=80&w=400&auto=format&fit=crop'
  },
  {
    id: 3,
    title: 'Retail Analytics Platform',
    category: 'Retail',
    status: 'Active',
    statusClass: 'bg-blue-50 text-blue-700 border-blue-200',
    duration: '9 months',
    roi: '28% ROI',
    client: 'PT Retail Indo',
    image:
      'https://images.unsplash.com/photo-1555421689-491a97ff2040?q=80&w=400&auto=format&fit=crop'
  },
  {
    id: 4,
    title: 'Renewable Energy Dashboard',
    category: 'Energy',
    status: 'On Going',
    statusClass: 'bg-amber-50 text-amber-700 border-amber-200',
    duration: '14 months',
    roi: '18% ROI',
    client: 'PT Green Energy',
    image:
      'https://images.unsplash.com/photo-1466611653911-95081537e5b7?q=80&w=400&auto=format&fit=crop'
  }
]
</script>

<template>
  <div class="space-y-2">
    <!-- Section Header -->
    <div class="flex items-center justify-between">
      <h2 class="text-xs font-bold text-slate-900 tracking-tight">Featured Portfolio</h2>

      <!-- Tombol View All -->
      <NuxtLink
        to="/portofolio"
        class="text-xs font-semibold text-blue-600 transition-colors hover:text-blue-700 cursor-pointer"
      >
        View All
      </NuxtLink>
    </div>

    <!-- 4 Projects Cards Grid (Semua Card Bisa Di-klik) -->
    <div class="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">
      <NuxtLink
        v-for="item in featuredProjects"
        :key="item.id"
        to="/portofolio"
        class="group flex flex-col justify-between overflow-hidden rounded-xl border border-slate-200/80 bg-white p-3 shadow-2xs transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md hover:border-blue-200 cursor-pointer"
      >
        <!-- Top Info with Thumbnail -->
        <div class="flex gap-2.5">
          <img
            :src="item.image"
            :alt="item.title"
            class="h-14 w-14 shrink-0 rounded-lg object-cover"
            loading="lazy"
          />

          <div class="flex-1 min-w-0">
            <h3
              class="text-xs font-bold text-slate-900 truncate group-hover:text-blue-600 transition-colors"
            >
              {{ item.title }}
            </h3>
            <p class="text-[11px] text-slate-400">
              {{ item.category }}
            </p>
            <div class="mt-1">
              <span
                class="inline-flex items-center rounded-full border px-2 py-0.2 text-[10px] font-semibold"
                :class="item.statusClass"
              >
                ● {{ item.status }}
              </span>
            </div>
          </div>
        </div>

        <!-- Bottom Meta: Duration, ROI, Client -->
        <div
          class="mt-3 flex items-center justify-between border-t border-slate-100 pt-2 text-[10px] text-slate-500 font-medium"
        >
          <div class="flex items-center gap-1">
            <UIcon name="i-lucide-calendar" class="h-3 w-3 text-slate-400" />
            <span>{{ item.duration }}</span>
          </div>

          <div class="flex items-center gap-1">
            <UIcon name="i-lucide-trending-up" class="h-3 w-3 text-slate-400" />
            <span>{{ item.roi }}</span>
          </div>

          <div class="flex items-center gap-1 truncate max-w-[85px]">
            <UIcon name="i-lucide-building" class="h-3 w-3 text-slate-400 shrink-0" />
            <span class="truncate">{{ item.client }}</span>
          </div>
        </div>
      </NuxtLink>
    </div>
  </div>
</template>
