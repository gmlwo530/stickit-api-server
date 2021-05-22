from typing import Union, List

from app.core.upload import Upload
from app.crud.base import CRUDBase
from app.models.collect import Collect, CollectCreate, CollectUpdate

from motor.motor_asyncio import AsyncIOMotorDatabase


class CRUDCollect(CRUDBase[Collect, CollectCreate, CollectUpdate]):
    async def _wrap_to_collect(
        self, obj_in: Union[CollectCreate, CollectUpdate], obj: Collect = None
    ) -> Collect:
        name = obj_in.name or (obj and obj.name)
        description = obj_in.description or (obj and obj.description)
        file_path = await Upload(obj_in.file).save() if obj_in.file else obj.file
        user_id = obj.user_id if obj else obj_in.user_id

        return Collect(
            user_id=user_id, name=name, description=description, file=file_path
        )

    async def get_many(
        self, db: AsyncIOMotorDatabase, *, user_id: str
    ) -> List[Collect]:
        pass

    async def create(
        self, db: AsyncIOMotorDatabase, *, obj_in: CollectCreate
    ) -> Collect:
        return await super().create(db, obj_in=await self._wrap_to_collect(obj_in))

    async def update(
        self, db: AsyncIOMotorDatabase, *, obj: Collect, obj_in: CollectUpdate
    ) -> Collect:
        old_collect_file_path = obj.file

        new_collect = await super().update(
            db, obj=obj, obj_in=await self._wrap_to_collect(obj_in, obj=obj)
        )

        if obj_in.file:
            old_collect_file_path.unlink()

        return new_collect


collect = CRUDCollect(Collect)
