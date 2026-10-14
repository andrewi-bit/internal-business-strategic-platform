<script setup lang="ts">
import type { PartnerDetailItem, ContactType } from '../../../types/detail.types'

interface Props {
  partner: PartnerDetailItem
}

defineProps<Props>()

const emit = defineEmits<{
  (e: 'edit-info'): void
  (e: 'edit-description'): void
  (e: 'edit-logo'): void
  (e: 'add-contact'): void
  (e: 'edit-expertise'): void
}>()

// Helper warna badge tipe kontak (Primary = Hijau, Technical = Biru, Commercial = Ungu)
const getContactBadgeClass = (type: ContactType) => {
  switch (type) {
    case 'Primary':
      return 'bg-emerald-50 text-emerald-700 border-emerald-200'
    case 'Technical':
      return 'bg-blue-50 text-blue-700 border-blue-200'
    case 'Commercial':
      return 'bg-purple-50 text-purple-700 border-purple-200'
    default:
      return 'bg-slate-50 text-slate-700 border-slate-200'
  }
}
</script>

<template>
  <div class="space-y-3.5">
    <!-- 1. Top Row: 3 Cards Grid -->
    <div class="grid grid-cols-1 gap-3.5 lg:grid-cols-12 items-stretch">
      <!-- Card 1: Company Information (5 Kolom) -->
      <div
        class="flex flex-col justify-between rounded-xl border border-slate-200/80 bg-white p-4 shadow-2xs space-y-3 lg:col-span-5"
      >
        <div class="flex items-center justify-between border-b border-slate-100 pb-2.5">
          <h2 class="text-xs font-bold text-slate-900 tracking-tight">Company Information</h2>
          <button
            type="button"
            class="inline-flex items-center gap-1 rounded-md border border-slate-200 bg-white px-2 py-0.5 text-[11px] font-semibold text-slate-700 shadow-2xs hover:bg-slate-50 cursor-pointer"
            @click="emit('edit-info')"
          >
            <UIcon name="i-lucide-edit" class="h-3 w-3 text-slate-500" />
            <span>Edit</span>
          </button>
        </div>

        <div class="space-y-2.5 text-xs flex-1">
          <div class="grid grid-cols-3 gap-2">
            <span class="text-slate-400 font-medium">Company Name</span>
            <span class="col-span-2 font-semibold text-slate-800">{{ partner.legalName }}</span>
          </div>

          <div class="grid grid-cols-3 gap-2">
            <span class="text-slate-400 font-medium">Website</span>
            <a
              :href="partner.companyOverview.website"
              target="_blank"
              class="col-span-2 inline-flex items-center gap-1 font-semibold text-blue-600 hover:underline"
            >
              <span>{{ partner.companyOverview.website }}</span>
              <UIcon name="i-lucide-external-link" class="h-3 w-3" />
            </a>
          </div>

          <div class="grid grid-cols-3 gap-2">
            <span class="text-slate-400 font-medium">Headquarters</span>
            <span class="col-span-2 font-medium text-slate-700">{{
              partner.companyOverview.headquarters
            }}</span>
          </div>

          <div class="grid grid-cols-3 gap-2">
            <span class="text-slate-400 font-medium">Industry</span>
            <span class="col-span-2 font-semibold text-slate-800">{{
              partner.companyOverview.industry
            }}</span>
          </div>

          <div class="grid grid-cols-3 gap-2">
            <span class="text-slate-400 font-medium">Business Focus</span>
            <span class="col-span-2 font-medium text-slate-700">{{
              partner.companyOverview.businessFocus
            }}</span>
          </div>

          <div class="grid grid-cols-3 gap-2 items-center">
            <span class="text-slate-400 font-medium">Key Markets</span>
            <div class="col-span-2 flex flex-wrap gap-1">
              <span
                v-for="market in partner.companyOverview.keyMarkets"
                :key="market"
                class="rounded-md bg-slate-100 px-2 py-0.5 text-[10px] font-semibold text-slate-600"
              >
                {{ market }}
              </span>
              <span
                class="rounded-md bg-slate-100 px-2 py-0.5 text-[10px] font-semibold text-slate-500"
              >
                +1
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Card 2: Company Description (4 Kolom) -->
      <div
        class="flex flex-col rounded-xl border border-slate-200/80 bg-white p-4 shadow-2xs space-y-3 lg:col-span-4"
      >
        <div class="flex items-center justify-between border-b border-slate-100 pb-2.5">
          <h2 class="text-xs font-bold text-slate-900 tracking-tight">Company Description</h2>
          <button
            type="button"
            class="inline-flex items-center gap-1 rounded-md border border-slate-200 bg-white px-2 py-0.5 text-[11px] font-semibold text-slate-700 shadow-2xs hover:bg-slate-50 cursor-pointer"
            @click="emit('edit-description')"
          >
            <UIcon name="i-lucide-edit" class="h-3 w-3 text-slate-500" />
            <span>Edit</span>
          </button>
        </div>

        <p class="text-xs leading-relaxed text-slate-600 flex-1">
          {{ partner.companyOverview.description }}
        </p>
      </div>

      <!-- Card 3: Company Logo (3 Kolom) -->
      <div
        class="flex flex-col justify-between rounded-xl border border-slate-200/80 bg-white p-4 shadow-2xs space-y-3 lg:col-span-3"
      >
        <div class="flex items-center justify-between border-b border-slate-100 pb-2.5">
          <h2 class="text-xs font-bold text-slate-900 tracking-tight">Company Logo</h2>
          <button
            type="button"
            class="inline-flex items-center gap-1 rounded-md border border-slate-200 bg-white px-2 py-0.5 text-[11px] font-semibold text-slate-700 shadow-2xs hover:bg-slate-50 cursor-pointer"
            @click="emit('edit-logo')"
          >
            <UIcon name="i-lucide-edit" class="h-3 w-3 text-slate-500" />
            <span>Edit</span>
          </button>
        </div>

        <!-- Logo Preview -->
        <div class="flex flex-col items-center justify-center p-2 text-center flex-1">
          <img :src="partner.logo" :alt="partner.name" class="h-16 w-auto object-contain" />
          <p class="mt-2 text-xs font-bold text-slate-800">
            {{ partner.name }}
          </p>
        </div>

        <!-- Subtext Info -->
        <div class="border-t border-slate-100 pt-2 text-[10px] text-slate-400 text-center">
          <p>Recommended size 512 × 512 px</p>
          <p>Format: PNG, JPG (Max 2MB)</p>
        </div>
      </div>
    </div>

    <!-- 2. Middle Row: Key Contacts Table -->
    <div class="rounded-xl border border-slate-200/80 bg-white p-4 shadow-2xs space-y-3">
      <div class="flex items-center justify-between border-b border-slate-100 pb-2.5">
        <h2 class="text-xs font-bold text-slate-900 tracking-tight">Key Contacts</h2>
        <button
          type="button"
          class="inline-flex items-center gap-1.5 rounded-lg bg-blue-600 px-2.5 py-1 text-xs font-semibold text-white shadow-2xs hover:bg-blue-700 cursor-pointer"
          @click="emit('add-contact')"
        >
          <UIcon name="i-lucide-plus" class="h-3.5 w-3.5" />
          <span>Add Contact</span>
        </button>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs">
          <thead class="border-b border-slate-100 text-[11px] font-bold text-slate-400">
            <tr>
              <th class="py-2 pr-4">Name</th>
              <th class="px-4 py-2">Position</th>
              <th class="px-4 py-2">Email</th>
              <th class="px-4 py-2">Phone</th>
              <th class="px-4 py-2">Type</th>
              <th class="py-2 pl-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 font-medium">
            <tr
              v-for="contact in partner.keyContacts"
              :key="contact.id"
              class="hover:bg-slate-50/60"
            >
              <!-- Name with Initials Avatar -->
              <td class="py-2.5 pr-4 whitespace-nowrap">
                <div class="flex items-center gap-2.5">
                  <div
                    class="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-slate-100 text-[10px] font-bold text-slate-700"
                  >
                    {{ contact.initials }}
                  </div>
                  <span class="font-bold text-slate-900">{{ contact.name }}</span>
                </div>
              </td>

              <!-- Position -->
              <td class="px-4 py-2.5 text-slate-600 whitespace-nowrap">
                {{ contact.position }}
              </td>

              <!-- Email -->
              <td class="px-4 py-2.5 whitespace-nowrap">
                <a :href="`mailto:${contact.email}`" class="text-blue-600 hover:underline">
                  {{ contact.email }}
                </a>
              </td>

              <!-- Phone -->
              <td class="px-4 py-2.5 text-slate-600 whitespace-nowrap">
                {{ contact.phone }}
              </td>

              <!-- Type Badge -->
              <td class="px-4 py-2.5 whitespace-nowrap">
                <span
                  class="rounded-full border px-2 py-0.2 text-[10px] font-semibold"
                  :class="getContactBadgeClass(contact.type)"
                >
                  {{ contact.type }}
                </span>
              </td>

              <!-- Action Menu -->
              <td class="py-2.5 pl-4 text-right whitespace-nowrap">
                <button
                  type="button"
                  class="inline-flex h-6 w-6 items-center justify-center rounded-md text-slate-400 hover:bg-slate-100 hover:text-slate-700 cursor-pointer"
                  aria-label="Actions"
                >
                  <UIcon name="i-lucide-more-vertical" class="h-3.5 w-3.5" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 3. Bottom Row: Expertise / Solutions -->
    <div class="rounded-xl border border-slate-200/80 bg-white p-4 shadow-2xs space-y-3">
      <div class="flex items-center justify-between border-b border-slate-100 pb-2.5">
        <h2 class="text-xs font-bold text-slate-900 tracking-tight">Expertise / Solutions</h2>
        <button
          type="button"
          class="inline-flex items-center gap-1 rounded-md border border-slate-200 bg-white px-2 py-0.5 text-[11px] font-semibold text-slate-700 shadow-2xs hover:bg-slate-50 cursor-pointer"
          @click="emit('edit-expertise')"
        >
          <UIcon name="i-lucide-edit" class="h-3 w-3 text-slate-500" />
          <span>Edit</span>
        </button>
      </div>

      <div class="flex flex-wrap gap-2">
        <div
          v-for="exp in partner.keyExpertise"
          :key="exp.name"
          class="inline-flex items-center gap-2 rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs font-bold text-slate-700 shadow-2xs"
        >
          <UIcon :name="exp.icon" class="h-3.5 w-3.5 text-blue-600" />
          <span>{{ exp.name }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
