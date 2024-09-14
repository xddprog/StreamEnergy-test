from app.database.models.models import User
from app.repositories.base import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    model = User
