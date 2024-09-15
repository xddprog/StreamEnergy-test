from database.models.models import TaskTag
from repositories.base import SqlAlchemyRepository


class TaskTagRepository(SqlAlchemyRepository):
    model = TaskTag
