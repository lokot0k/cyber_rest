import sqlalchemy as sa
from sqlalchemy.orm import relationship

from internal.entity.base import Base


class Device(Base):
    name = sa.Column(sa.Text(), nullable=False)
    description = sa.Column(sa.Text(), nullable=False)
    bookings = relationship('Booking', back_populates='device')
    is_available = sa.Column(sa.Boolean(), nullable=False, default=True)
