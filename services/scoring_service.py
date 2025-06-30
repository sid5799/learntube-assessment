import time
import uuid
import json
from typing import Optional
from redis import Redis
from schemas.scoring import AnswerSubmit, ScoreResponse
from utils.websocket_manager import connection_manager
from utils.db import persist_answer_result, get_correct_answer

redis = Redis(host='localhost', port=6379, decode_responses=True)

SCORE_KEY_PREFIX = "quiz:score:"
ANSWER_LOG_PREFIX = "quiz:answered:"

BASE_SCORE = 10

async def submit_answer(submit: AnswerSubmit) -> Optional[ScoreResponse]:
    match_id = str(submit.match_id)
    user_id = str(submit.user_id)
    question_id = str(submit.question_id)
    key_score_user = f"{SCORE_KEY_PREFIX}{match_id}:user:{user_id}"
    key_score_team = f"{SCORE_KEY_PREFIX}{match_id}:team"

    # Prevent double answering
    answered_key = f"{ANSWER_LOG_PREFIX}{match_id}:{user_id}:{question_id}"
    if redis.exists(answered_key):
        return None

    # Get correct answer
    correct_answer = await get_correct_answer(question_id)
    is_correct = correct_answer.lower() == submit.answer.lower()

    # Calculate score
    response_time = time.time() - submit.timestamp
    bonus = max(0, 5 - response_time)
    score_gain = BASE_SCORE + int(bonus) if is_correct else 0

    # Update scores in Redis (incr for atomicity)
    user_score = redis.incrby(key_score_user, score_gain)
    team_score = redis.incrby(key_score_team, score_gain)

    # Store answer log (set TTL = match duration)
    redis.set(answered_key, 1, ex=120)

    # Push to teammates via WebSocket
    await connection_manager.broadcast_to_match(
        match_id,
        {
            "type": "score_update",
            "user_id": user_id,
            "correct": is_correct,
            "user_score": user_score,
            "team_score": team_score
        }
    )

    # Persist for post-match results (async)
    await persist_answer_result(submit, is_correct, score_gain)

    return ScoreResponse(
        correct=is_correct,
        user_score=user_score,
        team_score=team_score
    )
