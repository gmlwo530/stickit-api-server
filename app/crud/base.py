from typing import Generic, Any, TypeVar, Optional, Dict, Union

from pydantic import BaseModel

from fastapi.encoders import jsonable_encoder

from motor.motor_asyncio import AsyncIOMotorDatabase

from pymongo.results import InsertOneResult, UpdateResult, DeleteResult

from .utils.exceptions import CRUDException

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: BaseModel):
        self.model = model
        self.model_name = model.__name__.lower()

    async def get(self, db: AsyncIOMotorDatabase, id: Any) -> Optional[ModelType]:
        document: Dict = await db[self.model_name].find_one({"_id": str(id)})

        if document:
            return self.model(**document)
        return None

    async def create(
        self, db: AsyncIOMotorDatabase, *, obj_in: Union[ModelType, CreateSchemaType]
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        created: InsertOneResult = await db[self.model_name].insert_one(obj_in_data)
        new_obj: Dict = await db[self.model_name].find_one({"_id": created.inserted_id})

        return self.model(**new_obj)

    async def update(
        self,
        db: AsyncIOMotorDatabase,
        *,
        obj: ModelType,
        obj_in: Union[ModelType, UpdateSchemaType],
    ) -> ModelType:
        old_obj_id = str(obj.id)
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data.pop("_id")

        result: UpdateResult = await db[self.model_name].update_one(
            {"_id": old_obj_id}, {"$set": obj_in_data}
        )
        if result.modified_count == 0:
            raise CRUDException(f"Update document is failed - {result.raw_result}")

        new_document: Dict = await db[self.model_name].find_one({"_id": old_obj_id})

        return self.model(**new_document)

    async def delete(self, db: AsyncIOMotorDatabase, *, obj: ModelType) -> ModelType:
        old_obj_id = str(obj.id)

        result: DeleteResult = await db[self.model_name].delete_one({"_id": old_obj_id})
        if result.deleted_count == 0:
            raise CRUDException(f"Delete document is failed - {result.raw_result}")

        return obj
