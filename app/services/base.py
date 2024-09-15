from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Table

from database.models import ModelType
from repositories.base import BaseRepository


class BaseService:
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    async def check_item(self, item_id, error: HTTPException) -> ModelType:
        item = await self.repository.get_item(item_id)

        if not item:
            raise error

        return item

    @staticmethod
    async def model_dump(db_model: Table, dto_model: BaseModel) -> BaseModel:
        return dto_model.model_validate(db_model, from_attributes=True)

    async def dump_items(
        self, db_models: list[Table], dto_model: BaseModel
    ) -> list[BaseModel] | list:
        return [await self.model_dump(model, dto_model) for model in db_models]
