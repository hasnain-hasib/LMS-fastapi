from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum

class UserBase(BaseModel):
    email: str
    role: int

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

