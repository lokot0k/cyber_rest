import uuid
from typing import Any, List, Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from internal.controller.http.v1.auth import get_current_user
from internal.dto.booking import (

    BookingRead,
    BookingFilter, BookingEdit,
    BookingCreate, BookingCreateFull
)
from internal.entity.booking import Booking
from internal.entity.user import User
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
        current_user: Annotated[User, Depends(get_current_user)],
        booking_service: BookingService = Depends(),

) -> Booking:
    full_dto = BookingCreateFull(user_id=current_user.id, **dto.dict())
    return await booking_service.create(full_dto)


@router.delete(
    path='/{booking_id}',
    responses=response.HTTP_404_NOT_FOUND(
        'Booking not found',
    ) | SuccessfulResponse.schema() | response.HTTP_403_FORBIDDEN(
        'Access denied',
    ),
)
async def delete_booking(
        booking_id: uuid.UUID,
        current_user: Annotated[User, Depends(get_current_user)],
        booking_service: BookingService = Depends(),
) -> SuccessfulResponse:
    booking_filter = BookingFilter(user_id=current_user.id, )
    bookings = await booking_service.find(booking_filter)
    if any([booking.id == booking_id for booking in bookings]):
        await booking_service.delete(booking_id)
        return SuccessfulResponse()
    return response.HTTP_403_FORBIDDEN()


@router.patch(
    path='/{booking_id}',
    responses=response.HTTP_404_NOT_FOUND(
        'Booking not found',
    ) | SuccessfulResponse.schema()
)
async def edit_booking(
        booking_id: uuid.UUID,
        current_user: Annotated[User, Depends(get_current_user)],
        dto: BookingEdit,
        booking_service: BookingService = Depends(),
) -> SuccessfulResponse:
    booking = await booking_service.find_one_or_fail(booking_id)
    if booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    await booking_service.edit(booking_id, dto)
    return SuccessfulResponse()
