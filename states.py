from aiogram.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    NAMES_PROCESSING = State()
    NAME_UPDATE = State()
    EVENT_PROCESS = State()
    CHANGE = State()
    BASE = State()

class EventProcess(StatesGroup):
    MENU = State()
    CHOOSE_EVENT_TYPE = State()
    CHOOSE_DELETE_TYPE = State()
    
    class Events(StatesGroup):
        PARTICIPANT = State()
        NAME = State()
        DATE = State()
        ORGANIZATOR = State()
        IS_ONLINE = State()
        FINISH_ADD = State()  

    class DeleteBy(StatesGroup):
        PARTICIPANT = State()
        NAME = State()
        DATE = State()
        ORGANIZATOR = State()        
