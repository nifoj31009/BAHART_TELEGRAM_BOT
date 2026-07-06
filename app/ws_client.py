"""
Minimal Socket.IO client that connects, emits optional auth, and calls a callback
for every incoming event. The callback should be an async function accepting
(event: str, data: Any).
"""
import os
import asyncio
from dotenv import load_dotenv
import socketio

load_dotenv()

WS_URL = os.getenv("DATA_WS_URL")
WS_AUTH = os.getenv("WS_AUTH_TOKEN")
WS_ORIGIN = os.getenv("WS_ORIGIN")
WS_COOKIE = os.getenv("WS_COOKIE")


async def start_ws_client(on_event):
    """Start the Socket.IO client and run until disconnected. on_event(event, data) must be async."""
    if not WS_URL:
        raise RuntimeError("DATA_WS_URL is not set in environment")

    headers = {}
    if WS_ORIGIN:
        headers["Origin"] = WS_ORIGIN
    if WS_COOKIE:
        headers["Cookie"] = WS_COOKIE

    sio = socketio.AsyncClient(logger=False, engineio_logger=False)

    @sio.event
    async def connect():
        print("Connected to Socket.IO server")
        if WS_AUTH:
            try:
                await sio.emit("auth", {"sessionToken": WS_AUTH})
                print("Sent auth (sessionToken hidden)")
            except Exception as e:
                print("Failed to emit auth:", e)

    @sio.on("*")
    async def catch_all(event, data):
        # forward to callback
        try:
            await on_event(event, data)
        except Exception as e:
            print("on_event callback error:", e)

    @sio.event
    async def disconnect():
        print("Disconnected from server")

    try:
        await sio.connect(WS_URL, transports=["websocket"], headers=headers)
        print("Awaiting messages. Press Ctrl+C to stop.")
        await sio.wait()
    except Exception as e:
        print("Connection error:", e)
    finally:
        if sio.connected:
            await sio.disconnect()
