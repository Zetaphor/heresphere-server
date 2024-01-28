import asyncio
import websockets
from logger_config import get_logger

logger = get_logger()
connected_clients = set()

async def broadcast(message):
    global connected_clients
    for websocket in set(connected_clients):
        try:
            await websocket.send(message)
        except Exception as e:
            logger.error(f"Error sending message to WebSocket: {e}")

async def websocket_server(websocket, path):
    global connected_clients
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            logger.debug(f"Received message from WebSocket: {message}")
            await websocket.send(f"Echo: {message}")
    finally:
        connected_clients.remove(websocket)

def start_websocket_server_thread(port):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_websocket_server(port))

async def start_websocket_server(port):
    server = await websockets.serve(websocket_server, '0.0.0.0', port)
    await server.wait_closed()

