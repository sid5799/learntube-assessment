from schemas.scoring import AnswerSubmit

async def get_correct_answer(question_id: str) -> str:
    # this will be fetched from pgsql where all questions/answers related to specific subjects are scored
    question_db = {
        "q1": "Paris",
        "q2": "Einstein",
        "q3": "Oxygen"
    }
    return question_db.get(question_id, "")


async def persist_answer_result(submit: AnswerSubmit, correct: bool, score: int):
    # insert match result to db here
    print(f"[DB] Persisting answer -> {submit.user_id}, Q: {submit.question_id}, Score: {score}")
