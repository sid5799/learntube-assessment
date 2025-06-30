from pydantic import BaseModel
from uuid import UUID

class MatchRequest(BaseModel):
    user_id: UUID
    subject: str

class MatchResponse(BaseModel):
    match_id: UUID
    team_id: UUID
    opponent_team_id: UUID
