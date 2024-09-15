from pydantic import BaseModel


class BaseTaskTagModel(BaseModel):
    id: int
    value: str
