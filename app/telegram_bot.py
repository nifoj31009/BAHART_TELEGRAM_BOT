"""
Minimal Telegram notifier using python-telegram-bot. This wraps the Bot.send_message call
in an async-friendly function.
"""
import os
import asyncio
from telegram import Bot

class TelegramNotifier:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self._bot = Bot(token=token)

    async def send(self, text: str):
        # run the blocking send in a thread so it doesn't block the event loop
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._bot.send_message, self.chat_id, text)
