import os
from litestar import Litestar
from litestar.di import Provide
from litestar.openapi import OpenAPIConfig
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.controllers.user_controller import UserController
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.models.user import Base


DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://postgres:zaripov_2002@localhost/lab_2"
)

engine = create_async_engine(
    DATABASE_URL, 
    echo=True,  
    future=True
)

async_session_factory = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)


async def provide_db_session() -> AsyncSession:
    """
    Провайдер сессии базы данных
    """
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    """
    Провайдер репозитория пользователей
    """
    return UserRepository()


async def provide_user_service(
    user_repository: UserRepository,
    db_session: AsyncSession
) -> UserService:
    """
    Провайдер сервиса пользователей
    """
    return UserService(user_repository, db_session)


async def init_database() -> None:
    """
    Инициализация базы данных
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = Litestar(
    route_handlers=[UserController],
    dependencies={
        "db_session": Provide(provide_db_session),
        "user_repository": Provide(provide_user_repository),
        "user_service": Provide(provide_user_service),
    },
    on_startup=[init_database], 
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
