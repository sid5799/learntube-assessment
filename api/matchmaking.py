from fastapi import APIRouter, HTTPException
from schemas.matchmaking import MatchRequest, MatchResponse
from services.matchmaking_service import handle_matchmaking

router = APIRouter()

@router.post("/matchmaking", response_model=MatchResponse)
async def match_player(match_request: MatchRequest):
    match = await handle_matchmaking(match_request)
    if not match:
        raise HTTPException(status_code=202, detail="Waiting for teammate or opponent")
    return match
