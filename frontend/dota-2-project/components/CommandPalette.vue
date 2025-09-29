<script setup lang="ts">
  import { ref, watch, computed } from 'vue';
  import { useRouter } from 'vue-router';
  import { CommandDialog, CommandEmpty, CommandGroup, CommandItem, CommandList, CommandShortcut } from '@/components/ui/command';
  import { Search } from 'lucide-vue-next';
  import { useDebounceFn } from '@vueuse/core'; // For debouncing AI calls.

  const props = defineProps<{ open: boolean }>();
  const emit = defineEmits(['update:open']);
  const router = useRouter();
  
  interface SearchResult { // Matches OpenDota search result structure
    account_id: number;
    personaname: string;
    avatarfull: string;
  }

  interface DisplayResult { // For displaying in the command palette
    type: 'player' | 'id';
    id: number;
    name: string;
    avatar?: string;
  }

  const searchQuery = ref('');
  const searchResults = ref<DisplayResult[]>([]); // Results to display
  const isLoading = ref(false);
  const searchError = ref<string | null>(null);

  const runtimeConfig = useRuntimeConfig();
  const API_BASE_URL = runtimeConfig.public.apiBaseUrl;

  const isAccountId = computed(() => {
    return /^\d{3,}$/.test(searchQuery.value); // 3 digits or more likely to be account ID
  })

  // API Search Logic
  const performSearch = async (query: string) => {
    console.log("Performing search for: ", query);
    isLoading.value = true;
    searchError.value = null;

    try {
      const results = await $fetch<SearchResult[]>(`${API_BASE_URL}/api/v1/opendota_proxy/search`, {
        params: { q: query }
      });

      console.log("Search results: ", results);

      searchResults.value = results.map(player => ({ 
        type: 'player',
        id: player.account_id,
        name: player.personaname,
        avatar: player.avatarfull
      }));

    } catch (e: any) {
      console.error("Search API error: ", e);
      searchError.value = e.data?.message || e.message || 'An error occurred while searching';
      searchResults.value = [];
    } finally {
      isLoading.value = false;
    }
  };

  // Avoid spamming API calls with debounce fn
  const debouncedSearch = useDebounceFn(performSearch, 300);

  // Watch for changes in searchQuery
  watch(searchQuery, (newQuery) => {
    searchResults.value = [];
    searchError.value = null;

    if (newQuery.trim() === '') { // Clear state if query is empty
      isLoading.value = false;
      searchResults.value = [];
    } else if (isAccountId.value) { // Directly navigate if it's an account ID
      isLoading.value = false;
      searchResults.value = [{
        type: 'id',
        id: parseInt(newQuery, 10),
        name: `Account ID: ${newQuery}`
      }];
    } else if (newQuery.length > 1) { // Only search if query length > 1
      debouncedSearch(newQuery);
    } else { 
      isLoading.value = false;
      searchResults.value = [];
    }
  });

  // Navigation logic
  function runCommand(command: () => void) {
    emit('update:open', false);
    command();
  }
</script>

<template>
  <CommandDialog :open="props.open" @update:open="(value) => emit('update:open', value)">
    <div class="flex h-12 items-center gap-2 border-b px-3">
      <Search class="size-4 shrink-0 opacity-50" />
      <input
        v-model="searchQuery" 
        placeholder="Search for a player or navigate.."
        class="flex h-12 w-full rounded-md bg-transparent py-3 text-sm outline-hidden disabled:cursor-not-allowed disabled:opacity-50 placeholder:text-muted-foreground"
        auto-focus
      />
    </div>
    <CommandList>
      
      <CommandEmpty v-if="isLoading">Searching for "{{ searchQuery }}"...</CommandEmpty>
      <CommandEmpty v-else-if="searchError">{{ searchError }}</CommandEmpty>
      <CommandEmpty v-else-if="searchQuery.length > 1 && !isLoading && searchResults.length === 0">No players found for "{{ searchQuery }}"</CommandEmpty>
      <CommandEmpty v-else-if="searchQuery.length === 0">Type to search for a player by name or ID</CommandEmpty>
      <CommandEmpty v-else>Type at least 2 characters to search</CommandEmpty>

      <CommandGroup heading="Navigation" v-show="searchQuery.length === 0">
        <CommandItem value="dashboard" @select = "runCommand(() => router.push('/'))">
          <span>Dashboard</span>
          <CommandShortcut>g d</CommandShortcut>
        </CommandItem>
        <CommandItem value="heroes" @select="runCommand(() => router.push('/heroes'))">
          <span>Heroes</span>
          <CommandShortcut>g h</CommandShortcut>
        </CommandItem>
        <CommandItem value="players" @select="runCommand(() => router.push('/players'))">
          <span>Players</span>
          <CommandShortcut>g p</CommandShortcut>
        </CommandItem>
      </CommandGroup>

      <CommandGroup v-if="searchResults.length > 0" heading="Players">
        <CommandItem
          v-for="player in searchResults"
          :key="player.id"
          value=""
          @select="runCommand(() => router.push(`/players/${player.id}`))"
        >
          <div class="flex items-center gap-2">
            <img v-if="player.avatar" :src="player.avatar" class="h-6 w-6 rounded-full"/>
            <div v-else class="h-6 w-6 rounded-full bg-gray-300 flex items-center justify-center text-xs">
              {{ player.name.charAt(0).toUpperCase() }}
            </div>
            <span>{{ player.name }}</span>
            <span v-if="player.type === 'id'" class="text-xs text-gray-500">(Account ID)</span>
          </div>
        </CommandItem>
      </CommandGroup>
    </CommandList>
  </CommandDialog>
</template>

<style scoped>

</style>
