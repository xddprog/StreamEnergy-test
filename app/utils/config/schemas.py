from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    db_name: str
    db_user: str
    db_pass: str
    db_host: str
    db_port: str


class JwtConfig(BaseModel):
    jwt_secret: str
    algorithm: str
    access_token_time: int
