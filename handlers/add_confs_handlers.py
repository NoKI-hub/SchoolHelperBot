from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboards import FORMAT_KEYBOARD, BASE_KEYBOARD
from filters import StatesFilter
from models.conf_models import ConfModel
from user_states import UserStates, ConfProcessing
from misc import message_from_error

from pydantic import ValidationError


add_conf_router = Router()


@add_conf_router.message(Command("add_conf"), StatesFilter([UserStates.base, ConfProcessing.finish_add]))
async def add_conf_starting(msg: Message, state: FSMContext):
    await msg.answer("Введите данные", reply_markup=ReplyKeyboardRemove())
    await msg.answer("Название конфереции:")
    await state.set_state(ConfProcessing.name)


@add_conf_router.message(ConfProcessing.name)
async def add_conf_name(msg: Message, state: FSMContext):
    try:
        conference = ConfModel(name=msg.text)
    except ValidationError as e:
        await msg.answer(message_from_error(e))
        await msg.answer("Проверьте правильность написания названия")
    else:
        await state.update_data(conference=conference)
        await msg.answer("Дата проведения:")
        await state.set_state(ConfProcessing.date)


@add_conf_router.message(ConfProcessing.date)
async def add_conf_date(msg: Message, state: FSMContext):
    conference = (await state.get_data()).get("conference")
    try:
        conference = ConfModel(name=conference.name, date=msg.text)
    except ValidationError as e:
        await msg.answer(message_from_error(e))
        await msg.answer("Проверьте правильность написания даты")
    else:
        await state.update_data(conference=conference)  
        await msg.answer("Организатор конференции:")
        await state.set_state(ConfProcessing.organizator)


@add_conf_router.message(ConfProcessing.organizator)
async def add_conf_organizator(msg: Message, state: FSMContext):
    conference = (await state.get_data()).get("conference")
    try:
        conference = ConfModel(name=conference.name, date=conference.date, organizator=msg.text)
    except:
        await msg.answer("Проверьте правильность написания наименования организатора")
    else:
        await state.update_data(conference=conference)
        await msg.answer("Формат проведения(очный/дистанционный):", reply_markup=FORMAT_KEYBOARD)
        await state.set_state(ConfProcessing.is_online)


@add_conf_router.message(ConfProcessing.is_online)
async def add_confs_handler(msg: Message, state: FSMContext):
    conference = (await state.get_data()).get("conference")
    if msg.text == "Очный":
        conference.is_online = False
    elif msg.text == "Дистанционный":
        conference.is_online = True
    else:
        await msg.answer("Воспользуйтесь кнопками")
        return
    ... # TODO добавить сохранение данных в бд
    await msg.answer("Данные приняты", reply_markup=ReplyKeyboardRemove())
    await msg.answer("/end | /add_conf")
    await state.set_state(ConfProcessing.finish_add)


@add_conf_router.message(Command("end"), ConfProcessing.finish_add)
async def add_confs_handler(msg: Message, state: FSMContext):
    await msg.answer("Добавление конференций успешно завершено!", reply_markup=BASE_KEYBOARD)
    await state.set_state(UserStates.base)