// frontend/dota-2-project/components/AppSidebar.vue
<script setup lang="ts">
// Import NuxtLink for navigation
// import { NuxtLink } from '#components'; // Nuxt auto-imports components, but explicit can be clearer

import { Button } from '@/components/ui/button';

// Import icons from lucide-vue-next
import { LayoutDashboard, Users, Swords /* Add other icons as needed */ } from 'lucide-vue-next';

// Define your navigation items for Dota 2
const navItems = [
  { label: 'Dashboard', path: '/', icon: LayoutDashboard }, // Assuming '/' is your main dashboard
  { label: 'Players', path: '/players', icon: Users },
  { label: 'heroes', path: '/heroes', icon: Swords },
];
</script>

<template>
  <div class="w-64 h-screen bg-background border-r p-4 flex flex-col">
    <!-- 1. Branding -->
    <div class="mb-8">
      <NuxtLink to="/" class="flex items-center space-x-2">
        <!-- You can replace 'Swords' with a proper logo component or SVG later -->
        <Swords class="h-8 w-8 text-primary" />
        <h1 class="text-xl font-bold text-foreground">Dota 2 Analytics</h1>
      </NuxtLink>
    </div>

    <!-- 2. Navigation Links -->
    <nav class="flex-grow">
      <ul>
        <li v-for="item in navItems" :key="item.path" class="mb-2">
          <NuxtLink :to="item.path" custom v-slot="{ navigate, isActive, href }">
            <Button
              :variant="isActive ? 'secondary' : 'ghost'"
              class="w-full justify-start text-left h-10 px-3"
              @click="navigate"
              as="a"
              :href="href"
            >
              <component :is="item.icon" class="h-5 w-5 mr-3" />
              <span>{{ item.label }}</span>
            </Button>
          </NuxtLink>
        </li>
      </ul>
    </nav>

    <!-- 3. Footer (Simplified) -->
    <div class="mt-auto pt-4 border-t">
      <p class="text-xs text-muted-foreground text-center">
        © {{ new Date().getFullYear() }} Dota 2 Project
      </p>
    </div>
  </div>
</template>

<style scoped>
/* Add any sidebar-specific styles if needed, but try to use Tailwind utilities */
</style>