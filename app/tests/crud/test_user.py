from fastapi.encoders import jsonable_encoder

from app import crud
from app.models.user import UserCreate
from app.tests.utils.utils import random_email, random_lower_string

import pytest


@pytest.mark.asyncio
async def test_create_user(db) -> None:
    email = random_email()
    name = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=email, username=name, password=password)
    user = await crud.user.create(db, obj_in=user_in)
    assert user.email == email


@pytest.mark.asyncio
async def test_get_user(db) -> None:
    password = random_lower_string()
    username = random_email()
    name = random_lower_string()
    user_in = UserCreate(email=username, username=name, password=password)
    user = await crud.user.create(db, obj_in=user_in)
    user_2 = await crud.user.get(db, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)
