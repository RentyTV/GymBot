from typing import Callable, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float):
        self.cache = TTLCache(maxsize=10000, ttl=rate_limit)

    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: dict[str, Any],
    ) -> Any:
        chat_id = data["event_chat"].id if isinstance(event, Message) else event.message.chat.id
        if chat_id in self.cache:
            return None
        self.cache[chat_id] = None
        return await handler(event, data)
