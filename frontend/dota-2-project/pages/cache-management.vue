<script setup lang="ts">
import { ref, computed } from 'vue';
import { useCacheStore } from '@/stores/cacheStore';
import { useHeroStore } from '@/stores/heroStore';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';

const cacheStore = useCacheStore();
const heroStore = useHeroStore();

const stats = computed(() => cacheStore.getStats());
const showSuccessMessage = ref(false);

const clearAllCache = () => {
  cacheStore.clearAll();
  heroStore.clearCache();
  showSuccessMessage.value = true;
  setTimeout(() => {
    showSuccessMessage.value = false;
  }, 3000);
};

const refreshHeroConstants = async () => {
  await heroStore.fetchHeroConstants(true);
  showSuccessMessage.value = true;
  setTimeout(() => {
    showSuccessMessage.value = false;
  }, 3000);
};

const cleanupExpired = () => {
  cacheStore.cleanupExpired();
  showSuccessMessage.value = true;
  setTimeout(() => {
    showSuccessMessage.value = false;
  }, 3000);
};
</script>

<template>
  <div class="container mx-auto py-8 px-4">
    <h1 class="text-3xl font-bold mb-6">Cache Management</h1>
    
    <Alert v-if="showSuccessMessage" class="mb-6">
      <AlertDescription>Cache operation completed successfully!</AlertDescription>
    </Alert>

    <div class="grid gap-6 md:grid-cols-2">
      <!-- Cache Statistics -->
      <Card>
        <CardHeader>
          <CardTitle>Cache Statistics</CardTitle>
        </CardHeader>
        <CardContent class="space-y-4">
          <div>
            <p class="text-sm font-medium text-muted-foreground">Memory Cache Items</p>
            <p class="text-2xl font-bold">{{ stats.memoryItems }}</p>
          </div>
          <div>
            <p class="text-sm font-medium text-muted-foreground">LocalStorage Cache Items</p>
            <p class="text-2xl font-bold">{{ stats.localStorageItems }}</p>
          </div>
          <div>
            <p class="text-sm font-medium text-muted-foreground">Total Storage Size</p>
            <p class="text-2xl font-bold">{{ stats.totalSize }}</p>
          </div>
          <div>
            <p class="text-sm font-medium text-muted-foreground">Hero Constants Status</p>
            <Badge v-if="heroStore.heroConstants" variant="default">Loaded</Badge>
            <Badge v-else-if="heroStore.isLoadingConstants" variant="secondary">Loading...</Badge>
            <Badge v-else variant="destructive">Not Loaded</Badge>
          </div>
          <div v-if="heroStore.isCacheValid">
            <p class="text-sm font-medium text-muted-foreground">Hero Cache Status</p>
            <Badge variant="default">Valid</Badge>
          </div>
        </CardContent>
      </Card>

      <!-- Cache Actions -->
      <Card>
        <CardHeader>
          <CardTitle>Cache Actions</CardTitle>
        </CardHeader>
        <CardContent class="space-y-4">
          <div>
            <h3 class="text-sm font-medium mb-2">General Cache</h3>
            <div class="space-y-2">
              <Button @click="cleanupExpired" variant="outline" class="w-full">
                Clean Expired Cache
              </Button>
              <Button @click="clearAllCache" variant="destructive" class="w-full">
                Clear All Cache
              </Button>
            </div>
          </div>
          
          <div>
            <h3 class="text-sm font-medium mb-2">Hero Data</h3>
            <div class="space-y-2">
              <Button @click="refreshHeroConstants" variant="outline" class="w-full">
                Refresh Hero Constants
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Cache Information -->
    <Card class="mt-6">
      <CardHeader>
        <CardTitle>Cache Configuration</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          <div>
            <p class="text-sm font-medium text-muted-foreground">Player Profiles</p>
            <p class="text-sm">30 minutes TTL</p>
          </div>
          <div>
            <p class="text-sm font-medium text-muted-foreground">Win/Loss Data</p>
            <p class="text-sm">1 hour TTL</p>
          </div>
          <div>
            <p class="text-sm font-medium text-muted-foreground">Player Heroes</p>
            <p class="text-sm">2 hours TTL</p>
          </div>
          <div>
            <p class="text-sm font-medium text-muted-foreground">Recent Matches</p>
            <p class="text-sm">10 minutes TTL</p>
          </div>
          <div>
            <p class="text-sm font-medium text-muted-foreground">Hero Constants</p>
            <p class="text-sm">24 hours TTL</p>
          </div>
          <div>
            <p class="text-sm font-medium text-muted-foreground">Search Results</p>
            <p class="text-sm">5 minutes TTL</p>
          </div>
        </div>
      </CardContent>
    </Card>
  </div>
</template>