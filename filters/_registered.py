from aiogram.filters import BaseFilter
from aiogram import types

import db


class Registered(BaseFilter):
    def __init__(self, true: bool = True):
        self.true = true
    
    async def __call__(self, message: types.Message | types.CallbackQuery) -> bool:
        if isinstance(message, types.CallbackQuery):
            message = message.message
        user = await db.user.by_id(message.chat.id)
        return self.true == (user is not None)
