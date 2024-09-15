from typing import Annotated
from fastapi import APIRouter, Depends

from app.dto.task_dto import AddTaskForm, BaseTaskModel, UpdateTaskForm
from app.dto.user_dto import BaseUserModel
from app.services.task_service import TaskService
from app.services.task_tag_service import TaskTagService
from app.services.user_service import UserService
from app.utils.dependencies import (
    get_current_user_dependency,
    get_task_service,
    get_task_tag_service,
    get_user_service,
)


router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
)


@router.post("/add")
async def add_note(
    user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
    task_tags_service: Annotated[
        TaskTagService, Depends(get_task_tag_service)
    ],
    form: AddTaskForm,
) -> BaseTaskModel:
    user = await user_service.get_user(user.id, dump=False)
    form.tags = [
        await task_tags_service.get_tag(tag_id, dump=False)
        for tag_id in form.tags
    ]
    return await task_service.add_task(user, form)


@router.delete("/{task_id}/delete")
async def delete_note(
    task_id: int,
    user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> dict[str, str]:
    await task_service.delete_note(task_id, user.id)
    return {"detail": "Задача удалена"}


@router.put("/{task_id}/update")
async def update_task(
    task_id: int,
    user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
    form: UpdateTaskForm,
) -> BaseTaskModel:
    return await task_service.update_task(task_id, user.id, form)


@router.get("/{task_id}")
async def get_task(
    task_id: int,
    user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> BaseTaskModel:
    return await task_service.get_task(task_id, user.id)