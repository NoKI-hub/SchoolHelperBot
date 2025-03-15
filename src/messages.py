from db import models


def event_description(event: models.Event) -> str:
    return f"""
<b>{event.name} ({event.type} | {"Онлайн" if event.is_online else "Очно"}):</b>
<b>Дата проведения:</b> {event.date.strftime("%d.%m.%Y")}
Участник - {event.participant}
Организатор - {event.organizator}
"""
