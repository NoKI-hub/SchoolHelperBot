from aiogram.utils.keyboard import ReplyKeyboardBuilder


def base(is_admin: bool = False):
    builder = ReplyKeyboardBuilder()
    builder.button(text="Изменить ФИО")
    builder.button(text="Мероприятия")
    if is_admin:
        builder.button(text="Получить отчет")
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)


def change_name():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Изменить")
    builder.button(text="Отмена")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


CHANGE_NAME = change_name()