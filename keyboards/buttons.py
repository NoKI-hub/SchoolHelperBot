class Buttons:
    @classmethod
    def all(self):
        return [attr for name, attr in vars(self).items() if not name.startswith("__")]


MENU = "Главное меню"

DELETE = "Удалить"

CONFIRM = "Ок"
CANCEL = "Отмена"


class Menu(Buttons):
    MY_EVENTS = "Мои мероприятия"
    ADD_EVENTS = "Добавить мероприятие"
    GET_REPORT = "Получить отчёт"


class ChooseFormat(Buttons):
    ONLINE = "Онлайн"
    OFFLINE = "Очно"