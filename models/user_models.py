from pydantic import BaseModel, Field, field_validator

import re


def validate_full_name(value):
    parts = value.split()
    if len(parts) != 3:
        raise ValueError('ФИО должно состоять из 3 слов')
    for part in parts:
        if not re.match(r'^[А-Яа-яЁёA-Za-z\-]+$', part):
            raise ValueError('ФИО должно состоять из букв')
    return value


class UserModel(BaseModel):
    id: int
    firstname: str = Field(min_length=2, max_length=20, default="Firstname")
    surname: str = Field(min_length=2, max_length=20, default="Surname")
    lastname: str = Field(min_length=2, max_length=20, default="Lastname")
    full_name: str = Field(min_length=6, max_length=60, default="Lastname Firstname Surname")

    @field_validator("firstname", "surname", "lastname")
    def validate_firstname(cls, value):
        if not re.match(r'^[А-Яа-яЁёA-Za-z\-]+$', value):
            raise ValueError(f'{value.__name__} должно состоять из букв')
        return value
        
    @field_validator("full_name")
    def validate_full_name(cls, value):
        return validate_full_name(value)
    
    def update_names(cls):
        parts = cls.full_name.split()
        cls.lastname = parts[0]
        cls.firstname = parts[1]
        cls.surname = parts[2]
            
        


