<template>
  <div class="space-y-1.5">
    <label
      :for="id"
      class="block text-sm font-medium text-blue-950"
    >
      {{ label }}
    </label>

    <div class="relative">
      <input
        :id="id"
        :type="inputType"
        :value="modelValue"
        :placeholder="placeholder"
        :autocomplete="autocomplete"
        :aria-invalid="Boolean(error)"
        :aria-describedby="describedBy"
        class="h-11 w-full rounded-xl border bg-white px-3.5 text-[15px] text-blue-950 shadow-sm transition-[border-color,box-shadow] duration-200 ease-out outline-none placeholder:text-slate-400 focus:ring-2"
        :class="inputClasses"
        @input="handleInput"
      >
      <button
        v-if="isPassword"
        type="button"
        class="absolute inset-y-0 right-0 flex w-11 items-center justify-center rounded-r-xl text-slate-400 transition-colors hover:text-blue-600 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
        :aria-label="revealed ? 'Hide password' : 'Show password'"
        :aria-pressed="revealed"
        @click="revealed = !revealed"
      >
        <UIcon
          :name="revealed ? 'i-lucide-eye-off' : 'i-lucide-eye'"
          aria-hidden="true"
          class="size-5"
        />
      </button>
    </div>

    <p
      v-if="error"
      :id="`${id}-error`"
      class="text-xs font-medium text-rose-600"
    >
      {{ error }}
    </p>
    <p
      v-else-if="hint"
      :id="`${id}-hint`"
      class="text-xs text-slate-400"
    >
      {{ hint }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

const props = withDefaults(defineProps<{
  id: string
  label: string
  modelValue: string
  type?: 'text' | 'email' | 'password'
  placeholder?: string
  autocomplete?: string
  error?: string
  hint?: string
}>(), {
  type: 'text',
  placeholder: '',
  error: '',
  hint: ''
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

const revealed = ref(false)

const isPassword = computed(() => props.type === 'password')

const inputType = computed(() => {
  if (isPassword.value && revealed.value) return 'text'
  return props.type
})

const describedBy = computed(() => {
  if (props.error) return `${props.id}-error`
  if (props.hint) return `${props.id}-hint`
  return undefined
})

const inputClasses = computed(() => {
  if (props.error) {
    return 'border-rose-300 focus:border-rose-500 focus:ring-rose-500/20'
  }
  return 'border-slate-200 focus:border-blue-500 focus:ring-blue-500/20'
})

const handleInput = (event: Event) => {
  emit('update:modelValue', (event.target as HTMLInputElement).value)
}
</script>
