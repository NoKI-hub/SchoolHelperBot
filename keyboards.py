from aiogram.utils.keyboard import ReplyKeyboardBuilder


def create_format_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Очный")
    builder.button(text="Дистанционный")
    builder.button(text="Отмена")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def base_keyboard(is_admin: bool = False):
    builder = ReplyKeyboardBuilder()
    builder.button(text="Изменить ФИО")
    builder.button(text="Мероприятия")
    if is_admin:
        builder.button(text="Получить отчет")
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)


def event_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Добавить мероприятие")
    builder.button(text="Удалить мероприятие")
    builder.button(text="Изменить мероприятие")
    builder.button(text="Мои мероприятия")
    builder.button(text="Назад")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
    


def change_name_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Изменить")
    builder.button(text="Отмена")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def event_type_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Конференция")
    builder.button(text="Конкурс учителя")
    builder.button(text="Конкурс ученика")
    builder.button(text="Отмена")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def end_or_add_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Добавить еще")
    builder.button(text="Завершить")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def cancel_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Отмена")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
    

FORMAT_KEYBOARD = create_format_keyboard()
CHANGE_NAME_KEYBOARD = change_name_keyboard()
EVENT_MENU_KEYBOARD = event_menu_keyboard()
EVENT_TYPE_KEYBOARD = event_type_keyboard()
END_OR_ADD_KEYBOARD = end_or_add_keyboard()
CANCEL_KEYBOARD = cancel_keyboard()