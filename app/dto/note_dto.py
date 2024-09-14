from pydantic import BaseModel

from app.dto.note_tags_dto import BaseNoteTagModel


class BaseNoteModel(BaseModel):
    title: str
    description: str
    tags: list[BaseNoteTagModel]


class AddNoteForm(BaseNoteModel):
    tags: list[int]
