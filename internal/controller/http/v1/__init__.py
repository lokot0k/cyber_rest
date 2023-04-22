from fastapi import APIRouter

from . import users, health, devices, booking

router = APIRouter()
router.include_router(
    users.router,
    prefix='/users',
    tags=['users'],
)
router.include_router(
    health.router,
    prefix='/health',
    tags=['health'],
)
router.include_router(
    devices.router,
    prefix='/devices',
    tags=['devices'],
)
router.include_router(
    booking.router,
    prefix='/bookings',
    tags=['booking'],
)
