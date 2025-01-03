from dto.task_dto import BaseTaskModel
from dto.user_dto import BaseUserModel
from errors.user_errors import UserNotFound
from services.base import BaseService


class UserService(BaseService):
    async def get_user(self, user_id: int, dump: bool = True):
        user = await self.check_item(user_id, UserNotFound)
        return await self.model_dump(user, BaseUserModel) if dump else user

    async def get_all_tasks(self, user_id: int):
        user = await self.repository.get_item(user_id)
        return await self.dump_items(user.tasks, BaseTaskModel)
