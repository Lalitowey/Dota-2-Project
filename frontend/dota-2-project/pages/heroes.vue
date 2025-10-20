<script setup lang="ts">
import { ref, computed, onMounted, type Component } from 'vue';
import { useHeroStore } from '@/stores/heroStore';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Skeleton } from '@/components/ui/skeleton';
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from '@/components/ui/sheet';
import { Search, Filter, TrendingUp, Star, Shield, Sword } from 'lucide-vue-next';

interface Hero {
  id: number;
  name: string;
  localized_name: string;
  roles: string[];
  primary_attr: string;
  attack_type: string;
}

interface TopHero {
  heroId: number;
  name: string;
  winRate: number;
  pickRate: number;
  tier: string;
}

interface HeroStats {
  winRate: number;
  pickRate: number;
  banRate: number;
  averageGPM: number;
  averageKDA: string;
  farmGoals: {
    '10min': string;
    '20min': string;
    [key: string]: string;
  };
  popularItems: { name: string; pickRate: number }[];
  metaRank: string;
  metaDescription: string;
}

const heroStore = useHeroStore();
const searchQuery = ref<string>('');
const selectedHero = ref<Hero | null>(null);
const isSheetOpen = ref<boolean>(false);

// Mock data for hero statistics and meta information
const mockHeroStats: Record<number, HeroStats> = {
  1: { // Anti-Mage
    winRate: 52.3,
    pickRate: 15.2,
    banRate: 8.5,
    averageGPM: 598,
    averageKDA: '8.2/4.1/6.5',
    farmGoals: {
      '10min': 'Last hits: 70-80, GPM: 400+',
      '20min': 'Last hits: 160-180, GPM: 550+, Core items: BF + Treads'
    },
    popularItems: [
      { name: 'Battle Fury', pickRate: 87.3 },
      { name: 'Power Treads', pickRate: 76.8 },
      { name: 'Manta Style', pickRate: 71.2 },
      { name: 'Black King Bar', pickRate: 68.9 },
      { name: 'Abyssal Blade', pickRate: 45.6 }
    ],
    metaRank: 'A-Tier',
    metaDescription: 'Strong late-game carry with excellent mobility and magic resistance.'
  },
  2: { // Axe 
    winRate: 49.8,
    pickRate: 12.1,
    banRate: 5.3,
    averageGPM: 345,
    averageKDA: '5.8/6.2/12.4',
    farmGoals: {
      '10min': 'Last hits: 25-35, Focus on ganks and initiation',
      '20min': 'Core items: Blink + Blade Mail, Tower damage participation'
    },
    popularItems: [
      { name: 'Blink Dagger', pickRate: 91.2 },
      { name: 'Blade Mail', pickRate: 78.4 },
      { name: 'Vanguard', pickRate: 65.7 },
      { name: 'Crimson Guard', pickRate: 52.3 },
      { name: 'Black King Bar', pickRate: 41.8 }
    ],
    metaRank: 'B+Tier',
    metaDescription: 'Solid initiator with strong early to mid-game presence.'
  }
};

// Top heroes for current patch (mock data)
const topHeroesThisPatch = ref<TopHero[]>([
  { heroId: 1, name: 'Anti-Mage', winRate: 52.3, pickRate: 15.2, tier: 'S' },
  { heroId: 74, name: 'Invoker', winRate: 51.8, pickRate: 18.7, tier: 'S' },
  { heroId: 2, name: 'Axe', winRate: 49.8, pickRate: 12.1, tier: 'A' },
  { heroId: 106, name: 'Ember Spirit', winRate: 48.9, pickRate: 14.3, tier: 'A' },
  { heroId: 11, name: 'Shadow Fiend', winRate: 47.5, pickRate: 11.8, tier: 'B' }
]);

onMounted(async () => {
  await heroStore.fetchHeroConstants();
});

const filteredHeroes = computed<Hero[]>(() => {
  if (!heroStore.allHeroesArray) return [];
  
  if (!searchQuery.value.trim()) {
    return heroStore.allHeroesArray as Hero[];
  }
  
  const query = searchQuery.value.toLowerCase();
  return (heroStore.allHeroesArray as Hero[]).filter((hero: Hero) => 
    hero.localized_name.toLowerCase().includes(query) ||
    hero.name.toLowerCase().includes(query) ||
    hero.roles.some((role: string) => role.toLowerCase().includes(query))
  );
});

const openHeroDetails = (hero: Hero | null | undefined) => {
  if (!hero) return;
  selectedHero.value = hero;
  isSheetOpen.value = true;
};

