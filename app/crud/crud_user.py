from app.crud.base import CRUDBase
from app.core.security import verify_password
from app.models.user import User, UserCreate, UserUpdate
from app.models.role import RoleEnum

from .utils import ensure_enums_to_strs

from motor.motor_asyncio import AsyncIOMotorDatabase

from typing import Optional, Dict


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_username(
        self, db: AsyncIOMotorDatabase, *, username: str
    ) -> Optional[User]:
        document: Dict = await db[self.model_name].find_one({"username": username})

        if document:
            return self.model(**document)
        return None

    async def get_by_email(
        self, db: AsyncIOMotorDatabase, *, email: str
    ) -> Optional[User]:
        document: Dict = await db[self.model_name].find_one({"email": email})

        if document:
            return self.model(**document)
        return None

    async def authenticate(
        self, db: AsyncIOMotorDatabase, *, username: str, password: str
    ):
        user = await self.get_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None

        return user

    def is_active(self):
        return not self.disabled

    def is_superuser(self):
        return RoleEnum.superuser.value in ensure_enums_to_strs(self.admin_roles or [])


user = CRUDUser(User)
