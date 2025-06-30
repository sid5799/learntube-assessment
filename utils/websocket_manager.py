class WebSocketConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list] = {}

    async def connect(self, match_id: str, user_id: str, websocket):
        await websocket.accept()
        self.active_connections.setdefault(match_id, []).append(websocket)

    async def disconnect(self, match_id: str, user_id: str):
        # Clean up logic here
        pass

    async def broadcast_to_match(self, match_id: str, message: dict):
        for ws in self.active_connections.get(match_id, []):
            await ws.send_json(message)

connection_manager = WebSocketConnectionManager()
