from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Annotated
from pydantic import HttpUrl


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


class ProfileModel(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            'examples': [
                {
                    "first_name": "John",
                    "last_name": "Doe",
                    "age": 25,
                    "bio": "Likes to eat cookies",
                    "contacts": [
                        {"telegram": "https://telegram.org/John-doe"},
                        {"instagram": "https://instagram.com/John-doe"}
                    ]
                }
            ]
        }
    )

    first_name: Annotated[str, Field(min_length=2, max_length=35)] = None
    last_name: Annotated[str, Field(min_length=2, max_length=35)] = None
    bio: Annotated[str, Field(max_length=256)] = None
    age: Annotated[int, Field(ge=14, le=150)] = None
    contacts: Annotated[list[dict[str, HttpUrl]], Field(max_length=10)] = []

