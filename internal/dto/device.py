import uuid
from dataclasses import dataclass

from pydantic import BaseModel
from fastapi import Query


class BaseDevice(BaseModel):
    name: str
    description: str


class DeviceRead(BaseDevice):
    id: uuid.UUID
    is_available: bool

    class Config(object):
        orm_mode = True


class DeviceEdit(BaseDevice):
    name: str | None = None
    description: str | None = None


@dataclass
class DeviceFilter(object):
    name: str = Query('')
    description: str = Query('')
    is_available: bool | None = Query(None)
