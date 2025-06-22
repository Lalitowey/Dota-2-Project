
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


export const useHeroStore = defineStore('heroStore', {
  state: () => ({
    heroConstants: null as HeroConstantsMap | null,
    isLoadingConstants: false,
    constantsError: null as string | null,
    openDotaBaseUrl: 'https://cdn.cloudflare.steamstatic.com',
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
    }
  },

  actions: {
    async fetchHeroConstants() {
      if (this.heroConstants) {
        console.log('Hero constants already loaded.');
        return;
      }
      if (this.isLoadingConstants) {
        console.log('Hero constants are currently being fetched.');
        return;
      }

      this.isLoadingConstants = true;
      this.constantsError = null;
      console.log('Fetching hero constants...');

      try {

        const runtimeConfig = useRuntimeConfig();
        const API_BASE_URL = runtimeConfig.public.apiBaseUrl;

        const data = await $fetch<HeroConstantsMap>(`${API_BASE_URL}/api/v1/opendota_proxy/constants/heroes`);

        this.heroConstants = data;
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