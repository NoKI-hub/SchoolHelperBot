from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboards import event_keyboards
from keyboards import keyboards
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
                     StatesFilter([EventProcess.CHOOSE_EVENT_TYPE,
                                   EventProcess.Events.FINISH_ADD]))
async def add_conf_starting(msg: Message, state: FSMContext):
    if msg.text == "Конкурс ученика":
        result_text = "ФИО ученика:"
        result_state = EventProcess.Events.PARTICIPANT
    else:
        result_text = "Название:"
        result_state = EventProcess.Events.NAME
        await state.update_data(conference=EventModel(participant=None))
    await msg.answer("Введите данные", reply_markup=ReplyKeyboardRemove())
    await msg.answer(result_text, reply_markup=keyboards.CANCEL)
    await state.set_state(result_state)


@data_router.message(EventProcess.Events.PARTICIPANT)
async def add_participant(msg: Message, state: FSMContext):
    try:
        conference = EventModel(participant=msg.text)
    except ValidationError as e:
        await msg.answer(message_from_error(e))
        await msg.answer("Проверьте правильность написания ФИО", reply_markup=keyboards.CANCEL)
    else:
        await state.update_data(conference=conference)
        await msg.answer("Название:", reply_markup=keyboards.CANCEL)
        await state.set_state(EventProcess.Events.NAME)


@data_router.message(EventProcess.Events.NAME)
async def add_conf_name(msg: Message, state: FSMContext):
    conference: EventModel = (await state.get_data()).get("conference")
    try:
        conference = EventModel(participant=conference.participant, name=msg.text)
    except ValidationError as e:
        await msg.answer(message_from_error(e))
        await msg.answer("Проверьте правильность написания названия", reply_markup=keyboards.CANCEL)
    else:
        await state.update_data(conference=conference)
        await msg.answer("Дата проведения в формате ДД.ММ.ГГГГ:", reply_markup=keyboards.CANCEL)
        await state.set_state(EventProcess.Events.DATE)


@data_router.message(EventProcess.Events.DATE)
async def add_conf_date(msg: Message, state: FSMContext):
    conference: EventModel = (await state.get_data()).get("conference")
    try:
        conference = EventModel(participant=conference.participant, name=conference.name, date=msg.text)
    except ValidationError as e:
        await msg.answer(message_from_error(e))
        await msg.answer("Проверьте правильность написания даты", reply_markup=keyboards.CANCEL)
    else:
        await state.update_data(conference=conference)  
        await msg.answer("Организатор конференции:", reply_markup=keyboards.CANCEL)
        await state.set_state(EventProcess.Events.ORGANIZATOR)


@data_router.message(EventProcess.Events.ORGANIZATOR)
async def add_conf_organizator(msg: Message, state: FSMContext):
    conference: EventModel = (await state.get_data()).get("conference")
    try:
        conference = EventModel(participant=conference.participant, name=conference.name, date=conference.date, organizator=msg.text)
    except:
        await msg.answer("Проверьте правильность написания наименования организатора", reply_markup=keyboards.CANCEL)
    else:
        await state.update_data(conference=conference)
        await msg.answer("Формат проведения:", reply_markup=event_keyboards.FORMAT)
        await state.set_state(EventProcess.Events.IS_ONLINE)


@data_router.message(EventProcess.Events.IS_ONLINE)
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
    await msg.answer("Данные приняты", reply_markup=event_keyboards.END_OR_ADD)
    await state.set_state(EventProcess.Events.FINISH_ADD)


@data_router.message(F.text == "Завершить", EventProcess.Events.FINISH_ADD)
async def add_confs_handler(msg: Message, state: FSMContext):
    await msg.answer("Добавление мероприятий успешно завершено!", reply_markup=event_keyboards.MENU)
    await state.set_state(EventProcess.MENU)