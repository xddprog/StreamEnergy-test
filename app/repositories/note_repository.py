from app.database.models.models import Note
from app.repositories.base import SqlAlchemyRepository


class NoteRepository(SqlAlchemyRepository):
    model = Note
