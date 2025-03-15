import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from config.config import settings
from middlewares.admin_middleware import AdminMiddleware

import handlers

import db


async def main():
    await db.create_tables(if_not_exist=not settings.DEBUG)
    if settings.DEBUG:
        await db.user.add(db.models.User(id=1651321123, fullname="Балыкин Н. Д."))
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(handlers.router)
    dp.message.middleware.register(AdminMiddleware())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())