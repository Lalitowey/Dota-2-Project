// plugins/loadHeroConstants.ts
import { useHeroStore } from '@/stores/heroStore';

export default defineNuxtPlugin(async (nuxtApp) => {
  const heroStore = useHeroStore();

  if (!heroStore.heroConstants && !heroStore.isLoadingConstants) {
    console.log('Plugin: Attempting to load hero constants...');
    try {
      await heroStore.fetchHeroConstants();
      // console.log('Plugin: Hero constants action finished.'); // to check heroStore.constantsError
    } catch (error) {
      // The fetchHeroConstants action should handle its own errors and update constantsError state
      console.error('Plugin: Error explicitly caught during fetchHeroConstants call:', error);
    }
  } else if (heroStore.heroConstants) {
    console.log('Plugin: Hero constants already available.');
  } else if (heroStore.isLoadingConstants) {
    console.log('Plugin: Hero constants are already being loaded elsewhere.');
  }
});