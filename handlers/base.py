from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import filters
import states
import keyboards


router = Router()


@router.message(Command('help'))
async def help_handler(msg: Message):
    await msg.answer("""\
Вот список команд принимаемых этим ботом:
/start - для начала регистрации
/help - вызывает список всех команд
/add_conf - позволяет добавить конференции в базу\
""")


@router.message(Command('start'), filters.Registered(False))
async def start_not_registered_handler(msg : Message, state: FSMContext):
    await msg.answer("Здравствуйте! Я - бот, помогающий завучу в работе")
    await msg.answer("Для начала сбора данных напишите ниже своё ФИО(Иванов Иван Иванович)")
    await state.set_state(states.NAMES_PROCESSING)


@router.message(Command("start"), filters.Registered(True))
async def main_menu(msg: Message, state: FSMContext):
    await msg.answer("Главное меню:", reply_markup=keyboards.base.MENU)
    await state.set_state(states.BASE)
