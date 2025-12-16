from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4, UUID
from sqlalchemy import ForeignKey

from user import Base


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    # user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    address_id: Mapped[UUID] = mapped_column(ForeignKey('addresses.id'), nullable=False)
    product_id: Mapped[UUID] = mapped_column(ForeignKey('products.id'), nullable=False)

    # user = relationship("User")
    address = relationship("Address")
    product = relationship("Product")