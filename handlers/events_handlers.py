from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards import EVENT_MENU_KEYBOARD, EVENT_TYPE_KEYBOARD
from keyboards import base_keyboard
from filters import StatesFilter
from states import UserStates, EventProcess
from handlers.data_handlers import data_router

from pydantic import ValidationError


event_router = Router()
event_router.include_router(data_router)


@event_router.message(F.text == "Мероприятия", UserStates.base)
async def event_menu(msg: Message, state: FSMContext):
    await msg.answer("Мероприятия (меню):", reply_markup=EVENT_MENU_KEYBOARD)
    await state.set_state(EventProcess.menu)


@event_router.message(F.text == "Назад", EventProcess.menu)
async def event_menu_back(msg: Message, state: FSMContext, is_admin: bool):
    await msg.answer("Главное меню:", reply_markup=base_keyboard(is_admin))
    await state.set_state(UserStates.base)
    

@event_router.message(F.text == "Добавить мероприятие", EventProcess.menu)
async def add_event(msg: Message, state: FSMContext):
    await msg.answer("Выберите тип мероприятия:", reply_markup=EVENT_TYPE_KEYBOARD)
    await state.set_state(EventProcess.choose_event_type)


@event_router.message(F.text == "Отмена", StatesFilter(EventProcess))
async def event_type_choose_cancel(msg: Message, state: FSMContext):
    await event_menu(msg, state)