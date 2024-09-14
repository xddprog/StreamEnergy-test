from app.database.models.models import NoteTag
from app.repositories.base import SqlAlchemyRepository


class NoteTagRepository(SqlAlchemyRepository):
    model = NoteTag
