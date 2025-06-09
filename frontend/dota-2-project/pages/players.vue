<script setup lang="ts">
const playerStats = ref({
  name: 'Player',
  gpm: 500,
  xpm: 450,
  winRate: 55,
  mostPlayedHeroes: [
    { name: 'Phantom Assassin', games: 20, winRate: 60 },
    { name: 'Invoker', games: 15, winRate: 50 },
    { name: 'Puck', games: 10, winRate: 70 }
  ]
});
</script>

<template>
<h1>
  Player Page
</h1>
</template>

<style scoped>

</style>