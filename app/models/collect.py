from fastapi import UploadFile, File
from pydantic import Field, FilePath, BaseModel

from typing import Optional

from .base import Base


class CollectBase(Base):
    user_id: str = Field(...)
    name: Optional[str] = None
    description: Optional[str] = None


class CollectCreate(CollectBase):
    file: UploadFile = File(...)


class CollectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    file: Optional[UploadFile] = None


class Collect(CollectBase):
    file: FilePath = Field(...)
