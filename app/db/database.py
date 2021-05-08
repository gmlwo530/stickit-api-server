from dotenv import load_dotenv
from bson import ObjectId

import os
import motor.motor_asyncio

load_dotenv()


def get_database(
    mongodb_url: str = os.environ["MONGODB_URL"],
    database_name: str = "pixhelves_db",
) -> motor.motor_asyncio.AsyncIOMotorDatabase:
    client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_url)
    return client[database_name]


def close_connection(db: motor.motor_asyncio.AsyncIOMotorDatabase):
    db.client.close()


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
