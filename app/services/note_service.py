from app.database.models.models import User
from app.dto.note_dto import BaseNoteModel
from app.repositories.note_repository import NoteRepository
from app.services.base import BaseService


class NoteService(BaseService):
    repository: NoteRepository

    async def add_note(self, user: User, form: BaseNoteModel):
        return await self.repository.add_item(**form.model_dump(), user=user)
