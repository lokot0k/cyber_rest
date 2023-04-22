import sqlalchemy as sa
from sqlalchemy.orm import relationship

from internal.entity.base import Base


class User(Base):
    username = sa.Column(sa.Text(), nullable=False)
    password = sa.Column(sa.Text(), nullable=False)
    bookings = relationship("Booking",back_populates='user')
    __table_args__ = (
        sa.UniqueConstraint('username', name='user_username_key'),
    )
