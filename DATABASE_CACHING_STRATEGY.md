# Database + Cache Architecture for Dota 2 Project

## Overview
Adding PostgreSQL would create a three-tier data strategy:
1. **Frontend Cache** (immediate response)
2. **Backend Cache** (fast API response) 
3. **PostgreSQL Database** (persistent storage + data enrichment)
4. **OpenDota API** (background synchronization)

## Backend Changes

### New Database Models
```python
# models.py
from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PlayerProfile(Base):
    __tablename__ = "player_profiles"
    
    account_id = Column(Integer, primary_key=True)
    personaname = Column(String)
    name = Column(String)
    avatarfull = Column(String)
    profileurl = Column(String)
    rank_tier = Column(Integer)
    competitive_rank = Column(Integer)
    last_login = Column(DateTime)
    
    # Metadata
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    last_sync = Column(DateTime)

class PlayerWinLoss(Base):
    __tablename__ = "player_winloss"
    
    account_id = Column(Integer, primary_key=True)
    win = Column(Integer)
    lose = Column(Integer)
    updated_at = Column(DateTime)

class HeroConstants(Base):
    __tablename__ = "hero_constants"
    
    hero_id = Column(Integer, primary_key=True)
    name = Column(String)
    localized_name = Column(String)
    primary_attr = Column(String)
    attack_type = Column(String)
    roles = Column(JSON)
    img = Column(String)
    icon = Column(String)
    updated_at = Column(DateTime)
```

### Enhanced Cache Strategy
```python
# Enhanced main.py with database integration

from sqlalchemy.orm import Session
from database import get_db
from models import PlayerProfile, PlayerWinLoss, HeroConstants
from datetime import datetime, timedelta

class DataService:
    def __init__(self, db: Session):
        self.db = db
        self.cache = cache  # Existing cache
    
    async def get_player_profile(self, account_id: int):
        # 1. Check cache first (fastest)
        cache_key = f"player_profile:{account_id}"
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data
        
        # 2. Check database (fast)
        db_profile = self.db.query(PlayerProfile).filter(
            PlayerProfile.account_id == account_id
        ).first()
        
        if db_profile and self._is_db_data_fresh(db_profile.last_sync, minutes=30):
            # Convert to dict and cache
            profile_data = self._model_to_dict(db_profile)
            self.cache.set(cache_key, profile_data, 30)
            return profile_data
        
        # 3. Fetch from API and update database
        return await self._fetch_and_store_profile(account_id)
    
    def _is_db_data_fresh(self, last_sync: datetime, minutes: int) -> bool:
        if not last_sync:
            return False
        return datetime.now() - last_sync < timedelta(minutes=minutes)
    
    async def _fetch_and_store_profile(self, account_id: int):
        # Fetch from OpenDota
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://api.opendota.com/api/players/{account_id}")
            api_data = response.json()
        
        # Update/create database record
        db_profile = self.db.query(PlayerProfile).filter(
            PlayerProfile.account_id == account_id
        ).first()
        
        if db_profile:
            # Update existing
            for key, value in api_data.items():
                if hasattr(db_profile, key):
                    setattr(db_profile, key, value)
            db_profile.last_sync = datetime.now()
        else:
            # Create new
            db_profile = PlayerProfile(**api_data, last_sync=datetime.now())
            self.db.add(db_profile)
        
        self.db.commit()
        
        # Cache the result
        cache_key = f"player_profile:{account_id}"
        self.cache.set(cache_key, api_data, 30)
        
        return api_data

# Updated endpoints
@app.get("/api/v1/opendota_proxy/players/{account_id}")
async def get_player_profile(account_id: int, db: Session = Depends(get_db)):
    service = DataService(db)
    return await service.get_player_profile(account_id)
```

## Frontend Changes (Minimal)

The frontend caching system we implemented would remain largely unchanged:

```typescript
// composables/useData.ts - No major changes needed
export const usePlayerData = () => {
  const cacheStore = useCacheStore();
  
  const fetchPlayerProfile = async (accountId: string | number): Promise<PlayerData> => {
    // Same frontend cache logic
    const cachedData = cacheStore.get<PlayerData>('player_profile', { accountId });
    if (cachedData) {
      return cachedData;
    }

    // Still calls same backend endpoint (which now has DB backing)
    const data = await $fetch<PlayerData>(`${API_BASE_URL}/api/v1/opendota_proxy/players/${accountId}`);
    cacheStore.set('player_profile', data, { accountId });
    return data;
  };
  
  // ... rest remains the same
};
```

## New Capabilities with Database

