from aiogram.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    names_processing = State()
    conf_processing = State()
    base = State()
