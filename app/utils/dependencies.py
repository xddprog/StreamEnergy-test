from typing import Annotated
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, Request

from dto.user_dto import BaseUserModel
from repositories.task_repository import TaskRepository
from repositories.task_tag_repository import TaskTagRepository
from repositories.user_repository import UserRepository
from services.auth_service import AuthService
from services.task_service import TaskService
from services.task_tag_service import TaskTagService
from services.user_service import UserService


bearer = HTTPBearer(auto_error=False)


async def get_session(request: Request) -> AsyncSession:
    return await request.app.state.db_connection.get_session()


async def get_auth_service(
    session: AsyncSession = Depends(get_session),
) -> AuthService:
    return AuthService(repository=UserRepository(session=session))


async def get_user_service(
    session: AsyncSession = Depends(get_session),
) -> UserService:
    return UserService(repository=UserRepository(session=session))


async def get_task_service(
    session: AsyncSession = Depends(get_session),
) -> UserService:
    return TaskService(repository=TaskRepository(session=session))


async def get_task_tag_service(
    session: AsyncSession = Depends(get_session),
) -> UserService:
    return TaskTagService(repository=TaskTagRepository(session=session))


async def get_current_user_dependency(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    token: Annotated[HTTPBearer, Depends(bearer)],
) -> BaseUserModel:
    username = await auth_service.verify_token(token)
    return await auth_service.check_user_exist(username)
