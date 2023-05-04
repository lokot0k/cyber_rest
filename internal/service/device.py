import uuid
from typing import Sequence

from fastapi import Depends
from pytorm.repository import InjectRepository
from sqlalchemy.ext.asyncio import AsyncSession

from internal.dto.device import (
    DeviceFilter,
    BaseDevice, DeviceEdit,
)
from internal.entity.device import Device
from internal.usecase.utils import get_session


class DeviceService(object):

    def __init__(
            self, session: AsyncSession = Depends(get_session),
    ) -> None:
        self.repository = InjectRepository(Device, session)

    async def create(self, dto: BaseDevice) -> Device:
        device = self.repository.create(**dto.dict())
        return await self.repository.save(device)

    async def find(self, dto: DeviceFilter) -> Sequence[Device]:
        if dto.is_available is not None:
            return await self.repository.find(
                Device.name.contains(dto.name),
                Device.description.contains(dto.description),
                Device.is_available.is_(dto.is_available)
            )
        return await self.repository.find(
            Device.name.contains(dto.name),
            Device.description.contains(dto.description),
        )

    async def find_by_id(self, device_id: uuid.UUID) -> Device:
        return await self.repository.find_one_or_fail(id=device_id)

    async def delete(self, device_id: uuid.UUID) -> None:
        return await self.repository.delete(id=device_id)

    async def edit(self, device_id: uuid.UUID, dto: DeviceEdit) -> Device:
        device = await self.repository.find_one_or_fail(id=device_id)
        if dto.name:
            device.name = dto.name
        if dto.description:
            device.description = dto.description
        return await self.repository.save(device)
