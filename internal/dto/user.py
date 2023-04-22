import uuid
from dataclasses import dataclass

from pydantic import BaseModel
from fastapi import Query


class BaseUser(BaseModel):
    username: str


class PasswordUser(BaseUser):
    password: str


class UserRead(BaseUser):
    id: uuid.UUID

    class Config(object):
        orm_mode = True


class UserEdit(BaseUser):
    username: str | None = None
    password: str | None = None


@dataclass
class UserFilter(object):
    username: str = Query('')
