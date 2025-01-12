from pydantic import BaseModel, Field, field_validator

import re


class UserModel(BaseModel):
    id: int
    firstname: str = Field(min_length=2, max_length=20)
    surname: str = Field(min_length=2, max_length=20)
    lastname: str = Field(min_length=2, max_length=20)
    full_name: str = Field(min_length=6, max_length=60)
    confs: BaseModel | None = ...

    @field_validator("full_name")
    def validate_full_name(cls, value):
        parts = value.split()
        if len(parts) != 3:
            raise ValueError('ФИО должно состоять из 3 слов')
        for part in parts:
            if not re.match(r'^[А-Яа-яЁёA-Za-z\-]+$', part):
                raise ValueError('ФИО должно состоять из букв')
        cls.lastname = parts[0]
        cls.firstname = parts[1]
        cls.surname = parts[2]
        return value
            
        


