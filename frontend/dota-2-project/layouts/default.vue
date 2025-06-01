<script setup lang="ts">
import sidebar from '@/components/sidebar.vue';
</script>

<template>
  <div class="flex h-screen bg-background">
    <sidebar/>
    <div class="flex-1 flex flex-col overflow-hidden">
      <header class="h-16 border-b flex items-center px-6">
        <h1 class="text-xl font-semibold">Page Title (from Navbar later)</h1>
      </header>
      <main class="flex-1 p-4 md:p-6 lg:p-8 overflow-y-auto">
        <slot/>
      </main>
    </div>
  </div>
</template>