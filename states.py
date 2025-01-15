from aiogram.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    names_processing = State()
    name_update = State()
    conf_processing = State()
    change = State()
    base = State()

class EventProcess(StatesGroup):
    menu = State()
    choose_event_type = State()
    
    class Events(StatesGroup):
        participant = State()
        name = State()
        date = State()
        organizator = State()
        is_online = State()
        finish_add = State()
