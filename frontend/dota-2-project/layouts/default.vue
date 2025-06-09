<script setup lang="ts">
import sidebar from '@/components/sidebar.vue';
import AppNavbar from '@/components/AppNavbar.vue';
</script>

<template>
  <div class="flex h-screen bg-background">
    <sidebar/>
    <div class="flex-1 flex flex-col overflow-hidden">

      <AppNavbar/>
      <main class="flex-1 p-4 md:p-6 lg:p-8 overflow-y-auto">
        <slot/>
      </main>
    </div>
  </div>
</template>