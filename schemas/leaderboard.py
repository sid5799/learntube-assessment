from pydantic import BaseModel

class LeaderboardEntry(BaseModel):
    user_id: str
    username: str
    score: int
    rank: int
