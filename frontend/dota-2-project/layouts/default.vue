<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import { onKeyStroke } from '@vueuse/core';
import sidebar from '@/components/sidebar.vue';
import AppNavbar from '@/components/AppNavbar.vue';
import CommandPalette from '@/components/CommandPalette.vue'

const open = ref(false); // Command palette open state
const router = useRouter(); // Router instance

// Open command palette with Ctrl+K or Cmd+K
onKeyStroke(['k'], (e) => {
  if (e.ctrlKey || e.metaKey) { // if Ctrl or Cmd is pressed
    e.preventDefault(); // Prevent default behavior
    open.value = !open.value; // Toggle command palette
  }
});
// Press Escape to close command palette
onKeyStroke('Escape', (e) => { // onKeyStroke for Escape key
  if (open.value) { // Only close if open
    e.preventDefault();
    open.value = false; // Close the command palette
  }
});

// Keystrokes to navigate to dashboard, heroes, and players
onKeyStroke (['g', 'd'], () => { router.push ('/'); });
onKeyStroke (['g', 'h'], () => { router.push ('/heroes'); });
onKeyStroke (['g', 'p'], () => { router.push ('/players'); });
onKeyStroke (['/'], () => { // if searching by ID, focus on search input
  const searchInput = document.getElementById('navbar-search-input'); // Get the search input element by ID
  if(searchInput) { // Ensure the element exists
    searchInput.focus(); // Focus on the search input
  }
})

</script>

<template>
  <div>
    <CommandPalette v-model:open="open"/>
    <div class="flex h-screen bg-background">
      <sidebar/>
      <div class="flex-1 flex flex-col overflow-hidden">
        <AppNavbar/>
        <main class="flex-1 p-4 md:p-6 lg:p-8 overflow-y-auto">
          <slot/>
        </main>
      </div>
    </div>
  </div>
</template>
