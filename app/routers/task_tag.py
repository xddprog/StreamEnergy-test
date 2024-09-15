from typing import Annotated
from fastapi import APIRouter, Depends

from services.task_tag_service import TaskTagService
from utils.dependencies import get_task_tag_service


router = APIRouter(
    prefix="/api/tasks_tags",
    tags=["tasks_tags"],
)


@router.get("/all")
async def get_all_tasks_tags(
    task_tag_service: Annotated[TaskTagService, Depends(get_task_tag_service)],
):
    return await task_tag_service.get_all_tags()
