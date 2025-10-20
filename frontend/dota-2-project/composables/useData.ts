import { useCacheStore } from '@/stores/cacheStore';
import { useHeroStore } from '@/stores/heroStore';

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
  loccountry_code?: string;
}

interface PlayerData {
  solo_competitive_rank?: number | null;
  competitive_rank?: number | null;
  rank_tier?: number | null;
  leaderboard_rank?: number | null;
  profile: PlayerProfile | null;
}

interface WinLossData {
  win: number;
  lose: number;
}

interface PlayerHeroStat {
  hero_id: number;
  last_played: number;
  games: number;
  win: number;
  with_games: number;
  with_win: number;
  against_games: number;
  against_win: number;
}

interface RecentMatch {
  match_id: number;
  player_slot: number;
  radiant_win: boolean;
  duration: number;
  game_mode: number;
  lobby_type: number;
  hero_id: number;
  start_time: number;
  version: number;
  kills: number;
  deaths: number;
  assists: number;
  skill?: number;
  xp_per_min?: number;
  gold_per_min?: number;
  hero_damage?: number;
  tower_damage?: number;
  hero_healing?: number;
  last_hits?: number;
  lane?: number;
  lane_role?: number;
  is_roaming?: boolean;
  cluster?: number;
  leaver_status?: number;
  party_size?: number;
}

export const usePlayerData = () => {
  const cacheStore = useCacheStore();
  const runtimeConfig = useRuntimeConfig();
  const API_BASE_URL = runtimeConfig.public.apiBaseUrl;

  const fetchPlayerProfile = async (accountId: string | number): Promise<PlayerData> => {
    const cachedData = cacheStore.get<PlayerData>('player_profile', { accountId });
    if (cachedData) {
      return cachedData;
    }

    try {
      const data = await $fetch<PlayerData>(`${API_BASE_URL}/api/v1/opendota_proxy/players/${accountId}`);
      cacheStore.set('player_profile', data, { accountId });
      return data;
    } catch (error) {
      console.error('Failed to fetch player profile:', error);
      throw error;
    }
  };

  const fetchPlayerWinLoss = async (accountId: string | number): Promise<WinLossData> => {
    const cachedData = cacheStore.get<WinLossData>('player_winloss', { accountId });
    if (cachedData) {
      return cachedData;
    }

    try {
      const data = await $fetch<WinLossData>(`${API_BASE_URL}/api/v1/opendota_proxy/players/${accountId}/wl`);
      cacheStore.set('player_winloss', data, { accountId });
      return data;
    } catch (error) {
      console.error('Failed to fetch player win/loss:', error);
      throw error;
    }
  };

  const fetchPlayerHeroes = async (accountId: string | number): Promise<PlayerHeroStat[]> => {
    const cachedData = cacheStore.get<PlayerHeroStat[]>('player_heroes', { accountId });
    if (cachedData) {
      return cachedData;
    }

    try {
      const data = await $fetch<PlayerHeroStat[]>(`${API_BASE_URL}/api/v1/opendota_proxy/players/${accountId}/heroes`);
      cacheStore.set('player_heroes', data, { accountId });
      return data;
    } catch (error) {
      console.error('Failed to fetch player heroes:', error);
      throw error;
    }
  };

  const fetchPlayerMatches = async (accountId: string | number, limit: number = 20): Promise<RecentMatch[]> => {
    const cachedData = cacheStore.get<RecentMatch[]>('player_matches', { accountId, limit });
    if (cachedData) {
      return cachedData;
    }

    try {
      const data = await $fetch<RecentMatch[]>(`${API_BASE_URL}/api/v1/opendota_proxy/players/${accountId}/recentMatches`);
      cacheStore.set('player_matches', data.slice(0, limit), { accountId, limit });
      return data.slice(0, limit);
    } catch (error) {
      console.error('Failed to fetch player matches:', error);
      throw error;
    }
  };

  const searchPlayers = async (query: string): Promise<any[]> => {
    if (!query.trim()) return [];
    
    const cachedData = cacheStore.get<any[]>('search_results', { query });
    if (cachedData) {
      return cachedData;
    }

    try {
      const data = await $fetch<any[]>(`${API_BASE_URL}/api/v1/opendota_proxy/search?q=${encodeURIComponent(query)}`);
      cacheStore.set('search_results', data, { query });
      return data;
    } catch (error) {
      console.error('Failed to search players:', error);
      throw error;
    }
  };

  return {
    fetchPlayerProfile,
    fetchPlayerWinLoss,
    fetchPlayerHeroes,
    fetchPlayerMatches,
    searchPlayers,
  };
};

export const useHeroData = () => {
  const heroStore = useHeroStore();
  
  const ensureHeroConstants = async (forceRefresh = false) => {
    await heroStore.fetchHeroConstants(forceRefresh);
  };

  const getHeroById = (heroId: string | number) => {
    return heroStore.getHeroById(heroId);
  };

  const getHeroImageURL = (heroId: string | number, type: 'img' | 'icon' = 'img') => {
    return heroStore.getHeroImageURL(heroId, type);
  };

  const getAllHeroes = () => {
    return heroStore.allHeroesArray;
  };

  return {
    ensureHeroConstants,
    getHeroById,
    getHeroImageURL,
    getAllHeroes,
    heroConstants: readonly(toRef(heroStore, 'heroConstants')),
    isLoading: readonly(toRef(heroStore, 'isLoadingConstants')),
    error: readonly(toRef(heroStore, 'constantsError')),
  };
};