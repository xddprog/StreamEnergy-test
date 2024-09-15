from typing import Annotated
from fastapi import APIRouter, Depends, Query

from dto.task_dto import AddTaskForm, BaseTaskModel, UpdateTaskForm
from dto.user_dto import BaseUserModel
from services.task_service import TaskService
from services.task_tag_service import TaskTagService
from services.user_service import UserService
from utils.dependencies import (
    get_current_user_dependency,
    get_task_service,
    get_task_tag_service,
    get_user_service,
)


router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
)


@router.get("/filter")
async def get_all_tasks(
    user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
    tasks_service: Annotated[TaskService, Depends(get_task_service)],
    task_tags_service: Annotated[
        TaskTagService, Depends(get_task_tag_service)
    ],
    tags: list = Query(),
) -> list[BaseTaskModel]:
    tags = [await task_tags_service.get_tag(int(tag)) for tag in tags]
    return await tasks_service.tasks_by_tags(user.id, tags)


@router.post("")
async def add_task(
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


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    user: Annotated[BaseUserModel, Depends(get_current_user_dependency)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> dict[str, str]:
    await task_service.delete_note(task_id, user.id)
    return {"detail": "Задача удалена"}


@router.put("/{task_id}")
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
