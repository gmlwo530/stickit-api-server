# from app.models.user import UserCreate`
from app.tests.utils.utils import random_lower_string
from app.tests.utils.user import authentication_token_from_username

import pytest


@pytest.mark.asyncio
async def test_create_user_by_normal_user(async_client):
    username = random_lower_string()
    password = random_lower_string()
    data = {"username": username, "password": password, "email": "test@example.com"}
    r = await async_client.post("/users/", json=data)
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_read_user(async_client):
    username = random_lower_string()
    email = f"{username}@example.com"
    password = random_lower_string()
    data = {"username": username, "password": password, "email": email}
    r = await async_client.post("/users/", json=data)
    assert r.status_code == 200

    token = await authentication_token_from_username(username, password)

    r = await async_client.get(f"/users/{username}/", headers=token)
    assert r.status_code == 200
