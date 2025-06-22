// frontend/dota-2-project/pages/players/[id].vue
<script setup lang="ts">
import { computed, watch } from 'vue'; // Removed ref, onMounted if not used elsewhere
import { useRoute } from 'vue-router'; // Nuxt auto-imports

// Import your UI components
import { Card, CardHeader, CardTitle, CardContent, CardDescription, CardFooter } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';

// Define an interface for the expected player data structure (same as before)
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
  loccountrycode?: string;
}

interface PlayerData {
  solo_competitive_rank?: number | null;
  competitive_rank?: number | null;
  rank_tier?: number | null;
  leaderboard_rank?: number | null;
  profile: PlayerProfile | null; // Allow profile to be null initially or on error
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

// Get API base URL from runtime config
const runtimeConfig = useRuntimeConfig();
const API_BASE_URL = runtimeConfig.public.apiBaseUrl;

const {
  data: playerData, // Will be ref<PlayerData | null>
  pending: isLoading, // Will be ref<boolean>
  error, // Will be ref<Error | null>
  refresh // Function to manually re-fetch
} = useFetch<PlayerData>(() => `${API_BASE_URL}/api/v1/opendota_proxy/players/${accountId.value}`, {
  // `key` helps Nuxt manage caching and updates. It's good practice to make it unique per request.
  key: `playerData-${accountId.value}`,

  // `watch: [accountId]` will automatically re-fetch when accountId changes.
  // This is super useful if the user navigates from one player profile to another directly.
  watch: [accountId],

  // `default` provides an initial value for `data` before the fetch completes.
  // This helps prevent template errors if you try to access nested properties of playerData too early.
  default: () => ({
    profile: null,
    rank_tier: null,
    leaderboard_rank: null,
    competitive_rank: null
  } as PlayerData),

  // `transform` allows you to modify the data before it's assigned to `playerData`.
  // Useful if you need to reshape the API response. Not strictly needed here for direct proxy.
  // transform: (data) => {
  //   console.log("Transforming data:", data);
  //   return data;
  // }
});

 // Fetch Win/Loss data using the same pattern
const {data: wlData, pending: wlLoading, error: wlError} = useFetch<WinLossData>(() => `${API_BASE_URL}/api/v1/opendota_proxy/players/${accountId.value}/wl`, {
  key: `playerWL-${accountId.value}`,
  watch: [accountId],
  default: () => ({ win: 0, lose: 0 }),
});

const {data: totalsData, pending: totalsLoading, error: totalsError} = useFetch<TotalDataEntry[]>(() => `${API_BASE_URL}/api/v1/opendota_proxy/players/${accountId.value}/totals`, {
  key: `playerTotals-${accountId.value}`,
  watch: [accountId],
  default: () => [],
});

// Optional: Watch for errors specifically to log them or show custom messages
watch(error, (newError) => {
  if (newError) {
    console.error('Error fetching player data with useFetch:', newError);
    // You could set a custom error message ref here if needed,
    // or rely on the generic error display in the template.
  }
});

// Helper to format rank tier (same as before)
const getRankTierDisplay = (tier?: number | null) => {
  // ... (same implementation)
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
}

// Function to calculate average values for stats
const calculateAverage = (sum?: number, n?: number, fixed: number = 1): string => {
  if ( sum === undefined || n === undefined  || n === 0) return 'N/A';
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
    <!-- The `error` object from useFetch can be complex.
         `error.value?.data?.detail` might contain your FastAPI error message.
         `error.value?.message` is a more generic message.
    -->
    <Alert v-else-if="error" variant="destructive">
      <AlertTitle>Error Fetching Player Data</AlertTitle>
      <AlertDescription>
        {{ error.data?.detail || error.message || 'An unknown error occurred.' }}
        <pre v-if="error.data" class="mt-2 text-xs whitespace-pre-wrap">{{ JSON.stringify(error.data, null, 2) }}</pre>
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
            <CardTitle class="text-3xl">{{ playerData.profile.personaname }}</CardTitle>
            <CardDescription v-if="playerData.profile.name && playerData.profile.name !== playerData.profile.personaname" class="text-sm">
              {{ playerData.profile.name }}
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
          <div v-if="playerData.profile.loccountrycode">
            <p class="text-sm font-medium text-muted-foreground">Country</p>
            <p class="text-lg font-semibold">{{ playerData.profile.loccountrycode }}</p>
          </div>
          <div v-if="playerData.profile.plus">
            <Badge variant="secondary">Dota Plus</Badge>
          </div>
        </CardContent>
        <CardFooter v-if="playerData.profile.last_login" class="text-xs text-muted-foreground pt-4">
          Last Login: {{ new Date(playerData.profile.last_login).toLocaleDateString() }}
        </CardFooter>
      </Card>

      <div class="grid md:grid-cols-2 gap-6 mt-6">
      <Card>
        <CardHeader><CardTitle>Performance Display</CardTitle></CardHeader>
        <CardContent>
          <div>
            <h3>Overall (Parsed Matches)</h3>
            <div v-if="wlLoading">
              <Skeleton class="h-4 w-20"/>
              <Skeleton class="h-4 w-24"/>
              <Skeleton class="h-4 w-28"/>
            </div>
            <div v-else-if="wlError">
              <p class="text-destructive">Could not load W/L data</p>
            </div>
            <div v-else-if="wlData" class="space-y-1">
              <div class="flex justify-between">Wins: <span class="font-semibold">{{ wlData.win }}</span></div>
              <div class="flex justify-between">Losses: <span class="font-semibold">{{ wlData.lose }}</span></div>
              <div class="flex justify-between">Win Rate: <span class="font-semibold">{{ winRate }}</span></div>
            </div>
          </div>


          <div class="mt-6 border-t pt-4">
            <h3 class="text-md font-semibold mb-3 text-foreground/80">Key Averages (All Time Parsed)</h3>
            <div v-if="totalsLoading" class="space-y-1">
              <Skeleton class="h-4 w-full mb-1" v-for="i in 5" :key="`total-skel-${i}`"/>
            </div>
            <div v-else-if="totalsError">
              <p class="text-destructive text-sm">Could not load player totals.</p>
              <pre v-if="totalsError.data" class="mt-1 text-xs whitespace-pre-wrap">{{JSON.stringify(totalsError.data, null, 2)}}</pre>
            </div>
            <div v-else-if="totalsData && totalsData.length > 0" class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-1.5 text-sm">
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

      <Card>
        <CardHeader><CardTitle>Most Played Heroes</CardTitle></CardHeader>
        <CardContent>
          <p >
            Hero data will go here
          </p>
        </CardContent>
      </Card>
      </div>
    </div>
    <div v-else class="text-center py-10">
      <p class="text-muted-foreground">No player data found, or profile is private.</p>
      <p class="text-xs mt-1">Attempted to fetch for Account ID: {{ accountId }}</p>
    </div>
  </div>
</template>