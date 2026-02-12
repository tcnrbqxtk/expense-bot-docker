import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, ENV
from handlers import all_handlers
# from db.base import engine, Base


if ENV == "PROD":
    from logger.logging_prod import setup_logging
else:
    from logger.logging_dev import setup_logging

setup_logging()

logger = logging.getLogger(__name__)


# async def create_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


async def main() -> str | None:
    if not BOT_TOKEN:
        return "Error: Bot token is not found in .env"
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # регистрируем роутеры
    dp.include_routers(*all_handlers)

    # гарантируем polling
    await bot.delete_webhook(drop_pending_updates=True)

    logger.info("🤖 Бот запущен (polling)")
    # await create_tables()
    await dp.start_polling(bot)  # type: ignore


asyncio.run(main())
