from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from ..models.user import User
from ..schemas.user_schema import UserCreate, UserUpdate
from typing import Optional


class UserRepository:
    """Репозиторий для работы с пользователями в базе данных"""

    async def get_by_id(self, session: AsyncSession, user_id: int) -> Optional[User]:
        """
        Получить пользователя по его ID
        """
        result = await session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_filter(
        self, 
        session: AsyncSession, 
        count: int = 10, 
        page: int = 1, 
        **kwargs
    ) -> list[User]:
        """
        Получаем список пользователей с фильтрацией и пагинацией
        """
        query = select(User)

        if "username" in kwargs and kwargs["username"]:
            query = query.where(User.username == kwargs["username"])
        if "email" in kwargs and kwargs["email"]:
            query = query.where(User.email == kwargs["email"])

        offset = (page - 1) * count

        query = query.offset(offset).limit(count)
        
        result = await session.execute(query)
        return list(result.scalars().all())

    async def get_total_count(self, session: AsyncSession) -> int:
        """
        Получаем общее количество пользователей, которые хранятся в базе данных
        """
        result = await session.execute(select(func.count(User.id)))
        return result.scalar_one()

    async def create(self, session: AsyncSession, user_data: UserCreate) -> User:
        """
        Создаем нового пользователя
        """
        user = User(
            username=user_data.username,
            email=user_data.email,
            description=user_data.description
            # addresses=user_data.addresses 
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def update(
        self, 
        session: AsyncSession, 
        user_id: int, 
        user_data: UserUpdate
    ) -> Optional[User]:
        """
        Обновляем данные пользователя
        """
        user = await self.get_by_id(session, user_id)
        if not user:
            return None

        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await session.commit()
        await session.refresh(user)
        return user

    async def delete(self, session: AsyncSession, user_id: int) -> bool:
        """
        Удаляем пользователя
        """
        user = await self.get_by_id(session, user_id)
        if not user:
            return False
        
        await session.delete(user)
        await session.commit()
        return True
