from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import Result, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import MappedColumn

from app.database.models import ModelType


class BaseRepository(ABC):
    @abstractmethod
    async def get_item(self, item_id: int) -> ModelType | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_items(self) -> list[ModelType] | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_attribute(
        self, attribute: MappedColumn[Any], value: int
    ) -> list[ModelType] | None:
        raise NotImplementedError

    @abstractmethod
    async def add_item(self, **kwargs: str | int | ModelType) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    async def delete_item(self, item: ModelType) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_item(
        self, item_id: int | str, **update_values: str | int | ModelType
    ) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    def get_model(self, **kwargs: str | int | ModelType) -> ModelType:
        raise NotImplementedError


class SqlAlchemyRepository(BaseRepository):
    model: ModelType

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_item(self, item_id: int) -> ModelType | None:
        item = await self.session.get(self.model, item_id)

        return item

    async def get_all_items(self) -> list[ModelType]:
        query = select(self.model)
        items: Result = await self.session.execute(query)

        return items.scalars().all()

    async def get_by_attribute(
        self, attribute: MappedColumn[Any], value: str | int
    ) -> list[ModelType] | None:
        query = select(self.model).where(attribute == value)
        items: Result = await self.session.execute(query)

        return items.scalars().all()

    async def add_item(self, **kwargs: int | str) -> ModelType:
        item = self.model(**kwargs)

        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)

        return item

    async def delete_item(self, item: ModelType) -> None:
        await self.session.delete(item)
        await self.session.commit()

    async def update_item(self, item_id: int, **update_values) -> ModelType:
        query = (
            update(self.model)
            .where(self.model.id == item_id)
            .values(update_values)
            .returning(self.model)
        )

        item: Result = await self.session.execute(query)
        await self.session.commit()

        return item.scalars().all()[0]

    async def get_model(self, **kwargs: int | str) -> ModelType:
        return self.model(**kwargs)
