from typing import Optional
from datetime import date
import re
from dateutil import parser
from dateutil.parser import ParserError

from pydantic import BaseModel, EmailStr, Field, model_validator, ConfigDict, field_validator, field_serializer

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    birth_date: date
    phone_number: Optional[str]

    model_config = ConfigDict(json_encoders={date: lambda v: v.strftime('%Y-%m-%d')}, extra='forbid')

class UserRegistration(BaseModel):
    username: str = Field(..., min_length=2, max_length=10)
    email: EmailStr
    password: str = Field(..., min_length=5)
    password_confirm: str
    birth_date: date
    phone_number: Optional[str] = None

    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    @model_validator(mode='after')
    def validate_password(self):
        if self.password != self.password_confirm:
            raise ValueError('Passwords are not the same!!')
        return self

    @field_validator('birth_date', mode='after')
    @classmethod
    def validate_birth_date(cls, value: date):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if not 18 <= age <= 60:
            raise ValueError('Age must be between 18 and 60!!')
        return value

    @field_validator('birth_date', mode='before')
    @classmethod
    def parse_birth_date(cls, value: str):
        if isinstance(value, date):
            return value
        try:
            return parser.parse(value, dayfirst=True).date()
        except (ParserError, TypeError):
            raise ValueError('Incorrect data format. Str with date is expected.')

    @field_validator('phone_number', mode='before')
    @classmethod
    def validate_phone(cls, value: str | None):
        if value is None or (isinstance(value, str) and not value.strip()):
            return None
        clean_phone = re.sub(r'[\s\-\(\)]', '', value)
        if not re.match(r'^\+\d{7,15}$', clean_phone):
            raise ValueError('Incorrect phone format: Expected international format (e.g., +1234567890).')
        return clean_phone

