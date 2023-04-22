import uuid
from typing import Sequence

from fastapi import Depends
from pytorm.repository import InjectRepository
from sqlalchemy.ext.asyncio import AsyncSession

from internal.dto.user import (
    UserFilter,
    BaseUser, UserEdit,
)
from internal.entity.user import User
from internal.usecase.utils import get_session


class UserService(object):

    def __init__(
            self, session: AsyncSession = Depends(get_session),
    ) -> None:
        self.repository = InjectRepository(User, session)

    async def create(self, dto: BaseUser) -> User:
        user = self.repository.create(**dto.dict())
        return await self.repository.save(user)

    async def find(self, dto: UserFilter) -> Sequence[User]:
        return await self.repository.find(
            User.username.contains(dto.username),
        )

    async def find_one_or_fail(self, user_id: uuid.UUID) -> User:
        return await self.repository.find_one_or_fail(
            id=user_id,
        )

    async def delete(self, user_id: uuid.UUID) -> None:
        return await self.repository.delete(id=user_id)

    async def edit(self, user_id: uuid.UUID, dto: UserEdit) -> User:
        user = await self.repository.find_one_or_fail(id=user_id)
        if dto.username:
            user.username = dto.username
        if dto.password:
            user.password = dto.password
        return await self.repository.save(user)
