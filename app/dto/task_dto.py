from datetime import datetime
from pydantic import BaseModel, field_validator

from dto.task_tags_dto import BaseTaskTagModel

months = [
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
]


class BaseTaskModel(BaseModel):
    id: int
    title: str
    description: str
    tags: list[BaseTaskTagModel]
    created_at: datetime | str
    updated_at: datetime | str

    @field_validator("created_at", "updated_at")
    def format_created_at(cls, value: datetime) -> str:
        return f"{value.day} {months[value.month - 1]}, {str(value.hour).zfill(2)}:{value.minute}"


class AddTaskForm(BaseModel):
    title: str
    description: str
    tags: list[int] | None = None


class UpdateTaskForm(BaseModel):
    title: str | None = None
    description: str | None = None
    tags: list[int] | None = None
