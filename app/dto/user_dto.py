from pydantic import BaseModel


class BaseUserModel(BaseModel):
    id: int
    login: str
    tg_id: int
