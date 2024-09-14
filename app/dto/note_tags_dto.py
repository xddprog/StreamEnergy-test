from pydantic import BaseModel


class BaseNoteTagModel(BaseModel):
    id: int
    value: str
