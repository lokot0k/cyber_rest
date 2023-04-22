import sqlalchemy as sa
from sqlalchemy.orm import relationship

from internal.entity.base import Base
from sqlalchemy.dialects import postgresql as psql


class Booking(Base):
    user_id = sa.Column(psql.UUID(as_uuid=True),sa.ForeignKey('user.id'))
    device_id = sa.Column(psql.UUID(as_uuid=True), sa.ForeignKey('device.id'))
    user = relationship("User", back_populates='bookings')
    device = relationship('Device', back_populates='bookings')
    start_time = sa.Column(sa.DateTime(), nullable=False)
    end_time = sa.Column(sa.DateTime(), nullable=False)
