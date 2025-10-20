import { defineStore } from 'pinia';

interface CachedItem<T = any> {
  data: T;
  timestamp: number;
  version: string;
  ttl: number; // Time to live in milliseconds
}

interface CacheConfig {
  version: string;
  ttl: number;
}

const DEFAULT_CACHE_CONFIGS: Record<string, CacheConfig> = {
  'player_profile': { version: '1.0', ttl: 30 * 60 * 1000 }, // 30 minutes
  'player_winloss': { version: '1.0', ttl: 60 * 60 * 1000 }, // 1 hour
  'player_heroes': { version: '1.0', ttl: 2 * 60 * 60 * 1000 }, // 2 hours
  'player_matches': { version: '1.0', ttl: 10 * 60 * 1000 }, // 10 minutes
  'hero_constants': { version: '1.0', ttl: 24 * 60 * 60 * 1000 }, // 24 hours
  'search_results': { version: '1.0', ttl: 5 * 60 * 1000 }, // 5 minutes
};

export const useCacheStore = defineStore('cacheStore', {
  state: () => ({
    cache: new Map<string, CachedItem>(),
  }),

  getters: {
    isCacheValid: (state) => {
      return (key: string): boolean => {
        const item = state.cache.get(key);
        if (!item) return false;
        
        const config = DEFAULT_CACHE_CONFIGS[key.split(':')[0]];
        if (!config) return false;
        
        return (
          item.version === config.version &&
          Date.now() - item.timestamp < item.ttl
        );
      };
    },
  },

  actions: {
    // Generate cache key with parameters
    generateKey(type: string, params: Record<string, any> = {}): string {
      const paramString = Object.keys(params)
        .sort()
        .map(key => `${key}=${params[key]}`)
        .join('&');
      return paramString ? `${type}:${paramString}` : type;
    },

    // Get cached data
    get<T>(type: string, params: Record<string, any> = {}): T | null {
      if (process.server) return null;

      const key = this.generateKey(type, params);
      
      // Try memory cache first
      if (this.isCacheValid(key)) {
        console.log(`Cache hit (memory): ${key}`);
        return this.cache.get(key)?.data as T;
      }

      // Try localStorage
      try {
        const stored = localStorage.getItem(`cache:${key}`);
        if (stored) {
          const item: CachedItem<T> = JSON.parse(stored);
          const config = DEFAULT_CACHE_CONFIGS[type];
          
          if (
            config &&
            item.version === config.version &&
            Date.now() - item.timestamp < item.ttl
          ) {
            // Restore to memory cache
            this.cache.set(key, item);
            console.log(`Cache hit (localStorage): ${key}`);
            return item.data;
          } else {
            // Remove expired cache
            localStorage.removeItem(`cache:${key}`);
          }
        }
      } catch (error) {
        console.error(`Error reading cache for ${key}:`, error);
      }

      return null;
    },

    // Set cached data
    set<T>(type: string, data: T, params: Record<string, any> = {}): void {
      if (process.server) return;

      const config = DEFAULT_CACHE_CONFIGS[type];
      if (!config) {
        console.warn(`No cache config found for type: ${type}`);
        return;
      }

      const key = this.generateKey(type, params);
      const item: CachedItem<T> = {
        data,
        timestamp: Date.now(),
        version: config.version,
        ttl: config.ttl,
      };

      // Store in memory
      this.cache.set(key, item);

      // Store in localStorage
      try {
        localStorage.setItem(`cache:${key}`, JSON.stringify(item));
        console.log(`Cache set: ${key}`);
      } catch (error) {
        console.error(`Error storing cache for ${key}:`, error);
      }
    },

    // Clear specific cache
    clear(type: string, params: Record<string, any> = {}): void {
      const key = this.generateKey(type, params);
      this.cache.delete(key);
      
      if (!process.server) {
        localStorage.removeItem(`cache:${key}`);
        console.log(`Cache cleared: ${key}`);
      }
    },

    // Clear all cache
    clearAll(): void {
      this.cache.clear();
      
      if (!process.server) {
        // Clear all cache items from localStorage
        const keys = Object.keys(localStorage).filter(key => key.startsWith('cache:'));
        keys.forEach(key => localStorage.removeItem(key));
        console.log('All cache cleared');
      }
    },

    // Clear expired cache entries
    cleanupExpired(): void {
      const now = Date.now();
      
      // Clean memory cache
      for (const [key, item] of this.cache.entries()) {
        if (now - item.timestamp >= item.ttl) {
          this.cache.delete(key);
        }
      }

      // Clean localStorage cache
      if (!process.server) {
        const keys = Object.keys(localStorage).filter(key => key.startsWith('cache:'));
        keys.forEach(key => {
          try {
            const item: CachedItem = JSON.parse(localStorage.getItem(key) || '');
            if (now - item.timestamp >= item.ttl) {
              localStorage.removeItem(key);
            }
          } catch (error) {
            // Remove corrupted cache items
            localStorage.removeItem(key);
          }
        });
      }
    },

    // Get cache statistics
    getStats(): { memoryItems: number; localStorageItems: number; totalSize: string } {
      const memoryItems = this.cache.size;
      let localStorageItems = 0;
      let totalSize = 0;

      if (!process.server) {
        const keys = Object.keys(localStorage).filter(key => key.startsWith('cache:'));
        localStorageItems = keys.length;
        totalSize = keys.reduce((size, key) => {
          return size + (localStorage.getItem(key)?.length || 0);
        }, 0);
      }

      return {
        memoryItems,
        localStorageItems,
        totalSize: `${(totalSize / 1024).toFixed(2)} KB`,
      };
    },
  },
});