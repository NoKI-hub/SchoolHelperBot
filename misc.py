from aiogram.types import Message
from models.user_models import UserModel
from pydantic import ValidationError
from aiogram.filters.state import State, StatesGroup


def message_from_error(e):
    raw_message = e.errors()[0].get("msg", ", Unknown error...")
    return ", ".join(raw_message.split(", ")[1:])

def user_data_validation(msg: Message):
    try:
        user = UserModel(id=msg.from_user.id, full_name=msg.text)
    except ValidationError as e:
        result = message_from_error(e)
    else:
        user.update_names()
        result = user
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