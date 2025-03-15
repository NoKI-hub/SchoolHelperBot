from pydantic import BaseModel, Field, field_validator
from datetime import datetime

from schemas.utils import fullname_field, validate_fullname


class EventAddTypeDTO(BaseModel):
    type: str


class EventAddIsOnlineDTO(EventAddTypeDTO):
    is_online: bool 
    

class EventAddNameDTO(EventAddIsOnlineDTO):
    name: str = Field(min_length=5)


class EventAddParticipantDTO(EventAddNameDTO):
    participant: str = fullname_field

    @field_validator("participant")
    def validate_participant(cls, value):
        if validate_fullname(value):
            return value
        raise ValueError("Неверный формат имени")


class EventAddDateDTO(EventAddParticipantDTO):
    date: datetime | str

    @field_validator("date")
    def validate_date(cls, value):
        if isinstance(value, str):
            try:
                if len(value) == 7:
                    value = datetime.strptime(value, "%m.%Y")
                elif len(value) == 10:
                    value = datetime.strptime(value, "%d.%m.%Y")
            except Exception as ex:
                raise ValueError("Неверный формат даты")
            else:
                if not datetime(year=1980, month=1, day=1) <= value < datetime.now():
                        raise ValueError("Проверьте правильность даты")
        return value


class EventAddDTO(EventAddDateDTO):
    organizator: str = Field(min_length=3)
