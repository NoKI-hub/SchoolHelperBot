from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import UserStates
from misc import user_data_validation, validation_handle
from keyboards import user_keyboards


change_router = Router()


@change_router.message(F.text == "Изменить ФИО", UserStates.BASE)
async def start_registered_handler(msg: Message, state: FSMContext):
    await msg.answer("Вы уже зарегистрированы. Желаете изменить свои данные?", reply_markup=user_keyboards.CHANGE_NAME)
    await state.set_state(UserStates.CHANGE)

    
@change_router.message(F.text == "Изменить", UserStates.CHANGE)
async def start_registered_handler(msg: Message, state: FSMContext):
    await msg.answer("Введите корректные данные")
    await state.set_state(UserStates.NAME_UPDATE)


@change_router.message(UserStates.NAME_UPDATE)
async def change_fullname_handler(msg: Message, state: FSMContext, is_admin: bool):
    result = user_data_validation(msg)
    if await validation_handle(result, msg):
        user = result
        ... # TODO обновление данных в базе
        await msg.answer("Изменение прошло успешно!", reply_markup=user_keyboards.base(is_admin))
        await state.set_state(UserStates.BASE)
        

@change_router.message(F.text == "Отмена", UserStates.CHANGE)
async def cancel_change_fullname(msg: Message, state: FSMContext, is_admin: bool):
    await msg.answer("Изменение отменено", reply_markup=user_keyboards.base(is_admin))
    await state.set_state(UserStates.BASE)