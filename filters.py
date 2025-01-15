from aiogram.filters import BaseFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from misc import get_all_states


class StatesFilter(BaseFilter):
    def __init__(self, state: State | list[State] | StatesGroup) -> None:
        if isinstance(state, StatesGroup):
            self.state = get_all_states(state)
        else:
            self.state = state
    
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        if isinstance(self.state, State):
            return await state.get_state() == self.state
        return await state.get_state() in self.state
    
# TODO связать с базой данных
class NotRegisteredFilter(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        return await state.get_state() is None
    

class TextFilter(BaseFilter):
    def __init__(self, texts: list[str]) -> None:
        self.texts = texts

    async def __call__(self, message: Message) -> bool:
        return message.text in self.texts

    
