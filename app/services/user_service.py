from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional


class UserService:
    """Сервисный слой для работы с пользователями"""
    
    def __init__(self, user_repository: UserRepository, db_session: AsyncSession):
        self.user_repository = user_repository
        self.db_session = db_session

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Получаем пользователя по ID
        """
        return await self.user_repository.get_by_id(self.db_session, user_id)

    async def get_by_filter(
        self, 
        count: int = 10, 
        page: int = 1, 
        **kwargs
    ) -> list[User]:
        """
        Получаем список всех пользователей с фильтрацией
        """
        return await self.user_repository.get_by_filter(
            self.db_session, count, page, **kwargs
        )

    async def get_total_count(self) -> int:
        """
        Получаем количество всех пользователей
        """
        return await self.user_repository.get_total_count(self.db_session)

    async def create(self, user_data: UserCreate) -> User:
        """
        Создаем нового пользователя
        """
        return await self.user_repository.create(self.db_session, user_data)

    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """
        Обновляем данные пользователя
        """
        return await self.user_repository.update(self.db_session, user_id, user_data)

    async def delete(self, user_id: int) -> bool:
        """
        Удаляем пользователя
        """
        return await self.user_repository.delete(self.db_session, user_id)
