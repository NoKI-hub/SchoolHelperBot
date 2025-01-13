from aiogram.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    names_processing = State()
    name_update = State()
    conf_processing = State()
    change = State()
    base = State()

class ConfProcessing(StatesGroup):
    name = State()
    date = State()
    organizator = State()
    is_online = State()
    finish_add = State()

