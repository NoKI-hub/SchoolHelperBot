from aiogram import Router
from aiogram import types, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from user_models import UserModel
from user_states import UserStates

from pydantic import ValidationError


router = Router()


@router.message(Command('help'))
async def start_handler(msg: Message):
    await msg.answer("""\
Вот список команд принимаемых этим ботом:
/start - для начала регистрации
/help - вызывает список всех команд
/add_confs - позволяет добавить конференции в базу\
""")

# TODO: добавить хендлер для обработки команды старт уже зареганых пользователей
@router.message(Command('start'))
async def start_handler(msg : Message, state: FSMContext):
    await msg.answer("Здравствуйте! Я - бот, помогающий завучу в работе")
    await msg.answer("Для начала сбора данных напишите ниже своё ФИО")
    await state.set_state(UserStates.names_processing)


@router.message(UserStates.names_processing)
async def fullname_handler(msg: Message, state: FSMContext):
    try:
        user = UserModel(id=msg.from_user.id,
                         full_name=msg.text,
                         firstname="  ",
                         lastname="  ",
                         surname="  ",
                         confs=None)
    except ValidationError as e:
        await msg.answer(e.errors()[0].get("msg", ", Unknown error...").split(", ")[1])
        await msg.answer("Попробуйте ещё раз")
    else:
        ... # добавление данных в базу
        await msg.answer("Регистрация прошла успешно!")
        await state.set_state(UserStates.base)


@router.message(Command("add_confs"), UserStates.base)
async def add_confs_handler(msg: Message, state: FSMContext):
    await msg.answer("Введите данные о конферециях в которых вы учавствовали на данный момент в следующем формате:")
    await msg.answer("\\<Формат данных\\>")
    await state.set_state(UserStates.conf_processing)



