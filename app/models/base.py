from pydantic import BaseModel, Field

from bson import ObjectId

from app.db.database import PyObjectId


class Base(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
