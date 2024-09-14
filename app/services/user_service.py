from app.dto.note_dto import BaseNoteModel
from app.dto.user_dto import BaseUserModel
from app.services.base import BaseService


class UserService(BaseService):
    async def get_user(self, user_id: int, dump: bool = True):
        user = await self.repository.get_item(user_id)
        return await self.model_dump(user, BaseUserModel) if dump else user

    async def get_all_notes(self, user_id: int):
        user = await self.repository.get_item(user_id)
        return await self.dump_items(user.notes, BaseNoteModel)
