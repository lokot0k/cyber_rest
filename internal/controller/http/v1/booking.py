import uuid
from typing import Any, List

from fastapi import APIRouter, Depends, status

from internal.dto.booking import (

    BookingRead, BaseBooking,
    BookingFilter, BookingEdit,
    BookingCreate
)
from internal.entity.booking import Booking
from internal.service.booking import BookingService
from internal.usecase.utils import SuccessfulResponse, response

router = APIRouter()


@router.get('', response_model=List[BookingRead])
async def read_bookings(
        dto: BookingFilter = Depends(),
        booking_service: BookingService = Depends(),
) -> Any:
    bookings = await booking_service.find(dto)
    return bookings


@router.post(
    path='',
    response_model=BookingRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_booking(
        dto: BookingCreate,
        booking_service: BookingService = Depends(),
) -> Booking:
    return await booking_service.create(dto)


@router.delete(
    path='/{booking_id}',
    responses=response.HTTP_404_NOT_FOUND(
        'Booking not found',
    ) | SuccessfulResponse.schema(),
)
async def delete_booking(
        booking_id: uuid.UUID,
        booking_service: BookingService = Depends(),
) -> SuccessfulResponse:
    await booking_service.delete(booking_id)
    return SuccessfulResponse()


@router.patch(
    path='/{booking_id}',
    responses=response.HTTP_404_NOT_FOUND(
        'Booking not found',
    ) | SuccessfulResponse.schema(),
)
async def edit_booking(
        booking_id: uuid.UUID,
        dto: BookingEdit,
        booking_service: BookingService = Depends(),
) -> SuccessfulResponse:
    await booking_service.edit(booking_id, dto)
    return SuccessfulResponse()
