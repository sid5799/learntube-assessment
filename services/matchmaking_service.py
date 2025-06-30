import uuid
import asyncio
import json
from typing import Optional
from schemas.matchmaking import MatchRequest, MatchResponse
from redis import Redis

redis = Redis(host='localhost', port=6379, decode_responses=True)

TEAM_QUEUE_PREFIX = "quiz:team_queue:"
PLAYER_QUEUE_PREFIX = "quiz:player_queue:"

async def handle_matchmaking(match_request: MatchRequest) -> Optional[MatchResponse]:
    subject = match_request.subject
    user_id = str(match_request.user_id)

    player_queue_key = PLAYER_QUEUE_PREFIX + subject
    teammate_id = redis.lpop(player_queue_key)

    if teammate_id:
        team_id = str(uuid.uuid4())
        team_data = {"team_id": team_id, "players": [teammate_id, user_id]}
        team_queue_key = TEAM_QUEUE_PREFIX + subject

        opponent_team_data = redis.lpop(team_queue_key)
        
        if not opponent_team_data:
            redis.rpush(team_queue_key, json.dumps(team_data))
            return None
        else:
            opponent_team = json.loads(opponent_team_data)
            match_id = str(uuid.uuid4())
            return MatchResponse(
                match_id=match_id,
                team_id=team_id,
                opponent_team_id=opponent_team["team_id"]
            )
    else:
        redis.rpush(player_queue_key, user_id)
        return None  
