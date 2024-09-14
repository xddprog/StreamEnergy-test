from app.dto.note_tags_dto import BaseNoteTagModel
from app.repositories.note_tag_repositories import NoteTagRepository
from app.services.base import BaseService


class NoteTagService(BaseService):
    repository: NoteTagRepository

    async def add_tag(self, value: str) -> BaseNoteTagModel:
        return await self.repository.add_item(value=value)

    async def get_tag(
        self, tag_id: int, dump: bool = True
    ) -> BaseNoteTagModel:
        tag = await self.repository.get_item(tag_id)
        return await self.model_dump(tag, BaseNoteTagModel) if dump else tag
