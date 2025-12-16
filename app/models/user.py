from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from uuid import uuid4, UUID

Base = declarative_base()

class User(Base):
    """Модель пользователя для базы данных"""
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(onupdate=datetime.now, default=datetime.now)
    description: Mapped[str] = mapped_column(nullable=True, unique=False)
    # addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
