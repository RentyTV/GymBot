from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from filters.is_admin import IsAdmin
from keyboards.reply import admin_kb, user_kb
from db.models import Users
from db.orm_query import orm_add_user, orm_get_user
from db.engine import session_maker
from sqlalchemy.ext.asyncio import AsyncSession

router = Router()


@router.message(CommandStart(), IsAdmin())
async def start(message: Message, session: AsyncSession) -> None:
    await message.answer_photo(photo='AgACAgIAAxkBAAPyZlOHb9FgLJzf1Nrbt-JbkHpqI48AArDeMRtdIZhKH1QUp1Q0a1IBAAMCAAN4AAM1BA', caption=f"<b>Hallo {message.from_user.first_name}!!!</b>\n\n<b>Du bist ein ADMIN</b>", reply_markup=admin_kb)
    # await message.answer(f"<b>Hallo {message.from_user.first_name}!!!</b>\n\n<b>Du bist ein ADMIN</b>", reply_markup=admin_kb)
    try:
        await orm_add_user(session, user_id=message.from_user.id, username=message.from_user.full_name, g_days=0, g_sets=0, g_timer=0.0, g_status=False)
    except Exception as e:
        await message.answer(
            f"Ошибка: \n{str(e)}\nОбратись к программеру, он опять денег хочет"
        )


@router.message(CommandStart())
async def start(message: Message, session: AsyncSession) -> None:
    await message.answer_photo(photo='AgACAgIAAxkBAAPyZlOHb9FgLJzf1Nrbt-JbkHpqI48AArDeMRtdIZhKH1QUp1Q0a1IBAAMCAAN4AAM1BA', caption=f"<b>Hallo {message.from_user.first_name}!!!</b>\n\nWillkommen bei Gym Bot, deinem persönlichen Assistenten in der Welt des Fitness.", reply_markup=user_kb)
    # await message.answer(f"<b>Hallo {message.from_user.first_name}!!!</b>\n\nWillkommen bei Gym Bot, deinem persönlichen Assistenten in der Welt des Fitness.", reply_markup=user_kb)
    try:
        await orm_add_user(session, user_id=message.from_user.id, username=message.from_user.full_name, g_days=0, g_sets=0, g_timer=0.0, g_status=False)
    except Exception as e:
        await message.answer(
            f"Ошибка: \n{str(e)}\nОбратись к программеру, он опять денег хочет"
        )