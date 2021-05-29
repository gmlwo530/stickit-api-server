from typing import Generic, Any, TypeVar, Optional, Dict, List


from app.core.config import PAGINATION_COUNT
from app.core.upload import Upload

from pydantic import BaseModel

from fastapi.encoders import jsonable_encoder
from starlette.datastructures import UploadFile

from motor.motor_asyncio import AsyncIOMotorDatabase

from pymongo import DESCENDING, ASCENDING
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult

from .utils.exceptions import CRUDException

from pathlib import Path

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

DESC = DESCENDING
ASC = ASCENDING


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: BaseModel):
        self.model = model
        self.model_name = model.__name__.lower()

    async def get(self, db: AsyncIOMotorDatabase, id: Any) -> Optional[ModelType]:
        document: Dict = await db[self.model_name].find_one({"_id": str(id)})

        if document:
            return self.model(**document)
        return None

    async def get_many(
        self,
        db: AsyncIOMotorDatabase,
        *,
        filter: Dict,
        sort=[],
        page=0,
    ) -> List[ModelType]:
        skip, limit = (
            page * PAGINATION_COUNT,
            PAGINATION_COUNT,
        )
        cursor = db[self.model_name].find(filter, skip=skip, limit=limit, sort=sort)
        return [self.model(**doc) for doc in await cursor.to_list(length=None)]

    async def create(
        self, db: AsyncIOMotorDatabase, *, obj_in: CreateSchemaType
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)

        for key, val in obj_in.__dict__.items():
            if isinstance(val, UploadFile):
                file_path = await Upload(getattr(obj_in, key)).save()
                obj_in_data[key] = jsonable_encoder(file_path)

        created: InsertOneResult = await db[self.model_name].insert_one(obj_in_data)
        new_obj: Dict = await db[self.model_name].find_one({"_id": created.inserted_id})

        return self.model(**new_obj)

    async def update(
        self,
        db: AsyncIOMotorDatabase,
        *,
        obj: ModelType,
        obj_in: UpdateSchemaType,
    ) -> ModelType:
        old_obj_id = str(obj.id)
        updated_file_paths: List[Path] = []
        obj_in_data = jsonable_encoder(obj_in, exclude_none=True, exclude={"_id"})

        for key, val in obj_in.__dict__.items():
            if isinstance(val, UploadFile):
                updated_file_paths.append(getattr(obj, key))
                file_path = await Upload(getattr(obj_in, key)).save()
                obj_in_data[key] = jsonable_encoder(file_path)

        result: UpdateResult = await db[self.model_name].update_one(
            {"_id": old_obj_id}, {"$set": obj_in_data}
        )
        if result.modified_count == 0:
            raise CRUDException(f"Update document is failed - {result.raw_result}")

        for path in updated_file_paths:
            path.unlink()

        new_document: Dict = await db[self.model_name].find_one({"_id": old_obj_id})

        return self.model(**new_document)

    async def delete(self, db: AsyncIOMotorDatabase, *, obj: ModelType) -> ModelType:
        old_obj_id = str(obj.id)

        result: DeleteResult = await db[self.model_name].delete_one({"_id": old_obj_id})
        if result.deleted_count == 0:
            raise CRUDException(f"Delete document is failed - {result.raw_result}")

        return obj
