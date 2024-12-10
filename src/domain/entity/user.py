import json

from typing import Annotated, Any
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, Field, model_validator


class UserSignUp(BaseModel):
    full_name: str = Field(max_length=50)
    email: EmailStr
    phone_number: Annotated[str, MinLen(11)]
    password: Annotated[str, MinLen(8)]
    role: str


class UserEmail(BaseModel):
    email: EmailStr

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value: Any) -> Any:
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class UserVerify(BaseModel):
    email: EmailStr
    confirmation_code: Annotated[str, MaxLen(6)]

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value: Any) -> Any:
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class UserSignIn(BaseModel):
    email: EmailStr
    password: Annotated[str, MinLen(8)]

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value: Any) -> Any:
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class ConfirmForgotPassword(BaseModel):
    email: EmailStr
    confirmation_code: Annotated[str, MaxLen(6)]
    new_password: Annotated[str, MinLen(8)]


class ChangePassword(BaseModel):
    old_password: Annotated[str, MinLen(8)]
    new_password: Annotated[str, MinLen(8)]
    access_token: str


class RefreshToken(BaseModel):
    refresh_token: str


class AccessToken(BaseModel):
    access_token: str
