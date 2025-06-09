// https://nuxt.com/docs/api/configuration/nuxt-config

import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2025-05-15',
  devtools: { enabled: true },
  css: ['@/assets/css/tailwind.css'],

  vite: {
    plugins: [
        tailwindcss(),
    ],
  },

  modules: ['shadcn-nuxt', '@pinia/nuxt', '@nuxtjs/color-mode', "@nuxtjs/color-mode"],

  colorMode: {
    classSuffix: '',
  },

  shadcn: {
    /**
     * Prefix for all the imported component
     */
    prefix: '',
    /**
     * Directory that the component lives in.
     * @default "./components/ui"
     */
    componentDir: './components/ui'
  },
})