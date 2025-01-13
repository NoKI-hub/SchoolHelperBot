from aiogram.filters import BaseFilter
from aiogram.filters.state import State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


class StatesFilter(BaseFilter):
    def __init__(self, state: State | list[State]) -> None:
        self.state = state
        
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        if isinstance(self.state, State):
            return await state.get_state() == self.state
        return await state.get_state() in self.state
    
# TODO связать с базой данных
class NotRegisteredFilter(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        return await state.get_state() is None
    
