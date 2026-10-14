// @ts-check
import withNuxt from './.nuxt/eslint.config.mjs'
import betterTailwindcss from 'eslint-plugin-better-tailwindcss'
import { getDefaultAttributes } from 'eslint-plugin-better-tailwindcss/api/defaults'

export default withNuxt(
  betterTailwindcss.configs['correctness-error'],
  {
    settings: {
      'better-tailwindcss': {
        entryPoint: 'app/assets/css/main.css',
        attributes: [
          ...getDefaultAttributes(),
          ['^v-bind:ui$', [{ match: 'objectValues' }]]
        ]
      }
    }
  },
  {
    // Shell (navbar/sidebar) dijaga persis seperti desain aslinya.
    // Aturan format dimatikan agar tidak perlu merapikan file ini,
    // aturan correctness tetap aktif dengan allowlist sempit.
    files: ['app/components/layout/AppNavbar.vue', 'app/components/layout/AppSidebar.vue'],
    rules: {
      'vue/max-attributes-per-line': 'off',
      'vue/singleline-html-element-content-newline': 'off',
      '@stylistic/arrow-parens': 'off',
      '@typescript-eslint/no-unused-vars': ['error', { varsIgnorePattern: '^_$|^computed$' }],
      'better-tailwindcss/no-unknown-classes': ['error', { ignore: ['^custom-scrollbar$'] }]
    }
  }
)
