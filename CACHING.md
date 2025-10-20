# Dota 2 Project - Data Caching Implementation

## Overview

This document describes the comprehensive caching system implemented to reduce API calls and improve performance for the Dota 2 analytics application.

## Frontend Caching Strategy

### 1. Enhanced Hero Store with Persistent Storage
- **Location**: `stores/heroStore.ts`
- **Features**:
  - localStorage persistence (24 hours TTL)
  - Version control for cache invalidation
  - Automatic cache validation
  - Force refresh capability
  - Fallback to API if cache is invalid

### 2. Centralized Cache Management
- **Location**: `stores/cacheStore.ts`
- **Features**:
  - Multi-level caching (memory + localStorage)
  - Configurable TTL per data type
  - Automatic cleanup of expired entries
  - Cache statistics and monitoring
  - Type-safe cache operations

### 3. Data Fetching Composables
- **Location**: `composables/useData.ts`
- **Features**:
  - Unified data fetching interface
  - Automatic cache integration
  - Type-safe API responses
  - Error handling and recovery

### 4. Cache Configuration

| Data Type | TTL | Description |
|-----------|-----|-------------|
| Player Profiles | 30 minutes | Basic player information |
| Win/Loss Data | 1 hour | Player win/loss statistics |
| Player Heroes | 2 hours | Hero performance stats |
| Recent Matches | 10 minutes | Latest match data |
| Hero Constants | 24 hours | Static hero metadata |
| Search Results | 5 minutes | Player search results |

## Backend Caching Strategy

### 1. In-Memory Cache System
- **Location**: `backend/app/main.py`
- **Features**:
  - Simple in-memory cache with TTL
  - Automatic cleanup of expired entries
  - Cache statistics endpoint
  - Manual cache clearing

### 2. Cached Endpoints

All OpenDota proxy endpoints now include caching:
- `/api/v1/opendota_proxy/players/{account_id}` - Player profiles
- `/api/v1/opendota_proxy/players/{account_id}/wl` - Win/loss data
- `/api/v1/opendota_proxy/players/{account_id}/heroes` - Player heroes
- `/api/v1/opendota_proxy/constants/heroes` - Hero constants
- `/api/v1/opendota_proxy/search` - Player search

### 3. Cache Management Endpoints
- `GET /api/v1/cache/stats` - Get cache statistics
- `DELETE /api/v1/cache/clear` - Clear all cache

## How It Works

### First Load (No Cache)
1. User visits a player page
2. Frontend checks localStorage cache - miss
3. Frontend makes API request to backend
4. Backend checks memory cache - miss
5. Backend fetches from OpenDota API
6. Backend caches response and returns to frontend
7. Frontend caches response in localStorage and displays data

### Subsequent Loads (Cache Hit)
1. User visits same player page or refreshes
2. Frontend checks localStorage cache - hit!
3. Data is immediately available, no API calls needed

### Cache Expiration
1. Cache entries automatically expire based on TTL
2. Next request will fetch fresh data from API
3. New data replaces expired cache entries

## Benefits

### Performance Improvements
- **Instant page loads** for cached data
- **Reduced API calls** by up to 90% for repeated visits
- **Lower bandwidth usage** for users
- **Improved user experience** with faster navigation

### API Rate Limiting Protection
- **Reduced OpenDota API calls** prevents rate limiting
- **Backend caching** reduces external API dependency
- **Smart cache invalidation** ensures data freshness

### Offline Resilience
- **localStorage persistence** allows some data to be available offline
- **Graceful degradation** when API is unavailable
- **Cached hero constants** always available

## Usage Examples

### Using the New Data Composables

```typescript
// In a Vue component
import { usePlayerData, useHeroData } from '@/composables/useData';

const { fetchPlayerProfile, fetchPlayerWinLoss } = usePlayerData();
const { ensureHeroConstants, getHeroById } = useHeroData();

// These will automatically use cache when available
const playerData = await fetchPlayerProfile(accountId);
const wlData = await fetchPlayerWinLoss(accountId);
```

### Cache Management

```typescript
// Access cache store
import { useCacheStore } from '@/stores/cacheStore';

const cacheStore = useCacheStore();

// Clear specific cache
cacheStore.clear('player_profile', { accountId: 12345 });

// Get cache statistics
const stats = cacheStore.getStats();

// Clean expired entries
cacheStore.cleanupExpired();
```

### Force Refresh Data

```typescript
// Refresh hero constants
import { useHeroStore } from '@/stores/heroStore';

const heroStore = useHeroStore();
await heroStore.fetchHeroConstants(true); // Force refresh
```

## Cache Management Interface

Visit `/cache-management` to:
- View cache statistics
- Clear all cache
- Refresh hero constants
- Clean expired entries
- Monitor cache performance

## Migration Guide

### From Old Implementation
1. Replace direct `$fetch` calls with composable functions
2. Remove manual cache checking logic
3. Use new reactive data patterns
4. Update error handling to use composable errors

### Example Migration

**Before:**
```typescript
const { data, pending, error } = useFetch(`/api/players/${id}`);
```

**After:**
```typescript
const { fetchPlayerProfile } = usePlayerData();
const playerData = ref(null);
const isLoading = ref(false);

const loadData = async () => {
  isLoading.value = true;
  try {
    playerData.value = await fetchPlayerProfile(id);
  } finally {
    isLoading.value = false;
  }
};
```

## Monitoring and Debugging

### Frontend Debugging
- Check browser DevTools Console for cache hit/miss logs
- Inspect localStorage for cached data
- Use `/cache-management` page for statistics

### Backend Debugging
- Check server logs for cache hit/miss messages
- Use `GET /api/v1/cache/stats` for cache statistics
- Monitor reduced OpenDota API calls

## Future Enhancements

### Planned Features
1. **Redis backend cache** for production scalability
2. **Cache warming** strategies for popular players
3. **Intelligent prefetching** based on user behavior
4. **Cache analytics** and performance metrics
5. **Background refresh** for critical data
6. **Cross-tab cache synchronization**

### Configuration Options
1. **Environment-based TTL** settings
2. **User preferences** for cache behavior
3. **Admin cache controls** for operators

## Troubleshooting

### Common Issues

1. **Stale Data**: Clear cache manually or wait for TTL expiration
2. **High Memory Usage**: Reduce cache TTL or clear cache more frequently
3. **API Errors**: Check if OpenDota API is accessible
4. **Cache Misses**: Verify cache keys and TTL configuration

### Cache Reset
If you encounter issues, you can reset all cache:
1. Visit `/cache-management`
2. Click "Clear All Cache"
3. Refresh the application

## Performance Metrics

### Expected Improvements
- **Page Load Time**: 80-90% faster for cached data
- **API Calls**: 70-90% reduction in external API calls
- **Bandwidth**: 60-80% reduction in data transfer
- **User Experience**: Near-instant navigation between cached pages

This caching implementation provides a robust foundation for scaling the Dota 2 analytics application while maintaining excellent performance and user experience.