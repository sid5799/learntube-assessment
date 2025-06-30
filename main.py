from fastapi import FastAPI
from api import matchmaking, scoring, leaderboard, websocket

app = FastAPI()

app.include_router(matchmaking.router, prefix="/api")
app.include_router(scoring.router, prefix="/api")
app.include_router(leaderboard.router, prefix="/api")
app.include_router(websocket.router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")