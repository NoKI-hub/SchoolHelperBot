from aiogram.types import Message
from models.user_models import UserModel
from models.event_models import EventModel
from pydantic import ValidationError, BaseModel
from aiogram.filters.state import State, StatesGroup


def message_from_error(e):
    raw_message = e.errors()[0].get("msg", ", Unknown error...")
    return ", ".join(raw_message.split(", ")[1:])


def data_validation(class_model: BaseModel, *args, **kwargs):
    try:
        model = class_model(*args, **kwargs)
    except ValidationError as e:
        ok = False
        result = message_from_error(e)
    else:
        ok = True
        result = model
    return ok, result


def user_data_validation(msg: Message):
    ok, result = data_validation(UserModel, id=msg.from_user.id, full_name=msg.text)
    if not ok:
        return result
    result.update_names()
    return result


async def validation_handle(validation_result, msg: Message, answer_msg: str = "Попробуйте еще раз"):
    if isinstance(validation_result, str):
        await msg.answer(validation_result)
        await msg.answer(answer_msg)
        return None
    return validation_result

def get_all_states(states_group):
    result = []
    for name, state in vars(states_group).items():
        if isinstance(state, State):
            result.append(state)
        elif isinstance(state, StatesGroup):
            result.extend(get_all_states(state))
    return result

 
def get_event_str(event: EventModel):
    return f"""\
{event.date.strftime("%d.%m.%Y")}: {event.name}
{event.organizator}, {"Дистанционно" if event.is_online else "Очно"}
{event.participant}\
"""