from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards import event_keyboards, keyboards, user_keyboards
from filters import StatesFilter, TextFilter
from states import UserStates, EventProcess
from handlers.data_handlers import data_router
from misc import data_validation, get_event_str, search_events
from models.event_models import EventModel


event_router = Router()
event_router.include_router(data_router)


@event_router.message(F.text == "Мероприятия", UserStates.BASE)
async def event_menu(msg: Message, state: FSMContext):
    await msg.answer("Мероприятия (меню):", reply_markup=event_keyboards.MENU)
    await state.set_state(EventProcess.MENU)


@event_router.message(F.text == "Назад", EventProcess.MENU)
async def event_menu_back(msg: Message, state: FSMContext, is_admin: bool):
    await msg.answer("Главное меню:", reply_markup=user_keyboards.base(is_admin))
    await state.set_state(UserStates.BASE)
    

@event_router.message(F.text == "Добавить мероприятие", EventProcess.MENU)
async def add_event(msg: Message, state: FSMContext):
    await msg.answer("Выберите тип мероприятия:", reply_markup=event_keyboards.TYPE)
    await state.set_state(EventProcess.CHOOSE_EVENT_TYPE)


@event_router.message(F.text == "Отмена", StatesFilter(EventProcess))
async def event_type_choose_cancel(msg: Message, state: FSMContext):
    await event_menu(msg, state)


@event_router.message(F.text == "Удалить мероприятие", EventProcess.MENU)
async def delete_event(msg: Message, state: FSMContext):
    await msg.answer("Выберить способ удаления:", reply_markup=event_keyboards.DELETE_TYPE)
    await state.set_state(EventProcess.CHOOSE_DELETE_TYPE)


@event_router.message(TextFilter(["По дате", "По названию", "По организатору", "По участнику"]), EventProcess.CHOOSE_DELETE_TYPE)
async def delete_by_date(msg: Message, state: FSMContext):
    answers = {
        "По дате": ("Введите дату в формате ДД.ММ.ГГГГ или MM.ГГГГ:", EventProcess.DeleteBy.DATE),
        "По названию": ("Введите название мероприятия:", EventProcess.DeleteBy.NAME),
        "По организатору": ("Введите организатора:", EventProcess.DeleteBy.ORGANIZATOR),
        "По участнику": ("Введите ФИО участника:", EventProcess.DeleteBy.PARTICIPANT),
    }
    await msg.answer("Можете указывать не полные данные (кроме даты)")
    await msg.answer(answers[msg.text][0], reply_markup=keyboards.CANCEL)
    await state.set_state(answers[msg.text][1])


@event_router.message(F.text == "Завершить удаление", StatesFilter(EventProcess.DeleteBy))
async def end_delete_event(msg: Message, state: FSMContext):
    await event_menu(msg, state)
    

@event_router.message(StatesFilter(EventProcess.DeleteBy))
async def search_and_send(msg: Message, state: FSMContext):
    if (user_state := await state.get_state()) == EventProcess.DeleteBy.DATE:
        ok, result = data_validation(EventModel, date=msg.text)
    else:
        ok, result = data_validation(EventModel, error_message="Неверный формат введенных данных", name=msg.text)
    if ok:
        search_data = {
            EventProcess.DeleteBy.DATE: ("date", result.date),
            EventProcess.DeleteBy.NAME: ("name", result.name),
            EventProcess.DeleteBy.ORGANIZATOR: ("organizator", result.organizator),
            EventProcess.DeleteBy.PARTICIPANT: ("participant", result.participant)
        }
        search_result = await search_events(search_data[user_state][0], search_data[user_state][1])
        if search_result:
            await msg.answer("Найденные мероприятия:", reply_markup=event_keyboards.END_DELETE)
            for event in search_result:
                await msg.answer(get_event_str(event), reply_markup=event_keyboards.inline_confirm_delete(event_id=event.event_id))
        else:
            await msg.answer("Мероприятий не найдено")
    else:
        await msg.answer(result)


@event_router.message(F.text == "Мои мероприятия")
async def events_list(msg: Message, state: FSMContext):
    search_result = await search_events("user_id", msg.from_user.id)
    await msg.answer("Ваши мероприятия:")
    if search_result:
        for event in search_result:
            await msg.answer(get_event_str(event))
    else:
        await msg.answer("Мероприятий не найдено")