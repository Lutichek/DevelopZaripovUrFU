from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4, UUID
from sqlalchemy import ForeignKey

from user import Base

class Address(Base):
    __tablename__ = 'addresses'
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    # user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    street: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=True)
    state: Mapped[str] = mapped_column(nullable=True)
    zip_code: Mapped[str] = mapped_column(nullable=True)
    country: Mapped[str] = mapped_column(nullable=True)
    is_primary: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(onupdate=datetime.now, default=datetime.now)

    # user = relationship("User", back_populates="addresses")