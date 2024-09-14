from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.database.models import Base
from app.utils.config.schemas import DatabaseConfig


class DatabaseConnection:
    def __init__(self, config: DatabaseConfig):
        self.__engine = create_async_engine(
            url=f"postgresql+asyncpg://{config.db_user}:{config.db_pass}"
            f"@{config.db_host}:{config.db_port}/{config.db_name}",
            pool_size=100,
        )

    async def get_session(self) -> AsyncSession:
        return AsyncSession(self.__engine)

    async def create_tables(self):
        async with self.__engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
