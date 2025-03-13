from pydantic import BaseModel, field_validator

from schemas.utils import fullname_field, validate_fullname


class UserRegistrationDTO(BaseModel):
    fullname: str = fullname_field

    @field_validator("fullname")
    def validate_participant(cls, value):
        if validate_fullname(value):
            return value
        raise ValueError("Неверный формат имени")


class UserDTO(UserRegistrationDTO):
    id: int
