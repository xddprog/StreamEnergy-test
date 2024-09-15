from pydantic import BaseModel

from app.dto.user_dto import BaseUserModel


class RegisterForm(BaseModel):
    login: str
    password: str
    tg_id: int


class LoginForm(BaseModel):
    login: str
    password: str


class RegisterResponse(BaseModel):
    detail: str
    new_user: BaseUserModel
    token: str


class LoginResponse(BaseModel):
    detail: str
    user: BaseUserModel
    token: str
