from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from handlers.base import main_menu

import messages

import states

import keyboards
from keyboards import buttons

import db
from db import models

from typing import Sequence


router = Router()


@router.callback_query(states.BASE, F.data == buttons.Menu.MY_EVENTS)
async def event_list(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Ваши мероприятия:")
    events: Sequence[models.Event] = await db.event.all(filters={"user_id": call.message.chat.id})
    if not events:
        await call.message.answer("У вас нет мероприятий.")
    else:
        for event in events:
            await call.message.answer(
                messages.event_description(event=event),
                reply_markup=keyboards.utils.inline_keyboard(
                    buttons.DELETE,
                    callback_suffix=f"_event_{event.id}"
                ),
            )
    await main_menu(call.message, state)


@router.callback_query(states.BASE, F.data.startswith(buttons.DELETE))
async def delete_event(call: CallbackQuery, state: FSMContext):
    if call.data.split("_")[1] == "event":
        event_id = int(call.data.split("_")[-1])
        await db.event.delete_by_id(event_id=event_id)
        first_line = call.message.text.split("\n")[0]
        other_lines = "\n".join(call.message.text.split("\n")[1:])
        new_text = f'<s>{first_line}</s>\n{other_lines}'
        await call.message.edit_text(new_text, reply_markup=None)