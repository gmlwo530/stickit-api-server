from dotenv import load_dotenv
from bson import ObjectId

import os
import motor.motor_asyncio

load_dotenv()


def get_database() -> motor.motor_asyncio.AsyncIOMotorDatabase:
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
    return client[os.environ["MONGODB_DATABASE"]]


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
