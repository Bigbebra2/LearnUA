from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Annotated


class RegisterModel(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={'examples': [
            {
                "email": "test@gmail.com",
                "password": "qwert123",
                "password_again": "qwerty123"
            }
        ]}
    )

    email: EmailStr
    password: Annotated[str, Field(min_length=8, max_length=128)]
    password_again: Annotated[str, Field(min_length=8, max_length=128)]


class LoginModel(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={'examples': [
            {
                "email": "test@gmail.com",
                "password": "qwert123",
            }
        ]}
    )

    email: EmailStr
    password: Annotated[str, Field(min_length=8, max_length=128)]

