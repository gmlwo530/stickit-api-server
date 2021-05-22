from app import crud
from app.main import app
from app.core import config
from app.db.database import get_database
from app.models.user import UserCreate
from app.tests.utils.utils import random_lower_string, get_server_api, random_email

from httpx import AsyncClient


async def user_authentication_headers(username, password):
    server_api = get_server_api()
    async with AsyncClient(app=app, base_url=f"{server_api}{config.API_V1_STR}") as ac:
        data = {"username": username, "password": password}

        r = await ac.post(
            f"{server_api}{config.API_V1_STR}/login/access-token", data=data
        )
        response = r.json()

        auth_token = response["access_token"]
        return {"Authorization": f"Bearer {auth_token}"}


async def create_random_user():
    email = random_email()
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(username=username, email=email, password=password)

    db = get_database()
    user = await crud.user.create(db, obj_in=user_in)
    return user


async def authentication_token_from_username(username, password):
    db = get_database()

    user = await crud.user.get_by_username(db, username=username)
    if not user:
        password = random_lower_string()
        username = random_lower_string()
        email = "f{}@example.com"
        user_in = UserCreate(username=username, email=email, password=password)
        user = crud.user.create(db, obj_in=user_in)

    return await user_authentication_headers(username, password)
