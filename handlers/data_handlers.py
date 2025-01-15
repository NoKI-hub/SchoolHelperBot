from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboards import  (FORMAT_KEYBOARD,
                        EVENT_MENU_KEYBOARD,
                        END_OR_ADD_KEYBOARD,
                        CANCEL_KEYBOARD)
from filters import StatesFilter, TextFilter
from models.event_models import EventModel
from states import EventProcess
from misc import message_from_error

from pydantic import ValidationError


data_router = Router()


@data_router.message(TextFilter(["Конференция",
                                 "Конкурс учителя",
                                 "Конкурс ученика",
                                 "Добавить еще"]),
                     StatesFilter([EventProcess.choose_event_type,
                                   EventProcess.Events.finish_add]))
async def add_conf_starting(msg: Message, state: FSMContext):
    if msg.text == "Конкурс ученика":
        result_state = EventProcess.Events.participant
    else:
        result_state = EventProcess.Events.name
        await state.update_data(conference=EventModel(participant=None))
    await msg.answer("Введите данные", reply_markup=ReplyKeyboardRemove())
    await msg.answer("Название:", reply_markup=CANCEL_KEYBOARD)
    await state.set_state(result_state)


@data_router.message(EventProcess.Events.participant)
async def add_participant(msg: Message, state: FSMContext):
    try:
        conference = EventModel(participant=msg.text)
    except ValidationError as e:
        await msg.answer(message_from_error(e))
        await msg.answer("Проверьте правильность написания ФИО", reply_markup=CANCEL_KEYBOARD)
    else:
        await state.update_data(conference=conference)
        await msg.answer("Название:", reply_markup=CANCEL_KEYBOARD)
        await state.set_state(EventProcess.Events.name)


@data_router.message(EventProcess.Events.name)
async def add_conf_name(msg: Message, state: FSMContext):
    conference: EventModel = (await state.get_data()).get("conference")
    try:
        conference = EventModel(participant=conference.participant, name=msg.text)
    except ValidationError as e:
        await msg.answer(message_from_error(e))
        await msg.answer("Проверьте правильность написания названия", reply_markup=CANCEL_KEYBOARD)
    else:
        await state.update_data(conference=conference)
        await msg.answer("Дата проведения:", reply_markup=CANCEL_KEYBOARD)
        await state.set_state(EventProcess.Events.date)


@data_router.message(EventProcess.Events.date)
async def add_conf_date(msg: Message, state: FSMContext):
    conference: EventModel = (await state.get_data()).get("conference")
    try:
        conference = EventModel(participant=conference.participant, name=conference.name, date=msg.text)
    except ValidationError as e:
        await msg.answer(message_from_error(e))
        await msg.answer("Проверьте правильность написания даты", reply_markup=CANCEL_KEYBOARD)
    else:
        await state.update_data(conference=conference)  
        await msg.answer("Организатор конференции:", reply_markup=CANCEL_KEYBOARD)
        await state.set_state(EventProcess.Events.organizator)


@data_router.message(EventProcess.Events.organizator)
async def add_conf_organizator(msg: Message, state: FSMContext):
    conference: EventModel = (await state.get_data()).get("conference")
    try:
        conference = EventModel(participant=conference.participant, name=conference.name, date=conference.date, organizator=msg.text)
    except:
        await msg.answer("Проверьте правильность написания наименования организатора", reply_markup=CANCEL_KEYBOARD)
    else:
        await state.update_data(conference=conference)
        await msg.answer("Формат проведения:", reply_markup=FORMAT_KEYBOARD)
        await state.set_state(EventProcess.Events.is_online)


@data_router.message(EventProcess.Events.is_online)
async def add_confs_handler(msg: Message, state: FSMContext):
    conference: EventModel = (await state.get_data()).get("conference")
    if msg.text == "Очный":
        conference.is_online = False
    elif msg.text == "Дистанционный":
        conference.is_online = True
    else:
        await msg.answer("Воспользуйтесь кнопками")
        return
    if conference.participant is None:
        conference.participant = ... # TODO добавить получение ФИО из бд
    ... # TODO добавить сохранение данных в бд
    await msg.answer("Данные приняты", reply_markup=END_OR_ADD_KEYBOARD)
    await state.set_state(EventProcess.Events.finish_add)


@data_router.message(F.text == "Завершить", EventProcess.Events.finish_add)
async def add_confs_handler(msg: Message, state: FSMContext):
    await msg.answer("Добавление мероприятий успешно завершено!", reply_markup=EVENT_MENU_KEYBOARD)
    await state.set_state(EventProcess.menu)