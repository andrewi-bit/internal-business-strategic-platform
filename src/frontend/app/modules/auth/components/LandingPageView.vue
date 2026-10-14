<template>
  <AuthShell
    labelledby="landing-title"
    eyebrow="Welcome"
    aside-title="Request access to the tools your team relies on."
    aside-description="Every role is granted after a short review so that internal data stays available to the right people."
    aside-footer="Access by request only"
  >
    <div class="flex flex-col items-center text-center">
      <div
        aria-hidden="true"
        class="flex size-14 items-center justify-center rounded-full bg-blue-50 text-blue-600 ring-1 ring-blue-100"
      >
        <UIcon
          name="i-lucide-user-check"
          class="size-7"
        />
      </div>

      <h1
        id="landing-title"
        class="mt-5 text-[26px] leading-tight font-semibold tracking-[-0.02em] text-blue-950"
      >
        Welcome to the platform
      </h1>
      <p class="mt-2 text-[15px] leading-relaxed font-medium text-slate-700">
        Your account does not have a role assigned yet.
      </p>
      <p class="mt-2 text-sm leading-relaxed text-slate-500">
        Request a role to access the dashboards. An administrator will review your request and notify you
        once a decision is made.
      </p>
    </div>

    <p
      v-if="formMessage"
      class="mt-6 rounded-xl bg-blue-50 px-3.5 py-2.5 text-xs font-medium text-blue-700"
      role="status"
    >
      {{ formMessage }}
    </p>

    <div class="mt-6 space-y-2.5">
      <button
        type="button"
        class="flex h-11 w-full cursor-pointer items-center justify-center rounded-xl bg-blue-600 px-5 text-[15px] font-semibold text-white shadow-[0_10px_24px_-12px_rgba(29,78,216,0.7)] transition-colors duration-200 ease-out hover:bg-blue-700 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
        @click="handleRequestRole"
      >
        Request Role
      </button>

      <NuxtLink
        to="/login"
        class="flex h-11 w-full items-center justify-center rounded-xl border border-slate-200 bg-white px-5 text-[15px] font-medium text-blue-950 transition-colors duration-200 ease-out hover:border-blue-300 hover:bg-blue-50 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
      >
        Back to Login
      </NuxtLink>
    </div>

    <p class="mt-5 text-center text-xs leading-relaxed text-slate-400">
      If you think you should already have access, please contact your platform administrator.
    </p>
  </AuthShell>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AuthShell from './AuthShell.vue'

const formMessage = ref('')

const handleRequestRole = () => {
  formMessage.value = 'Role requests are not connected to the review service yet. Wire this action to the backend request-role endpoint to enable it.'
}
</script>
