from pydantic import Field, EmailStr
from pydantic.main import BaseModel

from app.models.role import RoleEnum
from app.models.config import USERPROFILE_DOC_TYPE


from typing import Optional, Union, List

from .base import Base


class UserBase(Base):
    email: EmailStr = Field(...)  # ... indicate the field is required
    username: str = Field(...)
    admin_roles: Optional[List[Union[str, RoleEnum]]] = None
    admin_channels: Optional[List[Union[str, RoleEnum]]] = None
    disabled: Optional[bool] = None


class UserCreate(UserBase):
    password: str
    admin_roles: List[Union[str, RoleEnum]] = []
    admin_channels: List[Union[str, RoleEnum]] = None
    disabled: bool = False


class UserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class UserUpdateInDB(UserUpdate):
    hashed_password: Optional[str] = None


class User(UserBase):
    pass


class UserInDB(UserBase):
    type: str = USERPROFILE_DOC_TYPE
    hashed_password: str
    username: str
