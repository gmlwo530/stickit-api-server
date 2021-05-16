from app.crud.base import CRUDBase
from app.core.security import verify_password, get_password_hash
from app.models.user import User, UserInDB, UserCreate, UserUpdate
from app.models.role import RoleEnum

from .utils import ensure_enums_to_strs

from fastapi.encoders import jsonable_encoder

from motor.motor_asyncio import AsyncIOMotorDatabase

from pymongo.results import InsertOneResult

from typing import Optional, Dict


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_username(
        self, db: AsyncIOMotorDatabase, *, username: str
    ) -> Optional[UserInDB]:
        document: Dict = await db[self.model_name].find_one({"username": username})

        if document:
            return UserInDB(**document)
        return None

    async def get_by_email(
        self, db: AsyncIOMotorDatabase, *, email: str
    ) -> Optional[User]:
        document: Dict = await db[self.model_name].find_one({"email": email})

        if document:
            return self.model(**document)
        return None

    async def create(self, db: AsyncIOMotorDatabase, *, obj_in: UserCreate) -> User:
        db_obj = UserInDB(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
        )
        obj_in_data = jsonable_encoder(db_obj)

        created: InsertOneResult = await db[self.model_name].insert_one(obj_in_data)
        new_obj: Dict = await db[self.model_name].find_one({"_id": created.inserted_id})
        return self.model(**new_obj)

    async def authenticate(
        self, db: AsyncIOMotorDatabase, *, username: str, password: str
    ) -> Optional[User]:
        user = await self.get_by_username(db, username=username)

        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None

        return user

    def is_active(self, user: UserInDB):
        return not user.disabled

    def is_superuser(self):
        return RoleEnum.superuser.value in ensure_enums_to_strs(self.admin_roles or [])


user = CRUDUser(User)
