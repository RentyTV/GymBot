import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


from handlers import setup_message_routers
from callbacks import setup_callback_routers
from config_reader import config
from db.engine import create_db, session_maker
from middlewares.dbm import DataBaseSession
from middlewares.throttling import ThrottlingMiddleware


OWNER_ID = config.OWNER_ID.get_secret_value()


async def on_startup(bot):
    await create_db()
    await send_message_to_user(OWNER_ID, 'Bot hat gestartet')


async def on_shutdown(bot):
    print('bot ist rip')
    await send_message_to_user(OWNER_ID, 'Bot ist rip')


async def send_message_to_user(user_id: int, message_text: str):
        try:
            await bot.send_message(user_id, message_text)
        except Exception as e:
            print(f"Ошибка при отправке сообщения пользователю {user_id}: {str(e)}")


async def main() -> None:
    global bot
    bot = Bot(
        config.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    message_routers = setup_message_routers()
    callback_routers = setup_callback_routers()
    dp.include_router(message_routers)
    dp.include_router(callback_routers)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    dp.message.middleware(ThrottlingMiddleware(1))

    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())