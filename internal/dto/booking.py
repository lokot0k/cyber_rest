import datetime
import uuid
from dataclasses import dataclass

from pydantic import BaseModel
from fastapi import Query


class BaseBooking(BaseModel):
    user_id: uuid.UUID
    device_id: uuid.UUID


class BookingRead(BaseBooking):
    id: uuid.UUID
    start_time: datetime.datetime
    end_time: datetime.datetime

    class Config(object):
        orm_mode = True


class BookingCreate(BaseBooking):
    start_time: float
    end_time: float


class BookingEdit(BaseBooking):
    user_id: uuid.UUID | None = None
    device_id: uuid.UUID | None = None
    start_time: float | None = None
    end_time: float | None = None


@dataclass
class BookingFilter(object):
    user_id: uuid.UUID = Query('')
    device_id: uuid.UUID = Query('')
