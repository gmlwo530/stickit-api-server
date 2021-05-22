from dotenv import load_dotenv

from typing import Generator, Tuple

from httpx import AsyncClient

from starlette.datastructures import UploadFile as StarletteUploadFile

from app.main import app
from app.db import database
from app.core import config
from app.models.user import User
from app.tests.utils.user import create_random_user
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
async def async_client() -> Generator[None, AsyncClient, None]:
    server_api = get_server_api()
    async with AsyncClient(app=app, base_url=f"{server_api}{config.API_V1_STR}") as ac:
        yield ac


aiofiles.threadpool.wrap.register(mock.MagicMock)(
    lambda *args, **kwargs: aiofiles.threadpool.AsyncBufferedIOBase(*args, **kwargs)
)


@pytest.fixture
async def user_and_password() -> Generator[None, Tuple[User, str], None]:
    yield await create_random_user()


@pytest.fixture
def file() -> Generator[None, StarletteUploadFile, None]:
    path = Path(__file__).parent

    with open(
        path.joinpath("utils/images/test.png"), "rb"
    ) as f, SpooledTemporaryFile() as stf:
        content = f.read()
        stf.write(content)
        yield StarletteUploadFile(
            filename=random_lower_string(), file=stf, content_type="image/png"
        )
