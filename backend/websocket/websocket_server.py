import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

clients = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    print("New client connected")
    try:
        while True:
            data = await websocket.receive_text() 
            print(f"Received data from client: {data}")
            await send_to_clients(data)
    except WebSocketDisconnect:
        print("Client disconnected")
        clients.remove(websocket)

async def send_to_clients(message: str):
    print(f"Broadcasting message to {len(clients)} client(s): {message}")
    if clients:
        for client in clients:
            try:
                await client.send_text(message)
            except Exception as e:
                print(f"Error sending message to client: {e}")

async def send_data_to_websocket(data):
    message = json.dumps(data)
    await send_to_clients(message)
