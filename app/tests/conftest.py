from dotenv import load_dotenv

from typing import Generator

from httpx import AsyncClient

from app.main import app
from app.db import database
from app.core import config
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_server_api

import pytest
import motor

load_dotenv()


@pytest.fixture
async def db() -> motor.motor_asyncio.AsyncIOMotorDatabase:
    try:
        db = database.get_database()
        yield db
    finally:
        await db.client.drop_database("pixhelves_test_db")
        db.client.close()


@pytest.fixture
async def async_client() -> Generator:
    server_api = get_server_api()
    async with AsyncClient(app=app, base_url=f"{server_api}{config.API_V1_STR}") as ac:
        yield ac


@pytest.fixture
async def normal_user_token_headers():
    return await authentication_token_from_email("test@example.com")
