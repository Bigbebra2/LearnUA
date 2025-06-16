from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Annotated
from pydantic import HttpUrl


# General types
PasswordField = Annotated[str, Field(min_length=8, max_length=128)]
NameField = Annotated[str | None, Field(min_length=2, max_length=35, default=None)]
TitleField = Annotated[str, Field(min_length=10, max_length=180)]

class AuthModel(BaseModel):
    email: EmailStr
    password: PasswordField


class RegisterModel(AuthModel):
    model_config = ConfigDict(
        json_schema_extra={'examples': [
            {
                "email": "test@gmail.com",
                "password": "qwert123",
                "password_again": "qwerty123"
            }
        ]}
    )
    password_again: PasswordField


class LoginModel(AuthModel):
    model_config = ConfigDict(
        json_schema_extra={'examples': [
            {
                "email": "test@gmail.com",
                "password": "qwert123",
            }
        ]}
    )


class CourseIn(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={'examples': [
            {
                "title": "C++ mega course",
                "description": "Master modern C++ with hands-on coding."
            }
        ]}
    )

    title: TitleField
    description: Annotated[str, Field(min_length=32, max_length=1800)]


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

    first_name: NameField
    last_name: NameField
    bio: Annotated[str, Field(max_length=256)] = None
    age: Annotated[int, Field(ge=14, le=150)] = None
    contacts: Annotated[list[dict[str, HttpUrl]], Field(max_length=10)] = []


class SectionIn(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            'examples': [
                {'title': 'some section title'}
            ]
        }
    )
    title: TitleField

class LessonIn(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            'examples': [
                {'title': 'some lesson title'}
            ]
        }
    )
    title: TitleField

















