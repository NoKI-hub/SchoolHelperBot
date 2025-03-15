from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from typing import Iterable, Callable


class ReplyKBuilder(ReplyKeyboardBuilder):
    def __init__(self, *args, **kwargs):
        super().__init__()
    
    def add_buttons(self, *buttons: Iterable[str]):
        for button in buttons:
            self.button(text=button)


class InlineKBuilder(InlineKeyboardBuilder):
    def __init__(self, *args, **kwargs):
        super().__init__()
    
    def add_buttons(self, *buttons: Iterable[str], callback_prefix: str = "", callback_suffix: str = ""):
        for button in buttons:
            self.button(text=button, callback_data=callback_prefix + button + callback_suffix)


def inline_keyboard(
        *buttons: Iterable[str] | str,
        adjust: int | Iterable[int] | None = None,
        resized: bool = True,
        callback_prefix: str = "",
        callback_suffix: str = "",
    ):
    builder = InlineKBuilder()
    if isinstance(buttons, str):
        builder.button(text=buttons, callback_data=callback_prefix + buttons + callback_suffix)
    else:
        builder.add_buttons(*buttons, callback_prefix=callback_prefix, callback_suffix=callback_suffix)
    if isinstance(adjust, int):
        adjust = (adjust,)
    if adjust: builder.adjust(*adjust)
    return builder.as_markup(resize_keyboard=resized)


def reply_keyboard(*buttons: Iterable[str] | str, adjust: int | Iterable[int] | None = None, resized: bool = True):
    builder = ReplyKBuilder()
    if isinstance(buttons, str):
        builder.button(text=buttons)
    else:
        builder.add_buttons(*buttons)
    if isinstance(adjust, int):
        adjust = (adjust,)
    if adjust: builder.adjust(*adjust)
    return builder.as_markup(resize_keyboard=resized)


def inline_kbuild(adjust: int | Iterable[int] | None = None, resized: bool = True, *args, **kwargs):
    def first_wrapper(k_function: Callable):
        def second_wrapper(*args, **kwargs):
            builder = InlineKBuilder(*args, **kwargs)
            k_function(builder=builder, *args, **kwargs)
            if adjust:
                if isinstance(adjust, int):
                    builder.adjust(adjust)
                else:
                    builder.adjust(*adjust)
            return builder.as_markup(resize_keyboard=resized)
        return second_wrapper
    return first_wrapper


def reply_kbuild(adjust: int | Iterable[int] | None = None, resized: bool = True, *args, **kwargs):
    def first_wrapper(k_function: Callable):
        def second_wrapper(*args, **kwargs):
            builder = ReplyKBuilder(*args, **kwargs)
            k_function(builder=builder, *args, **kwargs)
            if adjust:
                if isinstance(adjust, int):
                    builder.adjust(adjust)
                else:
                    builder.adjust(*adjust)
            return builder.as_markup(resize_keyboard=resized)
        return second_wrapper
    return first_wrapper
