from fastapi.encoders import jsonable_encoder
from starlette.datastructures import UploadFile as StarletteUploadFile
from httpx import AsyncClient

from app import crud
from app.models.user import User
from app.models.collect import Collect, CollectCreate
from app.tests.utils.utils import random_lower_string
from app.tests.utils.user import authentication_token_from_username, create_random_user

from typing import Tuple

import pytest


async def _create_collect(db, user, file) -> Collect:
    collect_in = CollectCreate(user_id=user.id, name=random_lower_string(), file=file)
    return await crud.collect.create(db, obj_in=collect_in)


@pytest.mark.asyncio
async def test_read_collect(
    async_client: AsyncClient,
    db,
    file: StarletteUploadFile,
    user_and_password: Tuple[User, str],
):
    user = user_and_password[0]
    password = user_and_password[1]
    auth_token = await authentication_token_from_username(user.username, password)
    collect = await _create_collect(db, user, file)

    res = await async_client.get(f"/collects/{collect.id}")
    assert res.status_code == 401

    res = await async_client.get(f"/collects/{collect.id}", headers=auth_token)
    assert res.status_code == 200
    assert res.json() == jsonable_encoder(collect)

    res = await async_client.get(
        f"/collects/{random_lower_string()}", headers=auth_token
    )
    assert res.status_code == 404

    no_owner_password = random_lower_string()
    no_owner, _ = await create_random_user(password=no_owner_password)
    no_owner_auth_token = await authentication_token_from_username(
        no_owner.username, no_owner_password
    )
    res = await async_client.get(f"/collects/{collect.id}", headers=no_owner_auth_token)
    assert res.status_code == 403


@pytest.mark.asyncio
async def test_read_collects(
    async_client, db, file: StarletteUploadFile, user_and_password: Tuple[User, str]
):
    # user = user_and_password[0]
    # password = user_and_password[1]
    # auth_token = await authentication_token_from_username(user.username, password)
    # collect = await _create_collect(db, user, file)
    pass

@pytest.mark.asyncio
async def test_create_collect(async_client, file: StarletteUploadFile, user_and_password: Tuple[User, str],):
    url = "/collects"
    user = user_and_password[0]
    password = user_and_password[1]
    auth_token = await authentication_token_from_username(user.username, password)

    res = await async_client.post(url)
    assert res.status_code == 401

    files = {
        "file": (
            file.filename,
            file.file,
            file.content_type,
        )
    }

    # Content-Type은 자동으로 multipart/form-data로 세팅된다. 명시하면 오류가 났다.(아마 boundary 이슈이지 않을까)
    res = await async_client.post(
        url,
        data={"name": random_lower_string()},
        files=files,
        headers=auth_token,
    )
    assert res.status_code == 201


@pytest.mark.asyncio
async def test_update_collect(
    async_client: AsyncClient,
    db, 
    file: StarletteUploadFile,
    user_and_password: Tuple[User, str],
):
    url = "/collects"
    user = user_and_password[0]
    password = user_and_password[1]
    auth_token = await authentication_token_from_username(user.username, password)
    collect = await _create_collect(db, user, file)

    updated_name = random_lower_string()
    res = await async_client.put(f"{url}/{collect.id}", data={"name": updated_name}, headers=auth_token)
    assert res.status_code == 201
    assert res.json()["name"] == updated_name
    updated_collect = await crud.collect.get(db, collect.id)
    assert res.json() == jsonable_encoder(updated_collect)


    updated_desc = random_lower_string()
    res = await async_client.put(f"{url}/{collect.id}", data={"description": updated_desc}, headers=auth_token)
    assert res.status_code == 201
    assert res.json()["description"] == updated_desc
    updated_collect = await crud.collect.get(db, collect.id)
    assert res.json() == jsonable_encoder(updated_collect)


    files = {
        "file": (
            file.filename,
            file.file,
            file.content_type,
        )
    }

    res = await async_client.put(f"{url}/{collect.id}", files=files, headers=auth_token)
    assert res.status_code == 201
    updated_collect = await crud.collect.get(db, collect.id)
    assert res.json() == jsonable_encoder(updated_collect)


@pytest.mark.asyncio
async def test_delete_collect(async_client):
    pass
