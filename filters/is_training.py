from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from db.orm_query import orm_get_user
from sqlalchemy.ext.asyncio import AsyncSession


class IsTraining(BaseFilter):
    key = 'is_training'

    async def __call__(self, event: Message | CallbackQuery, session: AsyncSession) -> bool:
        user_id = event.from_user.id
        user_data = await orm_get_user(session, user_id)
        if user_data:
            return user_data.g_status == False
