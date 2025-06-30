from fastapi import APIRouter, Query
from schemas.leaderboard import LeaderboardEntry
# from services.leaderboard_service import get_global_leaderboard, get_local_leaderboard

router = APIRouter()

@router.get("/leaderboard/global", response_model=list[LeaderboardEntry])
async def global_board(limit: int = Query(default=10)):
    return await get_global_leaderboard(limit)

@router.get("/leaderboard/location", response_model=list[LeaderboardEntry])
async def location_board(country: str, limit: int = Query(default=10)):
    return await get_local_leaderboard(country, limit)
