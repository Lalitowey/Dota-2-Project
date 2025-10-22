"""
API v1 router combining all endpoint routers.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import players, heroes, matches, cache

router = APIRouter()

# Include all endpoint routers
router.include_router(players.router, tags=["players"])
router.include_router(heroes.router, tags=["heroes"])
router.include_router(matches.router, tags=["matches"])
router.include_router(cache.router, tags=["cache"])
