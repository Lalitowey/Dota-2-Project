// composables/usePlayerAnalytics.ts
import { useCacheStore } from '@/stores/cacheStore';

// TODO: [ ] Modularize this file for heroes & players separately

interface MatchPerformance {
  match_id: number;
  hero_id: number;
  kills: number;
  deaths: number;
  assists: number;
  gold_per_min: number;
  xp_per_min: number;
  duration: number;
  radiant_win: boolean;
  player_slot: number;
  start_time: number;
}

interface PerformanceTrend {
  avgKDA: number;
  avgGPM: number;
  avgXPM: number;
  recentWinRate: number;
  winStreak: number;
  lossStreak: number;
}

interface HeroPoolStats {
  hero_id: number;
  games: number;
  wins: number;
  winRate: number;
  lastPlayed: number;
  avgKDA: string;
}

export const usePlayerAnalytics = () => {
  const cacheStore = useCacheStore();
  const runtimeConfig = useRuntimeConfig();
  const API_BASE_URL = runtimeConfig.public.apiBaseUrl;

  /**
   * Fetch recent matches with detailed stats
   */
  const fetchRecentMatches = async (
    accountId: string | number,
    limit: number = 20
  ): Promise<MatchPerformance[]> => {
    const cacheKey = `recent_matches_${accountId}_${limit}`;
    const cached = cacheStore.get<MatchPerformance[]>('player_matches', { accountId, limit });
    
    if (cached) return cached;

    try {
      const data = await $fetch<MatchPerformance[]>(
        `${API_BASE_URL}/api/v1/opendota_proxy/players/${accountId}/matches`,
        { params: { limit } }
      );
      
      cacheStore.set('player_matches', data, { accountId, limit });
      return data;
    } catch (error) {
      console.error('Failed to fetch recent matches:', error);
      throw error;
    }
  };

  /**
   * Calculate performance trends from recent matches
   */
  const calculatePerformanceTrends = (matches: MatchPerformance[]): PerformanceTrend => {
    if (!matches.length) {
      return {
        avgKDA: 0,
        avgGPM: 0,
        avgXPM: 0,
        recentWinRate: 0,
        winStreak: 0,
        lossStreak: 0
      };
    }

    // Calculate averages
    const totalKills = matches.reduce((sum, m) => sum + m.kills, 0);
    const totalDeaths = matches.reduce((sum, m) => sum + m.deaths, 0);
    const totalAssists = matches.reduce((sum, m) => sum + m.assists, 0);
    const avgGPM = matches.reduce((sum, m) => sum + m.gold_per_min, 0) / matches.length;
    const avgXPM = matches.reduce((sum, m) => sum + m.xp_per_min, 0) / matches.length;
    
    const avgKDA = totalDeaths === 0 
      ? (totalKills + totalAssists) 
      : (totalKills + totalAssists) / totalDeaths;

    // Calculate win rate
    const wins = matches.filter(m => 
      (m.player_slot < 128 && m.radiant_win) || 
      (m.player_slot >= 128 && !m.radiant_win)
    ).length;
    const recentWinRate = (wins / matches.length) * 100;

    // Calculate streaks
    let winStreak = 0;
    let lossStreak = 0;
    for (const match of matches) {
      const won = (match.player_slot < 128 && match.radiant_win) || 
                  (match.player_slot >= 128 && !match.radiant_win);
      
      if (won) {
        winStreak++;
        lossStreak = 0;
      } else {
        lossStreak++;
        winStreak = 0;
      }
      
      if (winStreak > 0 || lossStreak > 0) break; // Only count current streak
    }

    return {
      avgKDA: Math.round(avgKDA * 100) / 100,
      avgGPM: Math.round(avgGPM),
      avgXPM: Math.round(avgXPM),
      recentWinRate: Math.round(recentWinRate * 10) / 10,
      winStreak,
      lossStreak
    };
  };

  /**
   * Analyze hero pool from player heroes data
   */
  const analyzeHeroPool = (
    heroStats: any[],
    limit: number = 10
  ): HeroPoolStats[] => {
    return heroStats
      .sort((a, b) => b.games - a.games)
      .slice(0, limit)
      .map(hero => ({
        hero_id: hero.hero_id,
        games: hero.games,
        wins: hero.win,
        winRate: Math.round((hero.win / hero.games) * 100 * 10) / 10,
        lastPlayed: hero.last_played,
        avgKDA: hero.games > 0 
          ? `${((hero.kills || 0) / hero.games).toFixed(1)}/${((hero.deaths || 0) / hero.games).toFixed(1)}/${((hero.assists || 0) / hero.games).toFixed(1)}`
          : 'N/A'
      }));
  };

  /**
   * Get quick scout summary for a player
   */
  const getQuickScoutSummary = async (accountId: string | number) => {
    try {
      const [profile, wlData, heroesData, recentMatches] = await Promise.all([
        $fetch(`${API_BASE_URL}/api/v1/opendota_proxy/players/${accountId}`),
        $fetch(`${API_BASE_URL}/api/v1/opendota_proxy/players/${accountId}/wl`),
        $fetch(`${API_BASE_URL}/api/v1/opendota_proxy/players/${accountId}/heroes`),
        fetchRecentMatches(accountId, 10)
      ]);

      const trends = calculatePerformanceTrends(recentMatches as MatchPerformance[]);
      const heroPool = analyzeHeroPool(heroesData as any[], 5);

      return {
        profile,
        wlData,
        trends,
        topHeroes: heroPool,
        recentForm: trends.winStreak > 0 ? 'hot' : trends.lossStreak > 2 ? 'cold' : 'neutral'
      };
    } catch (error) {
      console.error('Failed to fetch scout summary:', error);
      throw error;
    }
  };

  /**
   * Fetch hero statistics for meta analysis
   */
  const fetchHeroStats = async () => {
    const cached = cacheStore.get<any[]>('hero_stats', {});
    if (cached) return cached;

    try {
      const data = await $fetch<any[]>(
        `${API_BASE_URL}/api/v1/opendota_proxy/heroStats`
      );
      
      cacheStore.set('hero_stats', data, {}, 120); // Cache for 2 hours
      return data;
    } catch (error) {
      console.error('Failed to fetch hero stats:', error);
      throw error;
    }
  };

  /**
   * Get top meta heroes with filtering
   */
  const getMetaHeroes = async (limit: number = 20) => {
    const heroStats = await fetchHeroStats();
    
    return heroStats
      .map(hero => ({
        id: hero.id,
        name: hero.localized_name,
        pickRate: hero.pro_pick || 0,
        winRate: hero.pro_win ? (hero.pro_win / hero.pro_pick * 100) : 50,
        games: hero.pro_pick || 0
      }))
      .sort((a, b) => b.pickRate - a.pickRate)
      .slice(0, limit);
  };

  return {
    fetchRecentMatches,
    calculatePerformanceTrends,
    analyzeHeroPool,
    getQuickScoutSummary,
    fetchHeroStats,
    getMetaHeroes
  };
};