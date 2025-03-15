from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from handlers.base import main_menu

import states

from schemas.user import UserRegistrationDTO

import db
from db import models


router = Router()


@router.message(states.NAMES_PROCESSING)
async def register_prosessing(msg: Message, state: FSMContext):
    await msg.chat.do("typing")
    try:
        user = UserRegistrationDTO(fullname=msg.text)
    except:
        await msg.answer("Неверный формат данных. Попробуйте ещё раз")
    else:
        user_orm = models.User(**user.model_dump(), id=msg.chat.id)
        await db.user.add(user_orm)
        await msg.answer("Регистрация прошла успешно")
        await state.set_state(states.BASE)
        await main_menu(msg, state)