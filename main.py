import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from config.config import settings
from handlers.handlers import router
from handlers.events_handlers import event_router
from handlers.user_data_change_handlers import change_router
from middlewares.admin_middleware import AdminMiddleware


async def main():
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    dp.include_router(change_router)
    dp.include_router(event_router)
    dp.message.middleware.register(AdminMiddleware())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())