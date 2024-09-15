from typing import Annotated
from fastapi import APIRouter, Depends

from dto.task_dto import BaseTaskModel
from dto.user_dto import BaseUserModel
from services.user_service import UserService
from utils.dependencies import (
    get_current_user_dependency,
    get_user_service,
)


router = APIRouter(
    prefix="/api/user",
    tags=["user"],
)


@router.get("/tasks/all")
async def get_all_notes(
    user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> list[BaseTaskModel]:
    return await user_service.get_all_tasks(user.id)
