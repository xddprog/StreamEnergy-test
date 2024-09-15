from datetime import datetime, timedelta

from fastapi.security import HTTPBearer
from jwt import InvalidTokenError, encode, decode
from passlib.context import CryptContext

from app.database.models.models import User
from app.dto.auth_dto import LoginForm, RegisterForm
from app.dto.user_dto import BaseUserModel
from app.errors.auth_errors import (
    InvalidLoginData,
    InvalidToken,
    UserAlreadyNotRegister,
    UserAlreadyRegister,
)
from app.repositories.user_repository import UserRepository
from app.services.base import BaseService
from app.utils.config.loads import load_jwt_config


class AuthService(BaseService):
    repository: UserRepository

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.config = load_jwt_config()
        self.context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_user_by_login(self, login: str) -> User:
        user = await self.repository.get_by_attribute(
            self.repository.model.login, login
        )
        return user[0] if user else None

    async def hash_password(self, password: str) -> str:
        return self.context.hash(password)

    async def verify_password(
        self, password: str, hashed_password: str
    ) -> bool:
        return self.context.verify(password, hashed_password)

    async def authenticate_user(self, form: LoginForm) -> User:
        user = await self.get_user_by_login(form.login)

        if not user:
            raise UserAlreadyNotRegister
        if not await self.verify_password(form.password, user.password):
            raise InvalidLoginData

        return await self.model_dump(user, BaseUserModel)

    async def create_access_token(self, login: str) -> str:
        expire = datetime.now() + timedelta(
            minutes=self.config.access_token_time
        )
        data = {"sub": login, "exp": expire}
        token = encode(
            data, self.config.jwt_secret, algorithm=self.config.algorithm
        )

        return token

    async def verify_token(self, token: HTTPBearer) -> dict[str, str]:
        try:
            payload = decode(
                token.credentials,
                self.config.jwt_secret,
                algorithms=[self.config.algorithm],
            )
            login = payload.get("sub")

            if login is None:
                raise InvalidToken

            return login
        except (InvalidTokenError, AttributeError):
            raise InvalidToken

    async def check_user_exist(self, login: str) -> User:
        user = await self.get_user_by_login(login)

        if user is None:
            raise InvalidToken

        return await self.model_dump(user, BaseUserModel)

    async def register_user(self, form: RegisterForm) -> User:
        user = await self.get_user_by_login(form.login)

        if user:
            raise UserAlreadyRegister

        form.password = await self.hash_password(form.password)
        new_user = await self.repository.add_item(**form.model_dump())

        return await self.model_dump(new_user, BaseUserModel)
