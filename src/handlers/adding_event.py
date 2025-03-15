from aiogram import Router, F
from aiogram.types import CallbackQuery, ReplyKeyboardRemove, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

import states

import keyboards
from keyboards import buttons

from schemas import event

import db
from db import models

from typing import Sequence 

from handlers.base import main_menu


router = Router()


@router.callback_query(
        StateFilter(*states.EventAdding.all()),
        F.data == buttons.CANCEL,
    )
async def cancel_adding(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Отменено")
    await main_menu(call.message, state)


@router.callback_query(states.BASE, F.data == buttons.Menu.ADD_EVENTS)
async def start_adding_event(call: CallbackQuery, state: FSMContext):
    await call.message.answer(
        "Укажите необходимые данные", 
        reply_markup=keyboards.base.CANCEL,
    )
    types = [
        "Конференция",
        "Конкурс",
        "Конкурс ученика"
    ]
    markup = keyboards.utils.inline_keyboard(*types, adjust=1)
    await call.message.answer(
        "Выберите тип мероприятия:", 
        reply_markup=markup,
    )
    await state.set_state(states.EventAdding.EVENT_TYPE)


@router.callback_query(states.EventAdding.EVENT_TYPE)
async def event_type_processing(call: CallbackQuery, state: FSMContext):
    type_name = call.data
    data = await state.get_data()
    event_types: Sequence = data.get("event_types")
    event_dto = event.EventAddTypeDTO(type=type_name)
    await state.update_data(event_dto=event_dto)
    await call.message.edit_text(
        "Выберите формат мероприятия:", 
        reply_markup=keyboards.event_adding.CHOOSE_IS_ONLINE,
    )
    await state.set_state(states.EventAdding.IS_ONLINE)
    

@router.callback_query(states.EventAdding.IS_ONLINE)
async def is_online_processing(call: CallbackQuery, state: FSMContext):
    is_online = call.data
    data = await state.get_data()
    event_dto: event.EventAddTypeDTO = data.get("event_dto")
    if is_online == buttons.ChooseFormat.ONLINE:
        is_online = True
    else:
        is_online = False
    event_dto = event.EventAddIsOnlineDTO(
        **event_dto.model_dump(), 
        is_online=is_online
    )
    await state.update_data(event_dto=event_dto)
    await call.message.edit_text(
        "Укажите название мероприятия:", 
        reply_markup=None,
    )
    await state.set_state(states.EventAdding.NAME)


@router.message(states.EventAdding.NAME)
async def name_processing(msg: Message, state: FSMContext):
    data = await state.get_data()
    event_dto: event.EventAddIsOnlineDTO = data.get("event_dto")
    event_name = msg.text
    try:
        event_dto = event.EventAddNameDTO(
            **event_dto.model_dump(), 
            name=event_name,
        )
    except:
        await msg.answer("Некорректный ввод. Попробуйте еще раз")
    else:
        await state.update_data(event_dto=event_dto)
        user = await db.user.by_id(msg.from_user.id)
        markup = keyboards.utils.reply_keyboard(user.fullname)
        await msg.answer(
            "Укажите ФИО участника мероприятия(Иванов Иван Иванович):",
            reply_markup=markup,
        )
        await state.set_state(states.EventAdding.PARTICIPANT)


@router.message(states.EventAdding.PARTICIPANT)
async def participant_processing(msg: Message, state: FSMContext):
    data = await state.get_data()
    event_dto: event.EventAddNameDTO = data.get("event_dto")
    participant = msg.text
    try:
        event_dto = event.EventAddParticipantDTO.model_validate({
            **event_dto.model_dump(), 
            "participant": participant,
        })
    except Exception as e:
        await msg.answer("Некорректный ввод. Попробуйте еще раз")
    else:
        await state.update_data(event_dto=event_dto)
        await msg.answer(
            "Укажите дату проведения мероприятия(ДД.ММ.ГГГГ):",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.set_state(states.EventAdding.DATE)


@router.message(states.EventAdding.DATE)
async def date_processing(msg: Message, state: FSMContext):
    data = await state.get_data()
    event_dto: event.EventAddParticipantDTO = data.get("event_dto")
    date = msg.text
    try:
        event_dto = event.EventAddDateDTO.model_validate({
            **event_dto.model_dump(), 
            "date": date,
        })
    except:
        await msg.answer("Некорректный ввод. Попробуйте еще раз")
    else:
        await state.update_data(event_dto=event_dto)
        await msg.answer("Укажите организатора мероприятия:")
        await state.set_state(states.EventAdding.ORGANIZATOR)


@router.message(states.EventAdding.ORGANIZATOR)
async def organizator_processing(msg: Message, state: FSMContext):
    data = await state.get_data()
    event_dto: event.EventAddDateDTO = data.get("event_dto")
    organizator = msg.text
    try:
        event_dto = event.EventAddDTO.model_validate({
            **event_dto.model_dump(), 
            "organizator": organizator,
        })
    except Exception as e:
        await msg.answer("Некорректный ввод. Попробуйте еще раз")
    else:
        await state.update_data(event_dto=event_dto)
        await db.event.add(models.Event(
            **event_dto.model_dump(),
            user_id=msg.chat.id,
        ))
        await state.set_state(states.BASE)
        await msg.answer("Мероприятие успешно добавлено!")
        await main_menu(msg, state)
