import uuid
from typing import Any, List

from fastapi import APIRouter, Depends, status

from internal.dto.user import (

    UserRead,
    UserFilter, UserEdit, PasswordUser,
)
from internal.entity.user import User
from internal.service.user import UserService
from internal.usecase.utils import SuccessfulResponse, response

router = APIRouter()


@router.get('', response_model=List[UserRead])
async def read_users(
        dto: UserFilter = Depends(),
        user_service: UserService = Depends(),
) -> Any:
    users = await user_service.find(dto)
    return users


@router.post(
    path='',
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
        dto: PasswordUser,
        user_service: UserService = Depends(),
) -> User:
    return await user_service.create(dto)


@router.delete(
    path='/{user_id}',
    responses=response.HTTP_404_NOT_FOUND(
        'User not found',
    ) | SuccessfulResponse.schema(),
)
async def delete_user(
        user_id: uuid.UUID,
        user_service: UserService = Depends(),
) -> SuccessfulResponse:
    await user_service.delete(user_id)
    return SuccessfulResponse()


@router.patch(
    path='/{user_id}',
    responses=response.HTTP_404_NOT_FOUND(
        'User not found',
    ) | SuccessfulResponse.schema(),
)
async def edit_user(
        user_id: uuid.UUID,
        dto: UserEdit,
        user_service: UserService = Depends(),
) -> SuccessfulResponse:
    await user_service.edit(user_id, dto)
    return SuccessfulResponse()
