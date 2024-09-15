from app.dto.task_tags_dto import BaseTaskTagModel
from app.repositories.task_tag_repository import TaskTagRepository
from app.services.base import BaseService


class TaskTagService(BaseService):
    repository: TaskTagRepository

    async def add_tag(self, value: str) -> BaseTaskTagModel:
        return await self.repository.add_item(value=value)

    async def get_tag(
        self, tag_id: int, dump: bool = True
    ) -> BaseTaskTagModel:
        tag = await self.repository.get_item(tag_id)
        return await self.model_dump(tag, BaseTaskTagModel) if dump else tag