const getHeroStats = (heroId: number): HeroStats => {
  return mockHeroStats[heroId] || {
    winRate: 50.0,
    pickRate: 8.0,
    banRate: 3.0,
    averageGPM: 400,
    averageKDA: '6.0/5.0/8.0',
    farmGoals: {
      '10min': 'Standard farming pattern',
      '20min': 'Core items completion'
    },
    popularItems: [
      { name: 'Core Item 1', pickRate: 75.0 },
      { name: 'Core Item 2', pickRate: 65.0 },
      { name: 'Situational Item', pickRate: 45.0 }
    ],
    metaRank: 'B-Tier',
    metaDescription: 'Balanced hero with situational picks.'
  };
};

const getTierColor = (tier: string): string => {
  switch (tier) {
    case 'S': return 'bg-red-500';
    case 'A': return 'bg-orange-500';
    case 'B': return 'bg-yellow-500';
    default: return 'bg-gray-500';
  }
};

const getRoleIcon = (role: string): Component => {
  switch (role.toLowerCase()) {
    case 'carry': return Sword;
    case 'support': return Shield;
    case 'initiator': return Star;
    default: return Star;
  }
};
</script>

<template>
  <div class="container mx-auto py-8 px-4">
    <div class="mb-8">
      <h1 class="text-3xl font-bold mb-2">Heroes Dashboard</h1>
      <p class="text-muted-foreground">Explore heroes, their stats, and current meta standing</p>
    </div>

    <!-- Top Heroes This Patch Section -->
    <Card class="mb-8">
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <TrendingUp class="h-5 w-5" />
          Top Heroes This Patch
        </CardTitle>
        <CardDescription>
          Current highest performing heroes in the meta
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
          <div v-for="hero in topHeroesThisPatch" :key="hero.heroId" 
               class="flex items-center space-x-3 p-3 rounded-lg border bg-card hover:bg-accent/50 transition-colors cursor-pointer"
               @click="openHeroDetails(heroStore.getHeroById(hero.heroId))">
            <img
              v-if="heroStore.getHeroImageURL(hero.heroId, 'icon')"
              :src="heroStore.getHeroImageURL(hero.heroId, 'icon')"
              :alt="hero.name"
              class="h-10 w-10 rounded"
            />
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2">
                <h3 class="font-medium text-sm truncate">{{ hero.name }}</h3>
                <Badge :class="getTierColor(hero.tier)" class="text-xs px-1 py-0 text-white">
                  {{ hero.tier }}
                </Badge>
              </div>
              <p class="text-xs text-muted-foreground">
                {{ hero.winRate }}% WR • {{ hero.pickRate }}% PR
              </p>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Search and Filter -->
    <Card class="mb-6">
      <CardContent class="p-4">
        <div class="flex gap-2">
          <div class="relative flex-1">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              v-model="searchQuery"
              placeholder="Search heroes by name or role..."
              class="pl-10"
            />
          </div>
          <Button variant="outline" size="icon">
            <Filter class="h-4 w-4" />
          </Button>
        </div>
      </CardContent>
    </Card>

    <!-- Heroes Grid -->
    <Card>
      <CardHeader>
        <CardTitle>All Heroes</CardTitle>
        <CardDescription>Click on any hero to view detailed information</CardDescription>
      </CardHeader>
      <CardContent>
        <!-- Loading State -->
        <div v-if="heroStore.isLoadingConstants" class="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-8 gap-4">
          <Skeleton class="aspect-square rounded-lg" v-for="i in 32" :key="`hero-skeleton-${i}`" />
        </div>
        
        <!-- Error State -->
        <div v-else-if="heroStore.constantsError" class="text-center py-12">
          <p class="text-destructive mb-2">Failed to load heroes</p>
          <p class="text-sm text-muted-foreground">{{ heroStore.constantsError }}</p>
          <Button @click="heroStore.fetchHeroConstants()" class="mt-4">
            Retry
          </Button>
        </div>
        
        <!-- Heroes Grid -->
        <div v-else class="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-8 gap-4">
          <div
            v-for="hero in filteredHeroes"
            :key="hero.id"
            class="group cursor-pointer"
            @click="openHeroDetails(hero)"
          >
            <div class="aspect-square relative rounded-lg overflow-hidden border bg-card hover:bg-accent/50 transition-all duration-200 hover:scale-105">
              <img
                v-if="heroStore.getHeroImageURL(hero.id, 'img')"
                :src="heroStore.getHeroImageURL(hero.id, 'img')"
                :alt="hero.localized_name"
                class="w-full h-full object-cover"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
              <div class="absolute bottom-2 left-2 right-2">
                <h3 class="text-white font-medium text-sm truncate group-hover:text-primary-foreground">
                  {{ hero.localized_name }}
                </h3>
                <div class="flex items-center gap-1 mt-1">
                  <Badge variant="secondary" class="text-xs px-1 py-0">
                    {{ hero.primary_attr.toUpperCase() }}
                  </Badge>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- No results -->
        <div v-if="!heroStore.isLoadingConstants && !heroStore.constantsError && filteredHeroes.length === 0" class="text-center py-12">
          <Search class="h-12 w-12 mx-auto text-muted-foreground mb-4" />
          <h3 class="text-lg font-semibold mb-2">No Heroes Found</h3>
          <p class="text-muted-foreground">Try adjusting your search terms</p>
        </div>
      </CardContent>
    </Card>

    <!-- Hero Detail Sheet -->
    <Sheet v-model:open="isSheetOpen">
      <SheetContent class="w-full sm:max-w-lg overflow-y-auto">
        <div v-if="selectedHero">
          <SheetHeader class="space-y-4">
            <div class="flex items-center space-x-4">
              <img
                v-if="heroStore.getHeroImageURL(selectedHero.id, 'img')"
                :src="heroStore.getHeroImageURL(selectedHero.id, 'img')"
                :alt="selectedHero.localized_name"
                class="h-16 w-16 rounded-lg object-cover border"
              />
              <div class="flex-1">
                <SheetTitle class="text-2xl">{{ selectedHero.localized_name }}</SheetTitle>
                <SheetDescription class="text-base">
                  {{ selectedHero.name }}
                </SheetDescription>
                <div class="flex items-center gap-2 mt-2">
                  <Badge>{{ selectedHero.primary_attr }} Hero</Badge>
                  <Badge variant="outline">{{ selectedHero.attack_type }}</Badge>
                </div>
              </div>
            </div>
          </SheetHeader>

          <div class="space-y-6 mt-6">
            <!-- Roles -->
            <div>
              <h3 class="font-semibold mb-3 text-foreground">Roles</h3>
              <div class="flex flex-wrap gap-2">
                <Badge v-for="role in selectedHero.roles" :key="role" variant="secondary" class="flex items-center gap-1">
                  <component :is="getRoleIcon(role)" class="h-3 w-3" />
                  {{ role }}
                </Badge>
              </div>
            </div>

            <!-- Meta Information -->
            <div>
              <h3 class="font-semibold mb-3 text-foreground">Current Meta</h3>
              <Card>
                <CardContent class="pt-4">
                  <div class="grid grid-cols-2 gap-4 mb-4">
                    <div class="text-center">
                      <div class="text-2xl font-bold text-green-600">{{ getHeroStats(selectedHero.id).winRate }}%</div>
                      <div class="text-sm text-muted-foreground">Win Rate</div>
                    </div>
                    <div class="text-center">
                      <div class="text-2xl font-bold text-blue-600">{{ getHeroStats(selectedHero.id).pickRate }}%</div>
                      <div class="text-sm text-muted-foreground">Pick Rate</div>
                    </div>
                  </div>
                  <div class="text-center">
                    <Badge :class="getTierColor(getHeroStats(selectedHero.id).metaRank.split('-')[0])" class="text-white">
                      {{ getHeroStats(selectedHero.id).metaRank }}
                    </Badge>
                    <p class="text-sm text-muted-foreground mt-2">
                      {{ getHeroStats(selectedHero.id).metaDescription }}
                    </p>
                  </div>
                </CardContent>
              </Card>
            </div>

            <!-- Farm Goals -->
            <div>
              <h3 class="font-semibold mb-3 text-foreground">Farm Goals</h3>
              <div class="space-y-3">
                <Card>
                  <CardContent class="pt-4">
                    <h4 class="font-medium mb-2">10 Minutes</h4>
                    <p class="text-sm text-muted-foreground">{{ getHeroStats(selectedHero.id).farmGoals['10min'] }}</p>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent class="pt-4">
                    <h4 class="font-medium mb-2">20 Minutes</h4>
                    <p class="text-sm text-muted-foreground">{{ getHeroStats(selectedHero.id).farmGoals['20min'] }}</p>
                  </CardContent>
                </Card>
              </div>
            </div>

            <!-- Popular Items -->
            <div>
              <h3 class="font-semibold mb-3 text-foreground">Popular Items</h3>
              <div class="space-y-2">
                <div v-for="item in getHeroStats(selectedHero.id).popularItems" :key="item.name" 
                     class="flex items-center justify-between p-3 rounded-lg border bg-card">
                  <span class="font-medium">{{ item.name }}</span>
                  <Badge variant="secondary">{{ item.pickRate }}%</Badge>
                </div>
              </div>
            </div>

            <!-- Average Stats -->
            <div>
              <h3 class="font-semibold mb-3 text-foreground">Average Performance</h3>
              <Card>
                <CardContent class="pt-4">
                  <div class="grid grid-cols-2 gap-4">
                    <div>
                      <div class="text-lg font-semibold">{{ getHeroStats(selectedHero.id).averageKDA }}</div>
                      <div class="text-sm text-muted-foreground">Average K/D/A</div>
                    </div>
                    <div>
                      <div class="text-lg font-semibold">{{ getHeroStats(selectedHero.id).averageGPM }}</div>
                      <div class="text-sm text-muted-foreground">Average GPM</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  </div>
</template>

<style scoped>
/* Add any custom styles if needed */
</style>
