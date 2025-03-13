import asyncio

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

import states

from keyboards import buttons

import db

from misc import load_to_file

from schemas import event


router = Router() 


@router.callback_query(states.BASE, F.data == buttons.Menu.GET_REPORT)
async def get_report(call: CallbackQuery, state: FSMContext):
    events = await db.event.all(filters={"user_id": call.from_user.id})
    if not events:
        alert = await call.message.answer(text="Мероприятий не добавлено")
        await asyncio.sleep(3)
        await alert.delete()
    else:
        load_to_file(
            [event.EventAddDTO.model_validate(event_, from_attributes=True) for event_ in events]
        )
        await call.message.answer_document(
            FSInputFile("events.xlsx", filename="Отчёт.xlsx")
        )