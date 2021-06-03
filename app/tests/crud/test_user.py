from fastapi.encoders import jsonable_encoder

from app import crud
from app.core.security import get_password_hash
from app.models.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string

import pytest


@pytest.mark.asyncio
async def test_get_user(db) -> None:
    password = random_lower_string()
    email = random_email()
    username = random_lower_string()
    user_in = UserCreate(email=email, username=username, password=password)
    user = await crud.user.create(db, obj_in=user_in)
    user_2 = await crud.user.get(db, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


@pytest.mark.asyncio
async def test_create_user(db) -> None:
    email = random_email()
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=email, username=username, password=password)
    user = await crud.user.create(db, obj_in=user_in)
    assert user.email == email


@pytest.mark.asyncio
async def test_update_user(db) -> None:
    password = random_lower_string()
    email = random_email()
    username = random_lower_string()
    user_in = UserCreate(email=email, username=username, password=password)
    user = await crud.user.create(db, obj_in=user_in)

    updated_email = random_email()
    user_in = UserUpdate(email=updated_email)
    updated_user = await crud.user.update(db, obj=user, obj_in=user_in)
    assert updated_email == updated_user.email

    updated_username = random_lower_string()
    user_in = UserUpdate(username=updated_username)
    updated_user = await crud.user.update(db, obj=user, obj_in=user_in)
    assert updated_username == updated_user.username

    updated_password = random_lower_string()
    user_in = UserUpdate(password=updated_password)
    updated_user = await crud.user.update(db, obj=user, obj_in=user_in)

    authenticated_user = await crud.user.authenticate(
        db, username=updated_user.username, password=updated_password
    )
    assert authenticated_user
