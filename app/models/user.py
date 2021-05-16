from pydantic import Field, EmailStr

from app.db.database import PyObjectId
from app.models.role import RoleEnum
from app.models.config import USERPROFILE_DOC_TYPE

from bson import ObjectId

from typing import Optional, Union, List

from .base import Base


class UserBase(Base):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr = Field(...)  # ... indicate the field is required
    username: str = Field(...)
    admin_roles: Optional[List[Union[str, RoleEnum]]] = None
    admin_channels: Optional[List[Union[str, RoleEnum]]] = None
    disabled: Optional[bool] = None

    class Config:
        # whether an aliased field may be populated by its name as given by the model attribute,
        # as well as the alias
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        # schema_extra = {
        #     "example": {
        #         "email": "example@example.com",
        #         "username": "CHOI HEE JAE",
        #     }
        # }


class UserCreate(UserBase):
    password: str
    admin_roles: List[Union[str, RoleEnum]] = []
    admin_channels: List[Union[str, RoleEnum]] = None
    disabled: bool = False


class UserUpdate(UserBase):
    email: Optional[str]
    password: Optional[str]


class User(UserBase):
    pass


class UserInDB(UserBase):
    type: str = USERPROFILE_DOC_TYPE
    hashed_password: str
    username: str
