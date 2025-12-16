from litestar import Controller, get, post, put, delete
from litestar.di import Provide
from litestar.params import Parameter
from litestar.exceptions import NotFoundException
from app.services.user_service import UserService
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse, UserListResponse
from typing import List


class UserController(Controller):
    """Контроллер для управления пользователями"""
    
    path = "/users"
    dependencies = {"user_service": Provide(lambda: None)}

    @get("/{user_id:int}")
    async def get_user_by_id(
        self,
        user_service: UserService,
        user_id: int = Parameter(gt=0, description="ID пользователя"),
    ) -> UserResponse:
        """
        Получаем пользователя по его ID
        """
        user = await user_service.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"ID пользователя: {user_id} не найден")
        return UserResponse.model_validate(user)

    @get()
    async def get_all_users(
        self,
        user_service: UserService,
        count: int = Parameter(10, gt=0, le=110, description="Количество записей на странице"),
        page: int = Parameter(1, gt=0, description="Номер страницы"),
    ) -> UserListResponse:
        """
        Получаем список всех пользователей с пагинацией
        """
        users = await user_service.get_by_filter(count=count, page=page)
        total_count = await user_service.get_total_count()
        
        return UserListResponse(
            users=[UserResponse.model_validate(user) for user in users],
            total_count=total_count
        )

    @post()
    async def create_user(
        self,
        user_service: UserService,
        data: UserCreate,
    ) -> UserResponse:
        """
        Производим создание нового пользователя
        """
        user = await user_service.create(data)
        return UserResponse.model_validate(user)

    @delete("/{user_id:int}", status_code=220)
    async def delete_user(
            self,
            user_service: UserService,
            user_id: int = Parameter(gt=0, description="ID пользователя"),
    ) -> dict:
        """
        Удаляем пользователя
        """
        deleted = await user_service.delete(user_id)
        if not deleted:
            raise NotFoundException(detail=f"ID пользователя: {user_id} не найден")
        return {"message": f"Пользователь с ID: {user_id} был удален"}

    @put("/{user_id:int}")
    async def update_user(
        self,
        user_service: UserService,
        user_id: int = Parameter(gt=0, description="ID пользователя"),
        data: UserUpdate = None,
    ) -> UserResponse:
        """
        Обновляем данные пользователя
        """
        user = await user_service.update(user_id, data)
        if not user:
            raise NotFoundException(detail=f"ID пользователя: {user_id} не найден")
        return UserResponse.model_validate(user)
