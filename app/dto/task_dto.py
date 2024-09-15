from pydantic import BaseModel

from app.dto.task_tags_dto import BaseTaskTagModel


class BaseTaskModel(BaseModel):
    title: str
    description: str
    tags: list[BaseTaskTagModel]


class AddTaskForm(BaseTaskModel):
    tags: list[int]


class UpdateTaskForm(BaseTaskModel):
    title: str | None = None
    description: str | None = None
    tags: list[int] | None = None
