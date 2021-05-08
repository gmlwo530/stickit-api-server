# from app.models.user import UserCreate`
from app.tests.utils.utils import random_lower_string

import pytest


@pytest.mark.asyncio
async def test_create_user_by_normal_user(async_client):
    username = random_lower_string()
    password = random_lower_string()
    data = {"username": username, "password": password, "email": "test@example.com"}
    r = await async_client.post("/users/", json=data)
    assert r.status_code == 200
