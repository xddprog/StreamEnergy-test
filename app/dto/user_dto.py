from pydantic import BaseModel


class BaseUserModel(BaseModel):
    id: int
    login: str
