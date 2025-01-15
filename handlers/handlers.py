from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from filters import NotRegisteredFilter
from states import UserStates
from misc import user_data_validation, validation_handle
from keyboards import base_keyboard


router = Router()


@router.message(Command('help'))
async def start_handler(msg: Message):
    await msg.answer("""\
Вот список команд принимаемых этим ботом:
/start - для начала регистрации
/help - вызывает список всех команд
/add_conf - позволяет добавить конференции в базу\
""")


@router.message(Command('start'), NotRegisteredFilter())
async def start_not_registered_handler(msg : Message, state: FSMContext):
    await msg.answer("Здравствуйте! Я - бот, помогающий завучу в работе")
    await msg.answer("Для начала сбора данных напишите ниже своё ФИО")
    await state.set_state(UserStates.names_processing)
        

@router.message(UserStates.names_processing)
async def fullname_handler(msg: Message, state: FSMContext, is_admin: bool):
    result = user_data_validation(msg)
    if await validation_handle(result, msg):
        user = result
        ... # TODO добавление данных в базу
        await msg.answer("Регистрация прошла успешно!", reply_markup=base_keyboard(is_admin))
        await state.set_state(UserStates.base)


