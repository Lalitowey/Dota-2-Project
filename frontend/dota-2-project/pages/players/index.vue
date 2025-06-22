// pages/players/index.vue
<script setup lang="ts">
useHead({
  title: 'Search Players'
});
</script>
<template>
  <div class="container mx-auto py-8">
    <h1 class="text-2xl font-bold mb-4">Player Search</h1>
    <p>Use the search bar in the navbar to find specific players by their Account ID.</p>
    <p class="mt-2 text-sm text-muted-foreground">
      (This page could later include a list of bookmarked players, featured players, or advanced search filters.)
    </p>
  </div>
</template>