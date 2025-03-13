import pandas as pd

from keyboards import buttons

from schemas import event

from typing import Iterable


def load_to_file(all_events: Iterable[event.EventAddDTO], filename: str = "events.xlsx"):
    results = []
    for event in all_events:
        result = event.model_dump()
        result['date'] = event.date.strftime('%d.%m.%Y')
        result['is_online'] = buttons.ChooseFormat.ONLINE if event.is_online else buttons.ChooseFormat.OFFLINE
        results.append(result)
    dataframe = pd.DataFrame(results)
    dataframe = dataframe.rename(columns={"date": "Дата",
                              "type": "Тип мероприятия",
                              "name": "Название",
                              "organizator": "Организатор",
                              "participant": "Участник",
                              "is_online": "Очно/Онлайн"})
    dataframe = dataframe[["Дата", "Тип мероприятия", "Название", "Организатор", "Участник", "Очно/Онлайн"]]
    with pd.ExcelWriter(filename, engine="xlsxwriter", mode='w') as writer:
        dataframe.to_excel(writer, sheet_name="Data", index=False)
