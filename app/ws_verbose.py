"""
Verbose test script: prints detailed connection information and incoming events.
Run this to debug the WS connection before wiring into Telegram.
"""
import asyncio
import os
import traceback
from dotenv import load_dotenv
import socketio

load_dotenv()
WS_URL = os.getenv("DATA_WS_URL")
WS_AUTH = os.getenv("WS_AUTH_TOKEN")
WS_ORIGIN = os.getenv("WS_ORIGIN")
WS_COOKIE = os.getenv("WS_COOKIE")

headers = {}
if WS_ORIGIN:
    headers['Origin'] = WS_ORIGIN
if WS_COOKIE:
    headers['Cookie'] = WS_COOKIE

print('Connecting to:', WS_URL)
print('Using headers keys:', list(headers.keys()))

sio = socketio.AsyncClient(logger=True, engineio_logger=True)

@sio.event
async def connect():
    print('--- connected ---')
    if WS_AUTH:
        try:
            await sio.emit('auth', {"sessionToken": WS_AUTH})
            print('Sent auth event (sessionToken hidden)')
        except Exception as e:
            print('Auth emit error:', e)

@sio.on('*')
async def catch_all(event, data):
    print('EVENT:', event, 'DATA:', data)

@sio.event
async def disconnect():
    print('--- disconnected ---')

async def main():
    try:
        await sio.connect(WS_URL, transports=['websocket'], headers=headers)
        print('Awaiting messages. Press Ctrl+C to stop.')
        await sio.wait()
    except Exception as e:
        print('=== CONNECT EXCEPTION ===')
        traceback.print_exc()
    finally:
        if sio and sio.connected:
            await sio.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
