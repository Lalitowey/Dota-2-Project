
import { defineStore } from 'pinia';

export interface HeroConstantDetail {
  id: number;
  name: string;
  localized_name: string;
  primary_attr: string;
  attack_type: string;
  roles: string[];
  img: string;
  icon: string;
}
export type HeroConstantsMap = Record<string, HeroConstantDetail>;

interface CachedData {
  data: HeroConstantsMap;
  timestamp: number;
  version: string;
}

const CACHE_KEY = 'dota2_hero_constants';
const CACHE_VERSION = '1.0';
const CACHE_DURATION = 24 * 60 * 60 * 1000; // 24 hours in milliseconds

export const useHeroStore = defineStore('heroStore', {
  state: () => ({
    heroConstants: null as HeroConstantsMap | null,
    isLoadingConstants: false,
    constantsError: null as string | null,
    openDotaBaseUrl: 'https://cdn.cloudflare.steamstatic.com',
    lastFetched: null as number | null,
  }),

  getters: {
    getHeroById: (state) => {
      return (heroId: number | string): HeroConstantDetail | undefined => {
        if (!state.heroConstants) return undefined;
        return state.heroConstants[String(heroId)];
      };
    },
    getHeroImageURL: (state) => {
      return (heroId: number | string, type: 'img' | 'icon' = 'img'): string | undefined => {
        const hero = state.heroConstants?.[String(heroId)];
        if (!hero) return undefined;
        return `${state.openDotaBaseUrl}${hero[type]}`;
      };
    },
    allHeroesArray: (state): HeroConstantDetail[] => {
      if (!state.heroConstants) return [];
      return Object.values(state.heroConstants);
    },
    isCacheValid: (state): boolean => {
      if (!state.lastFetched) return false;
      return Date.now() - state.lastFetched < CACHE_DURATION;
    }
  },

  actions: {
    // Load data from localStorage if available and valid
    loadFromCache(): boolean {
      if (process.server) return false; // Skip on server-side
      
      try {
        const cached = localStorage.getItem(CACHE_KEY); // Cached data
        if (!cached) return false;

        const parsedCache: CachedData = JSON.parse(cached); 
        
        // Check cache validity
        if (
          parsedCache.version !== CACHE_VERSION ||
          Date.now() - parsedCache.timestamp > CACHE_DURATION
        ) {
          localStorage.removeItem(CACHE_KEY);
          return false;
        }

        this.heroConstants = parsedCache.data;
        this.lastFetched = parsedCache.timestamp;
        console.log('Hero constants loaded from cache:', Object.keys(parsedCache.data).length, 'heroes');
        return true;
      } catch (error) {
        console.error('Error loading hero constants from cache:', error);
        localStorage.removeItem(CACHE_KEY);
        return false;
      }
    },

    // Save data to localStorage
    saveToCache(data: HeroConstantsMap): void {
      if (process.server) return; // Skip on server-side
      
      try {
        const cacheData: CachedData = {
          data,
          timestamp: Date.now(),
          version: CACHE_VERSION
        };
        localStorage.setItem(CACHE_KEY, JSON.stringify(cacheData));
        this.lastFetched = cacheData.timestamp;
      } catch (error) {
        console.error('Error saving hero constants to cache:', error);
      }
    },

    // Clear cache and force refresh
    clearCache(): void {
      if (process.server) return;
      localStorage.removeItem(CACHE_KEY);
      this.heroConstants = null;
      this.lastFetched = null;
    },

    async fetchHeroConstants(forceRefresh: boolean = false) {
      // First, try to load from cache if not forcing refresh
      if (!forceRefresh && this.loadFromCache()) {
        return;
      }

      // Check if we already have valid data and don't need to force refresh
      if (!forceRefresh && this.heroConstants && this.isCacheValid) {
        console.log('Hero constants already loaded and cache is valid.');
        return;
      }

      if (this.isLoadingConstants) {
        console.log('Hero constants are currently being fetched.');
        return;
      }

      this.isLoadingConstants = true;
      this.constantsError = null;
      console.log('Fetching hero constants from API...');

      try {
        const runtimeConfig = useRuntimeConfig();
        const API_BASE_URL = runtimeConfig.public.apiBaseUrl;

        const data = await $fetch<HeroConstantsMap>(`${API_BASE_URL}/api/v1/opendota_proxy/constants/heroes`);

        this.heroConstants = data;
        this.saveToCache(data); // Save to localStorage
        console.log('Hero constants fetched successfully:', Object.keys(data).length, 'heroes');
      } catch (error: any) {
        console.error('Failed to fetch hero constants:', error);
        this.constantsError = error.data?.detail || error.message || 'Failed to load hero constants';
        this.heroConstants = null;
      } finally {
        this.isLoadingConstants = false;
      }
    },
  },
});