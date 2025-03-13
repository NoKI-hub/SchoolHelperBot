from aiogram.filters.state import State, StatesGroup


class BaseGroup(StatesGroup):
    @classmethod
    def all(self):
        return [attr for name, attr in vars(self).items() if not name.startswith("__")]


NAMES_PROCESSING = State()
NAME_UPDATE = State()
EVENT_PROCESS = State()
CHANGE = State()
BASE = State()

class EventAdding(BaseGroup):
    EVENT_TYPE = State()
    IS_ONLINE = State()
    NAME = State()
    PARTICIPANT = State()
    DATE = State()
    ORGANIZATOR = State()
