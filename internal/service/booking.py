from datetime import datetime
import uuid
from typing import Sequence

from fastapi import Depends
from pytorm.repository import InjectRepository
from sqlalchemy.ext.asyncio import AsyncSession

from internal.dto.booking import (
    BookingFilter,
    BaseBooking, BookingEdit, BookingCreate, BookingCreateFull
)
from internal.entity.booking import Booking
from internal.usecase.utils import get_session


class BookingService(object):

    def __init__(
            self, session: AsyncSession = Depends(get_session),
    ) -> None:
        self.repository = InjectRepository(Booking, session)

    async def create(self, dto: BookingCreateFull) -> Booking:
        dto.start_time = datetime.fromtimestamp(dto.start_time)
        dto.end_time = datetime.fromtimestamp(dto.end_time)
        booking = self.repository.create(**dto.dict())
        return await self.repository.save(booking)

    async def find(self, dto: BookingFilter) -> Sequence[Booking]:
        query_set = await self.repository.find()
        return list(filter((lambda b: str(dto.device_id) in str(
            b.device_id) and str(dto.user_id) in str(b.device_id)), query_set))

    async def find_one_or_fail(self, booking_id: uuid.UUID) -> Booking:
        return await self.repository.find_one_or_fail(
            id=booking_id,
        )

    async def delete(self, booking_id: uuid.UUID) -> None:
        return await self.repository.delete(id=booking_id)

    async def edit(self, booking_id: uuid.UUID, dto: BookingEdit) -> Booking:
        booking = await self.repository.find_one_or_fail(id=booking_id)
        if dto.end_time:
            booking.end_time = datetime.fromtimestamp(dto.end_time)
        if dto.start_time:
            booking.start_time = datetime.fromtimestamp(dto.start_time)
        return await self.repository.save(booking)
