from app.database.models.models import TaskTag
from app.repositories.base import SqlAlchemyRepository


class TaskTagRepository(SqlAlchemyRepository):
    model = TaskTag
