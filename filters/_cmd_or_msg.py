from aiogram.filters import BaseFilter
from aiogram import types

from typing import Iterable


class CommandOrMessage(BaseFilter):
    def __init__(self, commands: str | Iterable[str],
                 messages: str | Iterable[str],
                 prefix: str = '/',
                 nullable: bool = False,
                 *args, **kwargs):
        if isinstance(commands, str): commands = [commands]
        if isinstance(messages, str): messages = [messages]
        self.commands = set(commands)
        self.messages = set(messages)
        self.prefix = prefix
        self.nullable = nullable
    
    async def __call__(self, message: types.Message) -> bool:
        if message.text:
            return message.text.replace(self.prefix, '', 1) in self.commands or message.text in self.messages
        else:
            return self.nullable
