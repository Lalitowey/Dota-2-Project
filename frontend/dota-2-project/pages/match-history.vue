<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { 
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerDescription,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
} from '@/components/ui/drawer'
import { Separator } from '@/components/ui/separator'
import { 
  Search, Filter, TrendingUp, TrendingDown,
  Eye, Sword, Shield,  Activity, Target, Clock,
  Trophy, Skull, Users, Zap
} from 'lucide-vue-next';
import { usePlayerAnalytics } from '@/composables/usePlayerAnalytics'
import { useHeroData } from '@/composables/useData'

const { fetchRecentMatches, calculatePerformanceTrends } = usePlayerAnalytics();
const {getHeroById, getHeroImageURL } = useHeroData();

// Search functionality
const searchQuery = ref('');
const isSearching = ref(false);
const searchError = ref<string | null>(null);

const matches = ref<any[]>([]);
const selectedMatch = ref<any | null>(null); 
const isDrawerOpen = ref(false);

// Performance Summary

const performanceSummary = ref<any>(null);


const handleSearch = async () => {
  if (!searchQuery.value.trim()) return;

  isSearching.value = true;
  searchError.value = null;

  try {
    const accountId = searchQuery.value.trim();
    const data = await fetchRecentMatches(accountId, 20);
    matches.value = data;
    performanceSummary.value = calculatePerformanceTrends(data);
  } catch (error: any) {
    searchError.value = error.message || 'Failed to fetch match history';
    matches.value = []; // no data 
  } finally {
    isSearching.value = false;
  }
};

const openMatchDetails = (match: any) => {
  selectedMatch.value = match;
  isDrawerOpen.value = true;
};

const formatDuration = (seconds: number) => {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
};

const formatDate = (timestamp: number) => {
  const date = new Date(timestamp * 1000);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
};

