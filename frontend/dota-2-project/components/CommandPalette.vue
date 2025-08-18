<script setup lang="ts">
  import { ref, watch } from 'vue';
  import { useRouter } from 'vue-router';
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

  interface DisplayResult {
    type: 'player' | 'id';
    id: number;
    name: string;
    avatar?: string;
  }

  const searchQuery = ref('');
  const searchResults = ref<SearchResult[]>([]);
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

      DisplayResult.value = results.map(player => ({
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

    if (isAccountId.value) {
      isLoading.value = false;
      searchResults.value = [{
        type: 'id',
        id: parseInt(newQuery, 10),
        name: `Account ID: ${newQuery}`
      }];
    } else if (newQuery.length > 1) {
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
    <CommandInput v-model="searchQuery" placeholder="Search for a player or navigate.."/>
    <CommandList>
      <CommandEmpty v-if="isLoading">Searching...</CommandEmpty>
      <CommandEmpty v-else-if="searchQuery.length > 1 && !isLoading">No results found.</CommandEmpty>
      <CommandEmpty v-else>Type to search for a player</CommandEmpty>
      <CommandGroup heading="Navigation">
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

      <CommandGroup>
        <CommandItem
          v-for="player in searchResults"
          :key="player.account_id"
          :value="`player-${player.account_id}`"
          @select="runCommand(() => router.push(`/players/${player.account_id}`))"
        >
          <div class="flex items-center gap-2">
            <img :src="player.avatarfull" class="h-6 w-6 rounded-full"/>
            <span>{{ player.personaname}}</span>
          </div>
        </CommandItem>
      </CommandGroup>
    </CommandList>
  </CommandDialog>
</template>

<style scoped>

</style>
