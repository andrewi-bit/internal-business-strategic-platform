// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [
    '@nuxt/eslint',
    '@nuxt/ui',
    '@pinia/nuxt',
    'nuxt-echarts'
  ],

  devtools: {
    enabled: true
  },

  css: ['~/assets/css/main.css'],

  routeRules: {
    '/': { prerender: true, redirect: '/login' }
  },

  compatibilityDate: '2026-06-30',

  echarts: {
    renderer: 'canvas',
    charts: ['LineChart', 'BarChart', 'PieChart', 'FunnelChart'],
    components: [
      'GridComponent',
      'TooltipComponent',
      'LegendComponent',
      'TitleComponent',
      'DatasetComponent',
      'MarkLineComponent'
    ],
    features: ['LabelLayout']
  },

  eslint: {
    config: {
      stylistic: {
        commaDangle: 'never',
        braceStyle: '1tbs'
      }
    }
  }
})
