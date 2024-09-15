from app.dto.task_dto import BaseTaskModel, UpdateTaskForm
from app.errors.note_errors import NoteNotFound
from app.repositories.task_repository import TaskRepository
from app.services.base import BaseService


class TaskService(BaseService):
    repository: TaskRepository
    
    async def get_task(self, task_id: int, user_id: int) -> BaseTaskModel:
        return await self.check_item(user_id, task_id)
    
    async def add_task(self, user: int, form: BaseTaskModel) -> BaseTaskModel:
        return await self.repository.add_item(**form.model_dump(), user=user)

    async def check_item(self, user_id: int, task_id: int) -> None:
        task = await self.repository.get_item(task_id)

        if not task or task.user.id != user_id:
            raise NoteNotFound

        return task

    async def delete_note(self, task_id: int, user_id: int) -> None:
        task = await self.check_item(user_id, task_id)
        return await self.repository.delete_item(task)

    async def update_task(
        self, task_id: int, user_id: int, form: UpdateTaskForm
    ) -> BaseTaskModel:
        await self.check_item(user_id, task_id)
        return await self.repository.update_item(task_id, **form.model_dump())
