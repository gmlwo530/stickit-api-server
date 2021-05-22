from dotenv import load_dotenv

from typing import Generator

from httpx import AsyncClient

from starlette.datastructures import UploadFile as StarletteUploadFile

from app.main import app
from app.db import database
from app.core import config
from app.models.user import User
from app.tests.utils.user import authentication_token_from_username, create_random_user
from app.tests.utils.utils import get_server_api, random_lower_string

from tempfile import SpooledTemporaryFile
from pathlib import Path
from unittest import mock

import pytest
import motor
import aiofiles


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
    return await authentication_token_from_username("test@example.com")


aiofiles.threadpool.wrap.register(mock.MagicMock)(
    lambda *args, **kwargs: aiofiles.threadpool.AsyncBufferedIOBase(*args, **kwargs)
)


@pytest.fixture
async def user() -> User:
    yield await create_random_user()


@pytest.fixture
def file() -> StarletteUploadFile:
    path = Path(__file__).parent

    with open(
        path.joinpath("utils/images/test.png"), "rb"
    ) as f, SpooledTemporaryFile() as stf:
        content = f.read()
        stf.write(content)
        yield StarletteUploadFile(
            filename=random_lower_string(), file=stf, content_type="image/png"
        )
