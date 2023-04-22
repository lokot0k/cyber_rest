import uuid
from typing import Any, List

from fastapi import APIRouter, Depends, status

from internal.dto.device import (

    DeviceRead, BaseDevice,
    DeviceFilter, DeviceEdit
)
from internal.entity.device import Device
from internal.service.device import DeviceService
from internal.usecase.utils import SuccessfulResponse, response

router = APIRouter()


@router.get('', response_model=List[DeviceRead])
async def read_devices(
        dto: DeviceFilter = Depends(),
        device_service: DeviceService = Depends(),
) -> Any:
    devices = await device_service.find(dto)
    return devices


@router.post(
    path='',
    response_model=DeviceRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_device(
        dto: BaseDevice,
        device_service: DeviceService = Depends(),
) -> Device:
    return await device_service.create(dto)


@router.delete(
    path='/{device_id}',
    responses=response.HTTP_404_NOT_FOUND(
        'Device not found',
    ) | SuccessfulResponse.schema(),
)
async def delete_device(
        device_id: uuid.UUID,
        device_service: DeviceService = Depends(),
) -> SuccessfulResponse:
    await device_service.delete(device_id)
    return SuccessfulResponse()


@router.patch(
    path='/{device_id}',
    responses=response.HTTP_404_NOT_FOUND(
        'Device not found',
    ) | SuccessfulResponse.schema(),
)
async def edit_device(
        device_id: uuid.UUID,
        dto: DeviceEdit,
        device_service: DeviceService = Depends(),
) -> SuccessfulResponse:
    await device_service.edit(device_id, dto)
    return SuccessfulResponse()
