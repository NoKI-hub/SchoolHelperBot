from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def create_format():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Очный")
    builder.button(text="Дистанционный")
    builder.button(text="Отмена")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Добавить мероприятие")
    builder.button(text="Удалить мероприятие")
    builder.button(text="Изменить мероприятие")
    builder.button(text="Мои мероприятия")
    builder.button(text="Назад")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
    


def type():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Конференция")
    builder.button(text="Конкурс учителя")
    builder.button(text="Конкурс ученика")
    builder.button(text="Отмена")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def end_or_add():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Добавить еще")
    builder.button(text="Завершить")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def delete_type():
    builder = ReplyKeyboardBuilder()
    builder.button(text="По организатору")
    builder.button(text="По дате")
    builder.button(text="По участнику")
    builder.button(text="По названию")
    builder.button(text="Отмена")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def end_delete():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Завершить удаление")
    return builder.as_markup(resize_keyboard=True)


def inline_confirm_delete(event_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="Удалить", callback_data=f"delevent_{event_id}")
    return builder.as_markup(resize_keyboard=True)
    

FORMAT = create_format()
MENU = menu()
TYPE = type()
END_OR_ADD = end_or_add()
END_DELETE = end_delete()
DELETE_TYPE = delete_type()