### 1. Historical Data Tracking
```sql
-- Track player rank progression
CREATE TABLE player_rank_history (
    id SERIAL PRIMARY KEY,
    account_id INTEGER,
    rank_tier INTEGER,
    competitive_rank INTEGER,
    recorded_at TIMESTAMP DEFAULT NOW()
);

-- Track match history
CREATE TABLE player_matches (
    match_id BIGINT PRIMARY KEY,
    account_id INTEGER,
    hero_id INTEGER,
    kills INTEGER,
    deaths INTEGER,
    assists INTEGER,
    duration INTEGER,
    game_mode INTEGER,
    start_time TIMESTAMP,
    indexed_at TIMESTAMP DEFAULT NOW()
);
```

### 2. Data Analytics & Aggregations
```python
# New analytics endpoints possible
@app.get("/api/v1/analytics/player/{account_id}/rank-progression")
async def get_rank_progression(account_id: int, db: Session = Depends(get_db)):
    # Query historical rank data from database
    rank_history = db.query(PlayerRankHistory).filter(
        PlayerRankHistory.account_id == account_id
    ).order_by(PlayerRankHistory.recorded_at).all()
    
    return [{"date": r.recorded_at, "rank": r.rank_tier} for r in rank_history]

@app.get("/api/v1/analytics/heroes/meta-trends")
async def get_meta_trends(db: Session = Depends(get_db)):
    # Aggregate match data for meta analysis
    meta_data = db.execute("""
        SELECT hero_id, 
               COUNT(*) as games,
               AVG(CASE WHEN radiant_win = (player_slot < 128) THEN 1 ELSE 0 END) as win_rate
        FROM player_matches 
        WHERE start_time > NOW() - INTERVAL '7 days'
        GROUP BY hero_id
        ORDER BY games DESC
    """).fetchall()
    
    return meta_data
```

### 3. Background Data Synchronization
```python
# background_tasks.py
from celery import Celery

app = Celery('dota2_sync')

@app.task
def sync_player_data(account_id: int):
    """Background task to keep player data fresh"""
    # Update player profile, winloss, heroes, etc.
    pass

@app.task
def sync_hero_constants():
    """Daily task to update hero constants"""
    pass

@app.task
def analyze_meta_trends():
    """Hourly task to calculate meta statistics"""
    pass
```

## Migration Strategy

### Phase 1: Add Database Layer
1. Set up PostgreSQL
2. Create database models
3. Add database integration to existing endpoints
4. Keep current cache system intact

### Phase 2: Enhanced Features
1. Add historical data tracking
2. Implement analytics endpoints
3. Create background sync tasks
4. Add data validation and cleanup

### Phase 3: Optimization
1. Database query optimization
2. Advanced caching strategies
3. Data archiving policies
4. Performance monitoring

## Cache TTL Adjustments with Database

```typescript
// Updated cache configuration
const CACHE_CONFIG = {
  // Shorter TTLs since DB provides fast fallback
  'player_profile': 15,    // 15 minutes (was 30)
  'player_winloss': 30,    // 30 minutes (was 60) 
  'player_heroes': 60,     // 1 hour (was 2 hours)
  'player_matches': 5,     // 5 minutes (was 10)
  'hero_constants': 1440,  // 24 hours (unchanged)
  'search_results': 2,     // 2 minutes (was 5)
  
  // New analytics data
  'rank_progression': 60,  // 1 hour
  'meta_trends': 30,       // 30 minutes
  'player_analytics': 60,  // 1 hour
};
```

## Benefits of Database Integration

### 1. **Data Persistence**
- Survive server restarts
- Historical data tracking
- Backup and recovery

### 2. **Enhanced Analytics**
- Rank progression tracking
- Meta trend analysis
- Custom player statistics
- Cross-player comparisons

### 3. **Reduced API Dependency**
- Serve stale data when OpenDota is down
- Background sync keeps data fresh
- Rate limiting protection

### 4. **Performance**
- Database queries faster than API calls
- Complex aggregations possible
- Indexed searches

### 5. **New Features Possible**
- Player comparison tools
- Historical meta analysis
- Custom leaderboards
- Trend notifications

## Summary

Adding PostgreSQL would **enhance** rather than replace your current caching system:

- **Frontend cache** remains the same (instant responses)
- **Backend cache** becomes smaller/shorter TTL (database is fast fallback)
- **Database** provides persistence, analytics, and historical data
- **OpenDota API** becomes background sync rather than real-time dependency

The three-tier approach gives you the best of all worlds: instant responses, data persistence, and rich analytics capabilities!