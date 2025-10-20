// plugins/loadHeroConstants.ts
import { useHeroStore } from '@/stores/heroStore';
import { useCacheStore } from '@/stores/cacheStore';

export default defineNuxtPlugin(async (nuxtApp) => {
  const heroStore = useHeroStore();
  const cacheStore = useCacheStore();

  // Clean up expired cache entries on app start
  cacheStore.cleanupExpired();

  // Try to load hero constants from cache first
  if (!heroStore.heroConstants && !heroStore.isLoadingConstants) {
    console.log('Plugin: Attempting to load hero constants...');
    try {
      await heroStore.fetchHeroConstants();
    } catch (error) {
      console.error('Plugin: Error loading hero constants:', error);
    }
  } else if (heroStore.heroConstants) {
    console.log('Plugin: Hero constants already available.');
  } else if (heroStore.isLoadingConstants) {
    console.log('Plugin: Hero constants are already being loaded elsewhere.');
  }
});