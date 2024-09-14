from typing import Annotated
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, Request

from app.dto.user_dto import BaseUserModel
from app.repositories.note_repository import NoteRepository
from app.repositories.note_tag_repositories import NoteTagRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.note_service import NoteService
from app.services.note_tag_service import NoteTagService
from app.services.user_service import UserService


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


async def get_note_service(
    session: AsyncSession = Depends(get_session),
) -> UserService:
    return NoteService(repository=NoteRepository(session=session))


async def get_note_tag_service(
    session: AsyncSession = Depends(get_session),
) -> UserService:
    return NoteTagService(repository=NoteTagRepository(session=session))


async def get_current_user_dependency(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    token: Annotated[HTTPBearer, Depends(bearer)],
) -> BaseUserModel:
    username = await auth_service.verify_token(token)
    return await auth_service.check_user_exist(username)