const formatDetailedDate = (timestamp: number) => {
  const date = new Date(timestamp * 1000);
  return date.toLocaleDateString('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

const getWinLossColor = (won: boolean, isRadiant: boolean) => {
  const playerWon = (isRadiant && won) || (!isRadiant && !won);
  return playerWon ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400';
};

const getWinLossText = (won: boolean, isRadiant: boolean) => {
  const playerWon = (isRadiant && won) || (!isRadiant && !won);
  return playerWon ? 'Victory' : 'Defeat';
};

const didPlayerWin = (match: any) => {
  return (match.player_slot < 128 && match.radiant_win) ||
         (match.placeholder > 128 && !match.radiant_win);
}

const getKDA = (match: any) => {
  if (!match) return 0;
  return match.deaths === 0 ? match.kills + match.assists : ((match.kills + match.assists) / match.deaths).toFixed(2);
};

const getHeroName = (heroId: number) => {
  const hero = getHeroById(heroId);
  return hero?.localized_name || `${heroId}`;
};

// Average Stats Calculations
const averageStats = computed(() => {
  if (matches.value.length === 0) return null;

  const total = matches.value.reduce((acc, match) => ({
    kills: acc.kills + match.kills,
    deaths: acc.deaths + match.deaths,
    assists: acc.assists + match.assists,
    gpm: acc.gpm + match.gold_per_min,
    xpm: acc.xpm + match.xp_per_min,
    lastHist: acc.lastHits + (match.last_hits || 0)
  }), { kills: 0, deaths: 0, assists: 0, gpm: 0, xpm: 0, lastHits: 0});

  const count = matches.value.length;
  const wins = matches.value.filter(m => didPlayerWin(m)).length;

  return {
    avgKills: (total.kills / count).toFixed(1),
    avgDeaths: (total.deaths / count).toFixed(1),
    avgAssists: (total.assists / count).toFixed(1),
    avgGPM: Math.round(total.gpm / count),
    avgXPM: Math.round(total.xpm/ count),
    avgLastHits: Math.round(total.lastHits / count),
    winRate: Math.round((wins / count) * 100),
    wins,
    losses: count - wins
  };
});
</script>

<template>
  <div class="container mx-auto py-8 px-4">
    <div class="mb-8">
      <h1 class="text-3xl font-bold mb-2">Match History Analysis</h1>
      <p class="text-muted-foreground">Analyze detailed match performance and trends</p>
    </div>

    <!-- Search Section -->
    <Card class="mb-6">
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <Search class="h-5 w-5" />
          Search Player Matches
        </CardTitle>
        <CardDescription>
          Enter a player's Account ID to analyze their match history
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div class="flex gap-2">
          <Input
            v-model="searchQuery"
            placeholder="Enter Account ID (e.g., 123456789)"
            class="flex-1"
            @keypress.enter="handleSearch"
          />
          <Button @click="handleSearch" :disabled="isSearching || !searchQuery.trim()">
            <Search class="h-4 w-4 mr-2" />
            {{ isSearching ? 'Searching...' : 'Search' }}
          </Button>
        </div>
        
        <!-- Error Alert -->
        <Alert v-if="searchError" variant="destructive" class="mt-4">
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{{ searchError }}</AlertDescription>
        </Alert>
      </CardContent>
    </Card>

    <!-- Performance Summary Cards -->
    <div v-if="averageStats" class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <Card>
        <CardHeader class="pb-2">
          <CardTitle class="text-sm font-medium flex items-center gap-2">
            <Trophy class="h-4 w-4 text-primary" />
            Win Rate
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ averageStats.winRate }}%</div>
          <p class="text-xs text-muted-foreground">
            {{ averageStats.wins }}W - {{ averageStats.losses }}L
          </p>
        </CardContent>
      </Card>
      
      <Card>
        <CardHeader class="pb-2">
          <CardTitle class="text-sm font-medium flex items-center gap-2">
            <Sword class="h-4 w-4 text-primary" />
            Average KDA
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold font-mono">
            {{ averageStats.avgKills }}/{{ averageStats.avgDeaths }}/{{ averageStats.avgAssists }}
          </div>
          <p class="text-xs text-muted-foreground">Last {{ matches.length }} matches</p>
        </CardContent>
      </Card>
      
      <Card>
        <CardHeader class="pb-2">
          <CardTitle class="text-sm font-medium flex items-center gap-2">
            <Zap class="h-4 w-4 text-primary" />
            Avg GPM
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ averageStats.avgGPM }}</div>
          <p class="text-xs text-muted-foreground">Gold per minute</p>
        </CardContent>
      </Card>
      
      <Card>
        <CardHeader class="pb-2">
          <CardTitle class="text-sm font-medium flex items-center gap-2">
            <Activity class="h-4 w-4 text-primary" />
            Avg XPM
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ averageStats.avgXPM }}</div>
          <p class="text-xs text-muted-foreground">Experience per minute</p>
        </CardContent>
      </Card>
    </div>

    <!-- Match History Results -->
    <Card>
      <CardHeader class="flex flex-row items-center justify-between">
        <div>
          <CardTitle>Recent Matches</CardTitle>
          <CardDescription>
            {{ matches.length > 0 ? `Showing ${matches.length} matches` : 'Latest match performances and statistics' }}
          </CardDescription>
        </div>
        <Button variant="outline" size="sm" disabled>
          <Filter class="h-4 w-4 mr-2" />
          Filters
        </Button>
      </CardHeader>
      <CardContent>
        <!-- Loading State -->
        <div v-if="isSearching" class="space-y-4">
          <Skeleton class="h-16 w-full" v-for="i in 5" :key="`match-skeleton-${i}`" />
        </div>

        <!-- Empty State -->
        <div v-else-if="matches.length === 0" class="text-center py-12">
          <Search class="h-12 w-12 mx-auto text-muted-foreground mb-4" />
          <h3 class="text-lg font-semibold mb-2">No Matches Found</h3>
          <p class="text-muted-foreground">Search for a player to view their match history</p>
        </div>

        <!-- Matches Table -->
        <div v-else class="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Result</TableHead>
                <TableHead>Hero</TableHead>
                <TableHead>Duration</TableHead>
                <TableHead>K/D/A</TableHead>
                <TableHead>KDA Ratio</TableHead>
                <TableHead>LH</TableHead>
                <TableHead>GPM</TableHead>
                <TableHead>XPM</TableHead>
                <TableHead>Date</TableHead>
                <TableHead class="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow 
                v-for="match in matches" 
                :key="match.match_id"
                class="cursor-pointer hover:bg-muted/50"
                @click="openMatchDetails(match)"
              >
                <TableCell>
                  <Badge 
                    :variant="didPlayerWin(match) ? 'default' : 'destructive'"
                  >
                    {{ getWinLossText(match.radiant_win, match.player_slot < 128) }}
                  </Badge>
                </TableCell>
                <TableCell>
                  <div class="flex items-center gap-2">
                    <img
                      v-if="getHeroImageURL(match.hero_id, 'icon')"
                      :src="getHeroImageURL(match.hero_id, 'icon')"
                      :alt="getHeroName(match.hero_id)"
                      class="h-8 w-8 rounded"
                    />
                    <span class="font-medium">{{ getHeroName(match.hero_id) }}</span>
                  </div>
                </TableCell>
                <TableCell>
                  <div class="flex items-center gap-1">
                    <Clock class="h-3 w-3 text-muted-foreground" />
                    {{ formatDuration(match.duration) }}
                  </div>
                </TableCell>
                <TableCell>
                  <span class="font-mono text-sm">
                    {{ match.kills }}/{{ match.deaths }}/{{ match.assists }}
                  </span>
                </TableCell>
                <TableCell>
                  <Badge variant="outline" :class="
                    getKDA(match) >= 3 ? 'bg-green-500/10 text-green-600 border-green-600' :
                    getKDA(match) >= 2 ? 'bg-blue-500/10 text-blue-600 border-blue-600' :
                    'bg-gray-500/10'
                  ">
                    {{ getKDA(match) }}
                  </Badge>
                </TableCell>
                <TableCell>{{ match.last_hits || 0 }}</TableCell>
                <TableCell>
                  <span class="flex items-center gap-1">
                    {{ match.gold_per_min }}
                    <TrendingUp v-if="match.gold_per_min > 500" class="h-3 w-3 text-green-500" />
                    <TrendingDown v-else-if="match.gold_per_min < 350" class="h-3 w-3 text-red-500" />
                  </span>
                </TableCell>
                <TableCell>{{ match.xp_per_min }}</TableCell>
                <TableCell class="text-muted-foreground text-sm">
                  {{ formatDate(match.start_time) }}
                </TableCell>
                <TableCell class="text-right">
                  <Button 
                    variant="ghost" 
                    size="sm"
                    @click.stop="openMatchDetails(match)"
                  >
                    <Eye class="h-4 w-4 mr-2" />
                    Details
                  </Button>
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>

    <!-- Match Details Drawer -->
    <Drawer v-model:open="isDrawerOpen">
      <DrawerContent class="max-h-[90vh]">
        <div class="mx-auto w-full max-w-4xl overflow-y-auto">
          <DrawerHeader>
            <DrawerTitle class="flex items-center gap-3">
              <img
                v-if="selectedMatch && getHeroImageURL(selectedMatch.hero_id, 'img')"
                :src="getHeroImageURL(selectedMatch.hero_id, 'img')"
                :alt="getHeroName(selectedMatch?.hero_id)"
                class="h-12 w-12 rounded"
              />
              <div>
                <div class="text-2xl">{{ getHeroName(selectedMatch?.hero_id) }}</div>
                <div class="text-sm font-normal text-muted-foreground">
                  Match ID: {{ selectedMatch?.match_id }}
                </div>
              </div>
              <Badge 
                v-if="selectedMatch"
                :variant="didPlayerWin(selectedMatch) ? 'default' : 'destructive'"
                class="ml-auto text-base px-4 py-1"
              >
                {{ getWinLossText(selectedMatch.radiant_win, selectedMatch.player_slot < 128) }}
              </Badge>
            </DrawerTitle>
            <DrawerDescription>
              Played on {{ formatDetailedDate(selectedMatch?.start_time) }}
            </DrawerDescription>
          </DrawerHeader>
          
          <div class="p-6 space-y-6" v-if="selectedMatch">
            <!-- Quick Stats Grid -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Card>
                <CardContent class="pt-6 text-center">
                  <div class="text-3xl font-bold">{{ getKDA(selectedMatch) }}</div>
                  <div class="text-sm text-muted-foreground mt-1">KDA Ratio</div>
                  <div class="text-xs text-muted-foreground mt-1 font-mono">
                    {{ selectedMatch.kills }}/{{ selectedMatch.deaths }}/{{ selectedMatch.assists }}
                  </div>
                </CardContent>
              </Card>
              
              <Card>
                <CardContent class="pt-6 text-center">
                  <div class="text-3xl font-bold">{{ selectedMatch.gold_per_min }}</div>
                  <div class="text-sm text-muted-foreground mt-1">GPM</div>
                  <div class="text-xs text-muted-foreground mt-1">
                    Gold per minute
                  </div>
                </CardContent>
              </Card>
              
              <Card>
                <CardContent class="pt-6 text-center">
                  <div class="text-3xl font-bold">{{ selectedMatch.xp_per_min }}</div>
                  <div class="text-sm text-muted-foreground mt-1">XPM</div>
                  <div class="text-xs text-muted-foreground mt-1">
                    Experience per minute
                  </div>
                </CardContent>
              </Card>
              
              <Card>
                <CardContent class="pt-6 text-center">
                  <div class="text-3xl font-bold">{{ formatDuration(selectedMatch.duration) }}</div>
                  <div class="text-sm text-muted-foreground mt-1">Duration</div>
                  <div class="text-xs text-muted-foreground mt-1">
                    Match length
                  </div>
                </CardContent>
              </Card>
            </div>

            <Separator />

            <!-- Detailed Stats -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- Combat Stats -->
              <Card>
                <CardHeader>
                  <CardTitle class="flex items-center gap-2 text-lg">
                    <Sword class="h-5 w-5" />
                    Combat Statistics
                  </CardTitle>
                </CardHeader>
                <CardContent class="space-y-3">
                  <div class="flex justify-between items-center">
                    <span class="text-muted-foreground">Kills</span>
                    <span class="font-semibold text-lg">{{ selectedMatch.kills }}</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-muted-foreground">Deaths</span>
                    <span class="font-semibold text-lg">{{ selectedMatch.deaths }}</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-muted-foreground">Assists</span>
                    <span class="font-semibold text-lg">{{ selectedMatch.assists }}</span>
                  </div>
                  <Separator />
                  <div class="flex justify-between items-center">
                    <span class="text-muted-foreground">Hero Damage</span>
                    <span class="font-semibold">{{ (selectedMatch.hero_damage || 0).toLocaleString() }}</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-muted-foreground">Tower Damage</span>
                    <span class="font-semibold">{{ (selectedMatch.tower_damage || 0).toLocaleString() }}</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-muted-foreground">Hero Healing</span>
                    <span class="font-semibold">{{ (selectedMatch.hero_healing || 0).toLocaleString() }}</span>
                  </div>
                </CardContent>
              </Card>

              <!-- Farm Stats -->
              <Card>
                <CardHeader>
                  <CardTitle class="flex items-center gap-2 text-lg">
                    <Target class="h-5 w-5" />
                    Farming Statistics
                  </CardTitle>
                </CardHeader>
                <CardContent class="space-y-3">
                  <div class="flex justify-between items-center">
                    <span class="text-muted-foreground">Last Hits</span>
                    <span class="font-semibold text-lg">{{ selectedMatch.last_hits || 0 }}</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-muted-foreground">Denies</span>
                    <span class="font-semibold text-lg">{{ selectedMatch.denies || 0 }}</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-muted-foreground">Neutral Kills</span>
                    <span class="font-semibold text-lg">{{ selectedMatch.neutral_kills || 0 }}</span>
                  </div>
                  <Separator />
                  <div class="flex justify-between items-center">
                    <span class="text-muted-foreground">Gold Per Min</span>
                    <span class="font-semibold">{{ selectedMatch.gold_per_min }}</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-muted-foreground">XP Per Min</span>
                    <span class="font-semibold">{{ selectedMatch.xp_per_min }}</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-muted-foreground">Level</span>
                    <span class="font-semibold">{{ selectedMatch.level || 'N/A' }}</span>
                  </div>
                </CardContent>
              </Card>
            </div>

            <!-- Match Info -->
            <Card>
              <CardHeader>
                <CardTitle class="flex items-center gap-2 text-lg">
                  <Users class="h-5 w-5" />
                  Match Information
                </CardTitle>
              </CardHeader>
              <CardContent class="space-y-3">
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <span class="text-muted-foreground text-sm">Team</span>
                    <div class="font-semibold">
                      {{ selectedMatch.player_slot < 128 ? 'Radiant' : 'Dire' }}
                    </div>
                  </div>
                  <div>
                    <span class="text-muted-foreground text-sm">Game Mode</span>
                    <div class="font-semibold">
                      {{ selectedMatch.game_mode || 'All Pick' }}
                    </div>
                  </div>
                  <div>
                    <span class="text-muted-foreground text-sm">Lobby Type</span>
                    <div class="font-semibold">
                      {{ selectedMatch.lobby_type === 7 ? 'Ranked' : 'Normal' }}
                    </div>
                  </div>
                  <div>
                    <span class="text-muted-foreground text-sm">Skill Bracket</span>
                    <div class="font-semibold">
                      {{ selectedMatch.skill || 'Unknown' }}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          <DrawerFooter>
            <div class="flex gap-2 w-full">
              <Button 
                variant="outline" 
                class="flex-1"
                @click="openMatchDetails"
              >
                View on OpenDota
              </Button>
              <DrawerClose as-child>
                <Button variant="default" class="flex-1">Close</Button>
              </DrawerClose>
            </div>
          </DrawerFooter>
        </div>
      </DrawerContent>
    </Drawer>
  </div>
</template>

<style scoped>
/* Smooth drawer animations are handled by the Drawer component */
</style>