from typing import Tuple

from httpx import AsyncClient

from app.models.user import User
from app.tests.utils.utils import random_email, random_lower_string
from app.tests.utils.user import authentication_token_from_username

import pytest


@pytest.mark.asyncio
async def test_create_user_by_normal_user(async_client: AsyncClient):
    username = random_lower_string()
    password = random_lower_string()
    data = {"username": username, "password": password, "email": "test@example.com"}
    r = await async_client.post("/users/", json=data)
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_read_user(async_client: AsyncClient):
    username = random_lower_string()
    email = f"{username}@example.com"
    password = random_lower_string()
    data = {"username": username, "password": password, "email": email}
    r = await async_client.post("/users/", json=data)
    assert r.status_code == 200

    token = await authentication_token_from_username(username, password)

    r = await async_client.get(f"/users/{username}/", headers=token)
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_update_user(
    async_client: AsyncClient, user_and_password: Tuple[User, str]
):
    updated_username = random_lower_string()
    updated_password = random_lower_string()
    updated_email = random_email()

    user = user_and_password[0]
    password = user_and_password[1]

    token = await authentication_token_from_username(user.username, password)

    r = await async_client.put(
        f"/users/{user.username}", json={"email": updated_email}, headers=token
    )
    assert r.status_code == 200
    assert r.json()["email"] == updated_email

    r = await async_client.put(
        f"/users/{user.username}", json={"username": updated_username}, headers=token
    )
    assert r.status_code == 200
    assert r.json()["username"] == updated_username

    r = await async_client.get(f"/users/{updated_username}", headers=token)
    assert r.status_code == 404

    new_token = await authentication_token_from_username(updated_username, password)

    r = await async_client.put(
        f"/users/{updated_username}",
        json={"password": updated_password},
        headers=new_token,
    )
    assert r.status_code == 200
