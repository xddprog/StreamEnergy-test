from app.database.models.models import Task
from app.repositories.base import SqlAlchemyRepository


class TaskRepository(SqlAlchemyRepository):
    model = Task
