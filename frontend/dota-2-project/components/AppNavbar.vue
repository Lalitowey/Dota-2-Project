// components/AppNavbar.vue
<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip'; // For icons
import { Search, Moon, Sun, Github } from 'lucide-vue-next';


const colorMode = useColorMode();

const toggleTheme = () => {
  colorMode.preference = colorMode.value === 'dark' ? 'light' : 'dark';
};

const router = useRouter();
const route = useRoute(); // To get current route for page title
const searchQuery = ref('');

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push(`/players/${searchQuery.value.trim()}`);
    searchQuery.value = '';
  }
};

// Dynamic Page Title
const pageTitle = computed(() => {
  if (route.name) {
    // 'index' -> 'Dashboard', 'players-id' -> 'Player Profile'
    const name = String(route.name);
    if (name === 'index') return 'Dashboard';
    if (name.startsWith('players-id')) return 'Player Profile';
    if (name.startsWith('heroes-id')) return 'Hero Details';
    if (name.startsWith('players')) return 'Players';
    if (name.startsWith('heroes')) return 'Heroes';
    // Capitalize first letter of the route name's first segment
    const segments = name.split('-');
    return segments[0].charAt(0).toUpperCase() + segments[0].slice(1);
  }
  return 'Dota 2 Analytics'; // Default
});
</script>

<template>
  <header class="h-16 border-b bg-background flex items-center px-4 md:px-6 sticky top-0 z-30">
    <div class="flex-1">
      <h1 class="text-lg font-semibold text-foreground">{{ pageTitle }}</h1>
    </div>


<!--    <div class="flex-1 flex justify-center">-->
<!--      <form @submit.prevent="handleSearch" class="relative w-full max-w-md">-->
<!--        <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />-->
<!--        <Input-->
<!--          v-model="searchQuery"-->
<!--          type="search"-->
<!--          placeholder="Search Player by Account ID..."-->
<!--          class="pl-10 w-full h-9"-->
<!--        />-->
<!--      </form>-->
<!--    </div>-->


    <div class="flex-1 flex justify-end items-center gap-2">
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger as-child>
            <Button variant="ghost" size="icon" @click="toggleTheme">
              <Sun class="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
              <Moon class="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
              <span class="sr-only">Toggle theme</span>
            </Button>
          </TooltipTrigger>
          <TooltipContent>
            <p>Toggle Theme</p>
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>

      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger as-child>
            <a href="https://github.com/Lalitowey/Dota-2-Project" target="_blank" rel="noopener noreferrer">
              <Button variant="ghost" size="icon">
                <Github class="h-5 w-5" />
                <span class="sr-only">GitHub Repository</span>
              </Button>
            </a>
          </TooltipTrigger>
          <TooltipContent>
            <p>View on GitHub</p>
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>
    </div>
  </header>
</template>