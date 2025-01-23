from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str
    password: str


class CreateUser(UserBase):
    pass


class User(BaseModel):
    id: int
    username: str
    tg_id: Optional[int] = None
    reg_date: datetime
    is_admin: bool = Field(default=False, alias="is_admin")
    is_white: bool = Field(default=False, alias="is_white")

    class Config:
        orm_mode = True
