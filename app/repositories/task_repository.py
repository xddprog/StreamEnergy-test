from sqlalchemy import Result, select

from database.models.models import Task, TaskTag, User
from repositories.base import SqlAlchemyRepository


class TaskRepository(SqlAlchemyRepository):
    model = Task

    async def tasks_by_tags(
        self, user_id: int, tags: list[TaskTag]
    ) -> list[Task]:
        query = (
            select(self.model)
            .join(User)
            .where(
                User.id == user_id,
                self.model.tags.any(Task.id.in_([tag.id for tag in tags])),
            )
        )

        items: Result = await self.session.execute(query)

        return items.scalars().all()
