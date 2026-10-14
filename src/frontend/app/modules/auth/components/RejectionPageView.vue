<template>
  <AuthShell
    labelledby="rejection-title"
    eyebrow="Access review"
    aside-title="Your workspace access is reviewed by an administrator."
    aside-description="Role requests are evaluated to keep internal data secure and to grant access to the right people only."
    aside-footer="Secure access only"
  >
    <div class="flex flex-col items-center text-center">
      <div
        aria-hidden="true"
        class="flex size-14 items-center justify-center rounded-full bg-rose-50 text-rose-600 ring-1 ring-rose-100"
      >
        <UIcon
          name="i-lucide-shield-x"
          class="size-7"
        />
      </div>

      <span
        class="mt-5 inline-flex items-center gap-1.5 rounded-full border border-rose-200 bg-rose-50 px-3 py-1 text-xs font-semibold text-rose-700"
      >
        <span
          aria-hidden="true"
          class="size-1.5 rounded-full bg-rose-500"
        />
        Rejected
      </span>

      <h1
        id="rejection-title"
        class="mt-4 text-[26px] leading-tight font-semibold tracking-[-0.02em] text-blue-950"
      >
        Role Request Rejected
      </h1>
      <p class="mt-2 text-[15px] leading-relaxed font-medium text-slate-700">
        Your role request has been rejected.
      </p>
      <p class="mt-2 text-sm leading-relaxed text-slate-500">
        Unfortunately, your request for access has not been approved. You can review your request details
        or return to the landing page for further instructions.
      </p>
    </div>

    <div class="mt-6 rounded-xl border border-amber-200 bg-amber-50/70 p-4 text-left">
      <div class="flex items-start gap-2.5">
        <UIcon
          name="i-lucide-info"
          aria-hidden="true"
          class="mt-0.5 size-4 shrink-0 text-amber-600"
        />
        <div class="min-w-0">
          <p class="text-xs font-semibold text-amber-900">
            Reason for rejection
          </p>
          <p
            v-if="reason"
            class="mt-1 text-xs leading-relaxed text-amber-800"
          >
            {{ reason }}
          </p>
          <p
            v-else
            class="mt-1 text-xs leading-relaxed text-amber-800"
          >
            No specific reason was shared by the reviewer. Contact your platform administrator if you need
            more information about this decision.
          </p>
        </div>
      </div>
    </div>

    <div class="mt-6 space-y-2.5">
      <NuxtLink
        to="/landing"
        class="flex h-11 w-full items-center justify-center rounded-xl bg-blue-600 px-5 text-[15px] font-semibold text-white shadow-[0_10px_24px_-12px_rgba(29,78,216,0.7)] transition-colors duration-200 ease-out hover:bg-blue-700 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
      >
        Back to Landing Page
      </NuxtLink>

      <NuxtLink
        v-if="detailsTo"
        :to="detailsTo"
        class="flex h-11 w-full items-center justify-center rounded-xl border border-slate-200 bg-white px-5 text-[15px] font-medium text-blue-950 transition-colors duration-200 ease-out hover:border-blue-300 hover:bg-blue-50 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
      >
        View Request Details
      </NuxtLink>
    </div>

    <p class="mt-5 text-center text-xs leading-relaxed text-slate-400">
      If you believe this decision was made in error or need clarification, please contact your platform
      administrator.
    </p>
  </AuthShell>
</template>

<script setup lang="ts">
import AuthShell from './AuthShell.vue'

withDefaults(defineProps<{
  reason?: string | null
  detailsTo?: string | null
}>(), {
  reason: null,
  detailsTo: null
})
</script>
