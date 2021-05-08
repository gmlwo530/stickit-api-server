from app import crud
from app.core import config
from app.db.database import get_database
from app.models.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_lower_string, get_server_api

import requests


def user_authentication_headers(email, password):
    server_api = get_server_api()

    data = {"username": email, "password": password}

    r = requests.post(f"{server_api}{config.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    return {"Authorization": f"Bearer {auth_token}"}


async def create_random_user():
    email = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(username=email, email=email, password=password)

    db = get_database()
    user = await crud.user.create(db, obj_in=user_in)
    return user


async def authentication_token_from_email(email):
    password = random_lower_string()

    db = get_database()

    user = await crud.user.get_by_email(db, email=email)
    if not user:
        user_in = UserCreate(username=email, email=email, password=password)
        user = crud.user.create(db, obj_in=user_in)
    else:
        user_in = UserUpdate(password=password)
        user = crud.user.update(db, obj=user, obj_in=user_in)

    return user_authentication_headers(email, password)
