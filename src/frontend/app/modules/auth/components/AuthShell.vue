<template>
  <main class="grid min-h-screen lg:grid-cols-[1.05fr_1fr]">
    <aside
      class="relative isolate hidden overflow-hidden bg-linear-to-br from-blue-950 via-blue-900 to-blue-700 p-10 text-white lg:flex lg:flex-col lg:justify-between xl:p-14"
    >
      <div
        aria-hidden="true"
        class="pointer-events-none absolute inset-0 -z-10"
      >
        <div
          class="absolute -top-32 -left-28 size-[28rem] rounded-full bg-blue-500/25 blur-[110px]"
        />
        <div
          class="absolute -right-24 bottom-[-12rem] size-[30rem] rounded-full bg-sky-400/20 blur-[120px]"
        />
        <svg
          viewBox="0 0 400 400"
          fill="none"
          class="absolute -right-40 -bottom-52 size-[34rem] text-white/8"
        >
          <circle
            cx="200"
            cy="200"
            r="196"
            stroke="currentColor"
          />
          <circle
            cx="200"
            cy="200"
            r="150"
            stroke="currentColor"
          />
          <circle
            cx="200"
            cy="200"
            r="104"
            stroke="currentColor"
          />
          <circle
            cx="200"
            cy="200"
            r="58"
            stroke="currentColor"
          />
        </svg>
      </div>

      <div class="flex items-center gap-2.5">
        <span
          aria-hidden="true"
          class="size-2 rounded-full bg-blue-300"
        />
        <span class="text-sm font-semibold tracking-tight">Your Workspace</span>
      </div>

      <div class="max-w-sm">
        <p class="text-xs font-semibold tracking-[0.18em] text-blue-200 uppercase">
          {{ eyebrow }}
        </p>
        <p
          class="mt-4 text-3xl leading-[1.15] font-semibold tracking-tight text-balance text-white xl:text-[2.5rem]"
        >
          {{ asideTitle }}
        </p>
        <p class="mt-5 max-w-xs text-[15px] leading-relaxed text-blue-100/70">
          {{ asideDescription }}
        </p>
      </div>

      <p class="text-xs text-blue-200/60">
        {{ asideFooter }}
      </p>
    </aside>

    <section
      :aria-labelledby="labelledby"
      class="relative isolate flex items-center justify-center overflow-hidden bg-linear-to-b from-blue-900 via-blue-800 to-blue-600 px-5 py-12 sm:px-8 lg:from-blue-50 lg:via-white lg:to-white lg:px-10 xl:px-14"
    >
      <div
        aria-hidden="true"
        class="pointer-events-none absolute inset-0 -z-10 hidden lg:block"
      >
        <div
          class="absolute top-1/2 left-1/2 size-[34rem] -translate-x-1/2 -translate-y-1/2 rounded-full bg-blue-100/70 blur-[100px]"
        />
      </div>

      <div class="w-full max-w-sm">
        <div class="mb-6 flex items-center justify-center gap-2.5 lg:hidden">
          <span
            aria-hidden="true"
            class="size-2 rounded-full bg-blue-200"
          />
          <span class="text-sm font-semibold tracking-tight text-white">Your Workspace</span>
        </div>

        <div
          class="rounded-2xl bg-white p-7 shadow-[0_1px_2px_rgba(15,23,42,0.04),0_12px_32px_-12px_rgba(15,23,42,0.25)] ring-1 ring-slate-900/5 sm:p-8"
        >
          <slot />
        </div>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
const {
  labelledby = 'auth-title',
  eyebrow = 'Single sign-on',
  asideTitle = 'One secure sign-on for your whole workspace.',
  asideDescription = 'Reach every internal tool with the Google account your organization already trusts.',
  asideFooter = 'Authorized access only'
} = defineProps<{
  labelledby?: string
  eyebrow?: string
  asideTitle?: string
  asideDescription?: string
  asideFooter?: string
}>()
</script>
