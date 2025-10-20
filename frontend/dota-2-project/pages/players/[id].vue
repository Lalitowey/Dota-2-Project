<script setup lang="ts">
import { computed, watch, ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

// Import your UI components
import { Card, CardHeader, CardTitle, CardContent, CardDescription, CardFooter } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';

import { usePlayerData, useHeroData } from '@/composables/useData';

interface PlayerProfile {
  account_id: number;
  personaname: string;
  name?: string;
  plus?: boolean;
  cheese?: number;
  steamid?: string;
  avatarfull: string;
  profileurl: string;
  last_login?: string;
  loccountry_code?: string;
}

interface PlayerData {
  solo_competitive_rank?: number | null;
  competitive_rank?: number | null;
  rank_tier?: number | null;
  leaderboard_rank?: number | null;
  profile: PlayerProfile | null;
}

interface PlayerHeroStat {
  hero_id: number;
  last_played: number;
  games: number;
  win: number;
  with_games: number;
  with_win: number;
  against_games: number;
  against_win: number;
}

interface WinLossData {
  win: number;
  lose: number;
}

interface TotalDataEntry {
  field: string
  n: number
  sum: number
}

const route = useRoute();
const accountId = computed(() => route.params.id as string);

// Use our new composables
const { fetchPlayerProfile, fetchPlayerWinLoss, fetchPlayerHeroes, fetchPlayerMatches } = usePlayerData();
const { ensureHeroConstants, getHeroById, getHeroImageURL } = useHeroData();

// Reactive state
const playerData = ref<PlayerData | null>(null);
const wlData = ref<WinLossData | null>(null);
const playerHeroesData = ref<PlayerHeroStat[] | null>(null);
const totalsData = ref<TotalDataEntry[] | null>(null);

const isLoadingProfile = ref(false);
const wlLoading = ref(false);
const playerHeroesIsLoading = ref(false);
const totalsLoading = ref(false);

const profileError = ref<string | null>(null);
const wlError = ref<string | null>(null);
const playerHeroesError = ref<string | null>(null);
const totalsError = ref<string | null>(null);

// Computed properties
const isLoading = computed(() => 
  isLoadingProfile.value || wlLoading.value || playerHeroesIsLoading.value || totalsLoading.value
);

const error = computed(() => 
  profileError.value || wlError.value || playerHeroesError.value || totalsError.value
);

// Data fetching functions
const loadPlayerData = async () => {
  if (!accountId.value) return;
  
  isLoadingProfile.value = true;
  profileError.value = null;
  
  try {
    playerData.value = await fetchPlayerProfile(accountId.value);
  } catch (err: any) {
    profileError.value = err.message || 'Failed to load player data';
  } finally {
    isLoadingProfile.value = false;
  }
};

const loadWinLossData = async () => {
  if (!accountId.value) return;
  
  wlLoading.value = true;
  wlError.value = null;
  
  try {
    wlData.value = await fetchPlayerWinLoss(accountId.value);
  } catch (err: any) {
    wlError.value = err.message || 'Failed to load win/loss data';
  } finally {
    wlLoading.value = false;
  }
};

const loadHeroesData = async () => {
  if (!accountId.value) return;
  
  playerHeroesIsLoading.value = true;
  playerHeroesError.value = null;
  
  try {
    playerHeroesData.value = await fetchPlayerHeroes(accountId.value);
  } catch (err: any) {
    playerHeroesError.value = err.message || 'Failed to load heroes data';
  } finally {
    playerHeroesIsLoading.value = false;
  }
};

const loadTotalData = async () => {
  if (!accountId.value) return;
  
  totalsLoading.value = true;
  totalsError.value = null;
  
  try {
    const runtimeConfig = useRuntimeConfig();
    const API_BASE_URL = runtimeConfig.public.apiBaseUrl;
    totalsData.value = await $fetch<TotalDataEntry[]>(`${API_BASE_URL}/api/v1/opendota_proxy/players/${accountId.value}/totals`);
  } catch (err: any) {
    totalsError.value = err.message || 'Failed to load total stats';
  } finally {
    totalsLoading.value = false;
  }
};

// Load all data
const loadAllData = async () => {
  // Ensure hero constants are loaded first
  await ensureHeroConstants();
  
  // Load all player data in parallel
  await Promise.all([
    loadPlayerData(),
    loadWinLossData(),
    loadHeroesData(),
    loadTotalData(),
  ]);
};

// Watch for account ID changes
watch(accountId, () => {
  if (accountId.value) {
    loadAllData();
  }
}, { immediate: true });

// Initial load
onMounted(() => {
  if (accountId.value) {
    loadAllData();
  }
});

// Helper functions for display
function formatLastLogin(lastLogin: string | undefined) {
  if (!lastLogin) return 'Never logged in';
  return new Date(lastLogin).toLocaleString();
}

function getRankDisplay(rankTier: number | null | undefined) {
  if (!rankTier) return 'Unranked';
  const tier = rankTier % 10;
  const rank = Math.floor(rankTier / 10);
  const ranks = ['Herald', 'Guardian', 'Crusader', 'Archon', 'Legend', 'Ancient', 'Divine', 'Immortal'];
  return `${ranks[rank - 1]} ${tier}`;
}

function calculateWinRate(wins: number, total: number) {
  if (total === 0) return 0;
  return ((wins / total) * 100).toFixed(1);
}

function formatNumber(num: number | undefined) {
  if (num === undefined) return 'N/A';
  return num.toLocaleString();
}

function formatAverage(sum: number, count: number) {
  if (count === 0) return 'N/A';
  return (sum / count).toFixed(1);
}

// Function to calculate average values for stats
const calculateAverage = (sum?: number, n?: number, fixed: number = 1): string => {
  if (sum === undefined || n === undefined || n === 0) return 'N/A';
  return (sum / n).toFixed(fixed);
};

// Function to format stat keys for display
const formatStatKey = (key: string): string => {
  return key
    .replace(/_/g, ' ')
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

const topPlayedHeroes = computed(() => {
  if (!playerHeroesData.value) return [];
  return [...playerHeroesData.value].sort((a, b) => b.games - a.games).slice(0, 10);
});

// Optional: Watch for errors specifically to log them or show custom messages
watch(error, (newError) => {
  if (newError) {
    console.error('Error fetching player data with useFetch:', newError);
    // You could set a custom error message ref here if needed,
    // or rely on the generic error display in the template.
  }
});

const getRankTierDisplay = (tier?: number | null) => {
  if (tier === null || tier === undefined) return 'N/A';
  const mainTier = Math.floor(tier / 10);
  const star = tier % 10;
  if (mainTier === 0 && star === 0) return 'Uncalibrated'; // OpenDota rank_tier is null if uncalibrated, but this covers if it's 0
  if (mainTier === 8) return 'Immortal';
  const tiers = ['Uncalibrated', 'Herald', 'Guardian', 'Crusader', 'Archon', 'Legend', 'Ancient', 'Divine', 'Immortal'];
  return `${tiers[mainTier]} ${star > 0 ? '[' + star + ']' : ''}`;
};

// Computed win and loss rates
const winRate = computed(() => {
  // if we have win/loss data, calculate the win rate
  if (wlData.value && (wlData.value.win + wlData.value.lose > 0)) {
    return ((wlData.value.win / (wlData.value.win + wlData.value.lose)) * 100).toFixed(1) + '%';
  }
  return 'N/A';
});

// Function to find specific total data by field
const findTotal = (field: string): TotalDataEntry | undefined => {
  if (!totalsData.value) return undefined;
  return totalsData.value.find(entry => entry.field === field);
};

// Create hero store object using the composable
const heroStore = {
  getHeroById,
  getHeroImageURL
};
</script>

<template>
  <div class="container mx-auto py-8 px-4">
    <!-- Loading State -->
    <div v-if="isLoading" class="space-y-6">
      <div class="flex items-center space-x-4">
        <Skeleton class="h-20 w-20 rounded-full" /> {/* Adjusted size to match avatar */}
        <div class="space-y-2">
          <Skeleton class="h-8 w-48" />
          <Skeleton class="h-4 w-32" />
        </div>
      </div>
      <Skeleton class="h-32 w-full" />
      <Skeleton class="h-16 w-full" /> {/* Reduced height for other info card */}
    </div>

    <!-- Error State -->
    <Alert v-else-if="error" variant="destructive">
      <AlertTitle>Error Fetching Player Data</AlertTitle>
      <AlertDescription>
        {{ error }}
      </AlertDescription>
    </Alert>

    <!-- Player Data Display -->
    <!-- Make sure to safely access playerData.value and playerData.value.profile -->
    <div v-else-if="playerData && playerData.profile">
      <Card class="mb-6">
        <CardHeader class="flex flex-row items-center space-x-4 pb-4">
          <Avatar class="h-20 w-20 border">
            <AvatarImage :src="playerData.profile.avatarfull" :alt="playerData.profile.personaname" />
            <AvatarFallback>{{ playerData.profile.personaname?.substring(0, 2).toUpperCase() || 'P' }}</AvatarFallback>
          </Avatar>
          <div>
            <CardTitle class="text-3xl">{{ playerData.profile.name || playerData.profile.personaname }}</CardTitle>
            <CardDescription v-if="playerData.profile.name && playerData.profile.name !== playerData.profile.personaname" class="text-sm">
              {{ playerData.profile.personaname }}
            </CardDescription>
            <a :href="playerData.profile.profileurl" target="_blank" rel="noopener noreferrer" class="text-sm text-primary hover:underline">
              Steam Profile
            </a>
          </div>
        </CardHeader>
        <CardContent class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          <div>
            <p class="text-sm font-medium text-muted-foreground">Rank Tier</p>
            <p class="text-lg font-semibold">{{ getRankTierDisplay(playerData.rank_tier) }}</p>
          </div>
          <div v-if="playerData.leaderboard_rank">
            <p class="text-sm font-medium text-muted-foreground">Leaderboard</p>
            <p class="text-lg font-semibold">#{{ playerData.leaderboard_rank }}</p>
          </div>
          <div v-if="playerData.competitive_rank">
            <p class="text-sm font-medium text-muted-foreground">MMR (Est.)</p>
            <p class="text-lg font-semibold">{{ playerData.competitive_rank }}</p>
          </div>
          <div v-if="playerData.profile.loccountry_code">
            <p class="text-sm font-medium text-muted-foreground">Country</p>
            <p class="text-lg font-semibold">{{ playerData.profile.loccountry_code }}</p>
          </div>
          <div v-if="playerData.profile.plus">
            <Badge variant="secondary">Dota Plus</Badge>
          </div>
        </CardContent>
        <CardFooter v-if="playerData.profile.last_login" class="text-xs text-muted-foreground pt-4">
          Last Login: {{ new Date(playerData.profile.last_login).toLocaleDateString() }}
        </CardFooter>
      </Card>

      <Card class="mb-6">
        <CardHeader><CardTitle>Performance Display</CardTitle></CardHeader>
        <CardContent>
          <div class="mb-6">
            <h3 class='text-md font-semibold mb-2 text-foreground/80'>Overall (Parsed Matches)</h3>
            <div v-if="wlLoading">
              <Skeleton class="h-4 w-20"/>
              <Skeleton class="h-4 w-24"/>
              <Skeleton class="h-4 w-28"/>
            </div>
            <div v-else-if="wlError">
              <p class="text-destructive">Could not load W/L data</p>
            </div>
            <div v-else-if="wlData" class="space-y-1 text-sm">
              <div class="flex justify-between">Wins: <span class="font-semibold">{{ wlData.win }}</span></div>
              <div class="flex justify-between">Losses: <span class="font-semibold">{{ wlData.lose }}</span></div>
              <div class="flex justify-between">Win Rate: <span class="font-semibold">{{ winRate }}</span></div>
            </div>
          </div>

          <div>
            <h3 class="text-md font-semibold mb-3 text-foreground/80">Key Averages (All Time Parsed)</h3>
            <div v-if="totalsLoading" class="space-y-1">
              <Skeleton class="h-4 w-full mb-1" v-for="i in 5" :key="`total-skel-${i}`"/>
            </div>
            <div v-else-if="totalsError">
              <p class="text-destructive text-sm">Could not load player totals.</p>
              <pre v-if="totalsError" class="mt-1 text-xs whitespace-pre-wrap">{{ totalsError }}</pre>
            </div>
            <div v-else-if="totalsData && totalsData.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-x-6 gap-y-1.5 text-sm">
              <template v-for="statKey in ['kills', 'deaths', 'assists', 'gold_per_min', 'xp_per_min', 'last_hits', 'denies', 'hero_damage', 'tower_damage']" :key="statKey">
                <template v-if="findTotal(statKey)">
                  <div class="flex justify-between">
                    <span>{{ formatStatKey(statKey) }}:</span>
                    <span class="font-semibold">
                      {{ calculateAverage(findTotal(statKey)?.sum, findTotal(statKey)?.n, (statKey === 'kills' || statKey === 'deaths' || statKey === 'assists' ? 1 : 0) ) }}
                      <span v-if="statKey.includes('_per_min')">/min</span>
                    </span>
                  </div>
                </template>
              </template>
            </div>
            <div v-else>
              <p class="text-muted-foreground text-sm">No aggregated totals data available</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card class="mb-6">
        <CardHeader><CardTitle>Most Played Heroes</CardTitle></CardHeader>
        <CardContent>
          <div v-if="playerHeroesIsLoading">
            <Skeleton class="h-8 w-full mb-2" v-for="i in 5" :key="`ph-skel-${i}`"/>
          </div>
          <div v-else-if="playerHeroesError">
            <p class="text-destructive">Could not load most played Heroes.</p>
          </div>
          <div v-else-if="topPlayedHeroes && topPlayedHeroes.length > 0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead class="w-[80px]">Icon</TableHead>
                  <TableHead>Hero</TableHead>
                  <TableHead class="text-right">Games</TableHead>
                  <TableHead class="text-right">Win Rate</TableHead>
                  <TableHead class="text-right hidden sm:table-cell">Last Played</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                <TableRow v-for="heroStat in topPlayedHeroes" :key="heroStat.hero_id">
                  <TableCell>
                    <img
                      v-if="heroStore.getHeroImageURL(heroStat.hero_id, 'icon')"
                      :src="heroStore.getHeroImageURL(heroStat.hero_id, 'icon')"
                      :alt="heroStore.getHeroById(heroStat.hero_id)?.localized_name"
                      class="h-8 w-auto rounded"
                    />
                  </TableCell>
                  <TableCell class="font-medium">
                    {{ heroStore.getHeroById(heroStat.hero_id)?.localized_name || `Hero ID: ${heroStat.hero_id}` }}
                  </TableCell>
                  <TableCell class="text-right">{{heroStat.games}}</TableCell>
                  <TableCell class="text-right">
                    {{ heroStat.games > 0 ? ((heroStat.win / heroStat.games) * 100).toFixed(1) + '%' : 'N/A' }}
                  </TableCell>
                  <TableCell class="text-right hidden sm:table-cell">
                    {{ heroStat.last_played ? new Date(heroStat.last_played * 1000).toLocaleDateString() : 'N/A' }}
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </div>
          <div v-else>
            <p class="text-muted-foreground">No Hero data available</p>
          </div>
        </CardContent>
      </Card>
    </div>
    <div v-else class="text-center py-10">
      <p class="text-muted-foreground">No player data found, or profile is private.</p>
      <p class="text-xs mt-1">Attempted to fetch for Account ID: {{ accountId }}</p>
    </div>
  </div>
</template>