from database.models.models import User
from repositories.base import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    model = User
