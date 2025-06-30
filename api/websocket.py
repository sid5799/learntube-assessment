from fastapi import WebSocket, WebSocketDisconnect, APIRouter
# from utils.websocket_manager import connection_manager

router = APIRouter()

@router.websocket("/ws/{match_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, match_id: str, user_id: str):
    await connection_manager.connect(match_id, user_id, websocket)
    try:
        while True:
            await websocket.receive_text()  # or use pings for keep-alive
    except WebSocketDisconnect:
        await connection_manager.disconnect(match_id, user_id)
