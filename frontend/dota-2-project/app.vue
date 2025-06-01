// frontend/dota-2-project/app.vue
<template>
  <div>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>

<script setup lang="ts">
// You can add global imports or logic here if absolutely necessary,
// but often it's better to use plugins or composables for global concerns.

// Example: Setting a default page title template (can also be done in nuxt.config.ts)
// import { useHead } from '#imports' // or '@vueuse/head' if you added it
// useHead({
//   titleTemplate: (titleChunk) => {
//     return titleChunk ? `${titleChunk} - Dota 2 Analytics` : 'Dota 2 Analytics';
//   }
// })
</script>

<style>
/* Global styles can go here, but it's often recommended to put them in assets/css/main.css (or similar)
   and import that file in nuxt.config.ts or here.
   shadcn-vue's setup will likely create an `assets/css/globals.css` or similar for Tailwind base styles.
*/
body {
  /* Example: Basic body styling */
  /* font-family: 'Inter', sans-serif; Not needed if Tailwind handles it */
  /* background-color: theme('colors.background'); You'd use Tailwind's theme function */
}
</style>