from pydantic import BaseModel
from uuid import UUID

class AnswerSubmit(BaseModel):
    match_id: UUID
    user_id: UUID
    question_id: UUID
    answer: str
    timestamp: float

class ScoreResponse(BaseModel):
    correct: bool
    user_score: int
    team_score: int
