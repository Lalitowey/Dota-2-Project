<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Search, Filter, TrendingUp, TrendingDown } from 'lucide-vue-next';

// Search functionality
const searchQuery = ref('');
const isSearching = ref(false);

// Mock data for now - will be replaced with API calls
const mockMatches = ref([
  {
    match_id: 7234567890,
    hero_id: 1,
    start_time: 1703971200, // Dec 30, 2023
    duration: 2134, // 35 minutes
    radiant_win: true,
    player_slot: 0,
    kills: 12,
    deaths: 3,
    assists: 8,
    last_hits: 234,
    gpm: 567,
    xpm: 634,
    hero_damage: 23456,
    tower_damage: 3456,
  },
  {
    match_id: 7234567889,
    hero_id: 74,
    start_time: 1703884800, // Dec 29, 2023
    duration: 1876, // 31 minutes
    radiant_win: false,
    player_slot: 128,
    kills: 8,
    deaths: 6,
    assists: 12,
    last_hits: 187,
    gpm: 445,
    xpm: 521,
    hero_damage: 19834,
    tower_damage: 2143,
  }
]);

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    isSearching.value = true;
    // TODO: Implement API call to fetch match history
    setTimeout(() => {
      isSearching.value = false;
    }, 1000);
  }
};

const formatDuration = (seconds: number) => {
  const minutes = Math.floor(seconds / 60);
  return `${minutes}m ${seconds % 60}s`;
};

const formatDate = (timestamp: number) => {
  return new Date(timestamp * 1000).toLocaleDateString();
};

const getWinLossColor = (won: boolean, isRadiant: boolean) => {
  const playerWon = (isRadiant && won) || (!isRadiant && !won);
  return playerWon ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400';
};

const getWinLossText = (won: boolean, isRadiant: boolean) => {
  const playerWon = (isRadiant && won) || (!isRadiant && !won);
  return playerWon ? 'Victory' : 'Defeat';
};
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
      </CardContent>
    </Card>

    <!-- Match History Results -->
    <Card>
      <CardHeader class="flex flex-row items-center justify-between">
        <div>
          <CardTitle>Recent Matches</CardTitle>
          <CardDescription>Latest match performances and statistics</CardDescription>
        </div>
        <Button variant="outline" size="sm">
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
        <div v-else-if="mockMatches.length === 0" class="text-center py-12">
          <Search class="h-12 w-12 mx-auto text-muted-foreground mb-4" />
          <h3 class="text-lg font-semibold mb-2">No Matches Found</h3>
          <p class="text-muted-foreground">Search for a player to view their match history</p>
        </div>

        <!-- Matches Table -->
        <div v-else class="space-y-4">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Result</TableHead>
                <TableHead>Hero</TableHead>
                <TableHead>Duration</TableHead>
                <TableHead>K/D/A</TableHead>
                <TableHead>LH</TableHead>
                <TableHead>GPM</TableHead>
                <TableHead>XPM</TableHead>
                <TableHead>Date</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow v-for="match in mockMatches" :key="match.match_id">
                <TableCell>
                  <Badge 
                    :variant="(match.player_slot < 128 && match.radiant_win) || (match.player_slot >= 128 && !match.radiant_win) ? 'default' : 'destructive'"
                  >
                    {{ getWinLossText(match.radiant_win, match.player_slot < 128) }}
                  </Badge>
                </TableCell>
                <TableCell class="font-medium">
                  Hero {{ match.hero_id }}
                </TableCell>
                <TableCell>{{ formatDuration(match.duration) }}</TableCell>
                <TableCell>
                  <span class="font-mono">{{ match.kills }}/{{ match.deaths }}/{{ match.assists }}</span>
                </TableCell>
                <TableCell>{{ match.last_hits }}</TableCell>
                <TableCell>
                  <span class="flex items-center gap-1">
                    {{ match.gpm }}
                    <TrendingUp v-if="match.gpm > 500" class="h-3 w-3 text-green-500" />
                    <TrendingDown v-else class="h-3 w-3 text-red-500" />
                  </span>
                </TableCell>
                <TableCell>{{ match.xpm }}</TableCell>
                <TableCell class="text-muted-foreground">{{ formatDate(match.start_time) }}</TableCell>
                <TableCell>
                  <Button variant="ghost" size="sm">
                    View Details
                  </Button>
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>

          <!-- Performance Summary Cards -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
            <Card>
              <CardHeader class="pb-2">
                <CardTitle class="text-sm font-medium">Average KDA</CardTitle>
              </CardHeader>
              <CardContent>
                <div class="text-2xl font-bold">10.0 / 4.5 / 10.0</div>
                <p class="text-xs text-muted-foreground">Last 10 matches</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader class="pb-2">
                <CardTitle class="text-sm font-medium">Win Rate</CardTitle>
              </CardHeader>
              <CardContent>
                <div class="text-2xl font-bold">65%</div>
                <p class="text-xs text-muted-foreground">8 wins, 2 losses</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader class="pb-2">
                <CardTitle class="text-sm font-medium">Avg GPM</CardTitle>
              </CardHeader>
              <CardContent>
                <div class="text-2xl font-bold">506</div>
                <p class="text-xs text-muted-foreground">
                  <TrendingUp class="inline h-3 w-3 text-green-500 mr-1" />
                  +15 from last period
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<style scoped>
/* Add any custom styles if needed */
</style>