from datetime import datetime
import uuid
from typing import Sequence, Any

from fastapi import Depends
from pytorm.repository import InjectRepository
from sqlalchemy.ext.asyncio import AsyncSession

from internal.dto.booking import (
    BookingFilter,
    BaseBooking, BookingEdit, BookingCreate, BookingCreateFull
)
from internal.dto.device import DeviceFilter
from internal.entity.booking import Booking
from internal.service.device import DeviceService
from internal.usecase.utils import get_session
from internal.usecase import scheduler
import time


class BookingService(object):

    def __init__(
            self, session: AsyncSession = Depends(get_session),
    ) -> None:
        self.repository = InjectRepository(Booking, session)

    async def set_device_available(self, booking_id: uuid.UUID):
        booking = await self.repository.find_one_or_fail(id=booking_id)
        booking.device.is_available = True
        await self.repository.save(booking)

    async def set_device_unavailable(self, booking_id: uuid.UUID):
        booking = await self.repository.find_one_or_fail(id=booking_id)
        booking.device.is_available = False
        await self.repository.save(booking)

    async def create(self, dto: BookingCreateFull) -> Booking | None:
        dto.start_time = datetime.fromtimestamp(dto.start_time)
        dto.end_time = datetime.fromtimestamp(dto.end_time)
        booking = self.repository.create(**dto.dict())
        await self.repository.save(booking)
        bookings = await self.repository.find(device_id=dto.device_id)
        if any([(dto.start_time < b.start_time < dto.end_time) or
                (b.start_time < dto.start_time < b.end_time) for b in
                bookings]):
            return await self.repository.delete(booking)
        scheduler.add_job(self.set_device_unavailable, 'date',
                          run_date=dto.start_time, id=f'{booking.id}__start',
                          args=[booking.id])
        scheduler.add_job(self.set_device_available, 'date',
                          run_date=dto.end_time, id=f'{booking.id}__end',
                          args=[booking.id])
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
        start_job = scheduler.get_job(f'{booking_id}__start')
        end_job = scheduler.get_job(f'{booking_id}__end')
        if start_job and not end_job:
            await self.set_device_available(booking_id)
        return await self.repository.delete(id=booking_id)

    async def edit(self, booking_id: uuid.UUID, dto: BookingEdit) -> Booking:
        booking = await self.repository.find_one_or_fail(id=booking_id)
        start_time = dto.start_time or booking.start_time.timestamp()
        end_time = dto.end_time or booking.end_time.timestamp()
        dto = {'start_time': start_time, 'end_time': end_time}
        await self.delete(booking_id)
        booking = await self.create(dto=BookingCreateFull(**dto))
        return await self.repository.save(booking)
