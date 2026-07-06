"""Entry point for the small Socket.IO -> Telegram scaffold.

This main file loads environment variables, starts the ws client, and forwards
incoming events to Telegram (if configured).

This is intentionally minimal so you can run and inspect behavior locally.
"""
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from app.ws_client import start_ws_client
from app.telegram_bot import TelegramNotifier


async def main():
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat = os.getenv("TELEGRAM_CHAT_ID")

    notifier = None
    if telegram_token and telegram_chat:
        notifier = TelegramNotifier(telegram_token, telegram_chat)
        print("Telegram notifier configured")
    else:
        print("Telegram notifier not configured (set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env to enable)")

    # callback called for every event from WS: (event, data)
    async def on_event(event, data):
        text = f"EVENT: {event} DATA: {data}"
        print(text)
        if notifier:
            # send message but don't await long; run in background
            try:
                await notifier.send(text)
            except Exception as e:
                print("Failed to send Telegram message:", e)

    # Run ws client until cancelled
    try:
        await start_ws_client(on_event)
    except asyncio.CancelledError:
        pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped by user")
