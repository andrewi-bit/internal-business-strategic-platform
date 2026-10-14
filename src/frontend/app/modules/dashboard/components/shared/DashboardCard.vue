<script setup lang="ts">
interface Props {
  title: string
  subtitle?: string
  padded?: boolean
}

withDefaults(defineProps<Props>(), {
  padded: true
})
</script>

<template>
  <section
    class="flex min-w-0 flex-col overflow-hidden rounded-xl border border-slate-200/80 bg-white shadow-xs"
  >
    <!-- Card Header -->
    <header
      class="flex h-9 shrink-0 items-center justify-between gap-3 border-b border-slate-100 px-4"
    >
      <div class="flex min-w-0 items-baseline gap-2">
        <h2 class="shrink-0 truncate text-xs leading-5 font-bold tracking-tight text-slate-900">
          {{ title }}
        </h2>
        <p
          v-if="subtitle"
          class="min-w-0 truncate text-[11px] leading-4 text-slate-400"
        >
          {{ subtitle }}
        </p>
      </div>

      <div
        v-if="$slots.actions"
        class="shrink-0"
      >
        <slot name="actions" />
      </div>
    </header>

    <!-- Card Body -->
    <div
      class="min-w-0 flex-1 overflow-hidden"
      :class="padded ? 'p-4' : ''"
    >
      <slot />
    </div>
  </section>
</template>
