from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from user_states import UserStates
from misc import user_data_validation, validation_handle
from keyboards import BASE_KEYBOARD, CHANGE_NAME_KEYBOARD


change_router = Router()


@change_router.message(Command('start'), UserStates.base)
async def start_registered_handler(msg: Message, state: FSMContext):
    await msg.answer("Вы уже зарегистрированы. Желаете изменить свои данные?", reply_markup=CHANGE_NAME_KEYBOARD)
    await state.set_state(UserStates.change)

    
@change_router.message(F.text == "Изменить", UserStates.change)
async def start_registered_handler(msg: Message, state: FSMContext):
    await msg.answer("Введите корректные данные")
    await state.set_state(UserStates.name_update)


@change_router.message(UserStates.name_update)
async def change_fullname_handler(msg: Message, state: FSMContext):
    result = user_data_validation(msg)
    if await validation_handle(result, msg):
        user = result
        ... # TODO обновление данных в базе
        await msg.answer("Изменение прошло успешно!", reply_markup=BASE_KEYBOARD)
        await state.set_state(UserStates.base)
        

@change_router.message(F.text == "Отмена", UserStates.change)
async def cancel_change_fullname(msg: Message, state: FSMContext):
    await msg.answer("Изменение отменено", reply_markup=BASE_KEYBOARD)
    await state.set_state(UserStates.base)