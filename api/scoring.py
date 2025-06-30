from fastapi import APIRouter, HTTPException
from schemas.scoring import AnswerSubmit, ScoreResponse
from services.scoring_service import submit_answer

router = APIRouter()

@router.post("/scoring/submit", response_model=ScoreResponse)
async def scoring_submit(answer: AnswerSubmit):
    result = await submit_answer(answer)
    if result is None:
        raise HTTPException(status_code=400, detail="Invalid match or expired session")
    return result
