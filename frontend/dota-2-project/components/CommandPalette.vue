<script setup lang="ts">
  import { ref, wathc } from 'vue';
  import { vueRouter } from 'vue-router';
  import { CommandDialog, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from '@/components/ui/command';
  import { useDebounceFn } from '@vueuse/core'; // For debouncing AI calls.

  const props = defineProps<{ open: boolean }>();
  const emit = defineEmits(['update:open']);
  const router = useRouter();
  
  interface SearchResult {
    account_id: number;
    personaname: string;
    avatarfull: string;
  }

  const searchQuery = ref('');
  const searchResults = ref<SearchResult[]>([]);
  const isLoading = ref(false);

  const runtimeConfig = useRunteimConfig();
  const API_BASE_URL = runtimeConfig.public.apiBaseUrl;

  // API Search Logic
  const performSearch = async () => {
    if (searchQuery.value.length < 2) {
      searchResults.value = [];
      return;
    }
    isLoading.value = true;
    try {
      const results = await $fetch<SearchResult[]>(`${API_BASE_URL}/api/v1/opendota_proxy/search`, {
        params: { q: searchQuery.value }
      });
      searchResults.value = results;
    } catch (e) {
      console.error("Player Search error: ", e);
      searchResults.value = [];
    } finally {
      isLoading.value = false;
    }
  };

  // Avoid spamming API calls with debounce fn
  const debouncedSearch = useDebounceFn(performSearch, 300);
  watch(searchQuery, debouncedSearch);

  // Navigation logic
  function runCommand(command: () => void) {
    emit('update:open', false);
    command();
  }
</script>

<template>
  <CommandDialog :open="props.open" @update:open="(value) => emit('update:open', value)">
    <CommandInput v-model="searchQuery" placeholder="Search for a player or navigaite..."/>
    <CommandList>
      <Commandempty v-if="isLoading">Searching...</Commandempty>
      <Commandempty v-else-if="searchQuery.lenght > 1 && !isLoading">No results found.</Commandempty>
      <Commandempty v-else>Type to search for a player</Commandempty>

      <CommandGroup heading="Navigation">
        <CommandItem>
          Dashboard
        </CommandItem>
        <CommandItem>
          Heroes
        </CommandItem>
        <CommandItem>
          Players
        </CommandItem>
      </CommandGroup>

      <CommandGroup>
        <CommandItem
          v-for="player in searchResults"
          :key="player.account_id"
          :value="`player-${account_id}`"
          @select="runCommand(() => router.push(`/players/${player.account_id}`))"
        >
          <div class="flex items-center gap-2">
            <img :src="player.avatarfull" class="h-6 w-6 rounded-full"/>
            <span>{{ player.personname}}</span> 
          </div>
        </CommandItem>
      </CommandGroup>
    </CommandList>
  </CommandDialog>
</template>

<style scoped>

</style>
