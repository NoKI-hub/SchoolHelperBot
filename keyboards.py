from aiogram.utils.keyboard import ReplyKeyboardBuilder


def create_format_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Очный")
    builder.button(text="Дистанционный")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def base_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="/start")
    builder.button(text="/help")
    builder.button(text="/add_conf")
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True) 


def change_name_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Изменить")
    builder.button(text="Отмена")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
    


FORMAT_KEYBOARD = create_format_keyboard()
BASE_KEYBOARD = base_keyboard()
CHANGE_NAME_KEYBOARD = change_name_keyboard()