from pydantic import BaseModel, Field, field_validator
from datetime import datetime

import re


class ConfModel(BaseModel):
    conf_id: int = Field(default=0)
    name: str = Field(min_length=5, default="Conference")
    date: datetime | str = Field(default_factory=datetime.now)
    organizator: str = Field(min_length=3, default="Organizator")
    is_online: bool = Field(default=True)

    @field_validator("name")
    def validate_name(cls, value):
        if not re.match(r'^[А-Яа-яA-Za-z0-9\s\-\&\(\)\,\.\'"\:\[\]\_\|\№]+$', value):
            raise ValueError("Название конференции не должно содержать спец. символы: @, #, $, %, ^, *, +, =, {, }, \\, /, ?, ;, !, ~")
        return value
    
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
    
    @field_validator("organizator")
    def validate_organizator(cls, value):
        if not re.match(r'^[А-Яа-яA-Za-z0-9\s\-\&\(\)\,\.\'"\:\[\]\_\|\№]+$', value):
            raise ValueError("Наименование организатора не должно содержать спец. символы: @, #, $, %, ^, *, +, =, {, }, \\, /, ?, ;, !, ~")
        return value
    

            

