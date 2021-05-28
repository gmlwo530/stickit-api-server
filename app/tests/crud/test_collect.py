from fastapi.encoders import jsonable_encoder
from starlette.datastructures import UploadFile as StarletteUploadFile

from app import crud
from app.crud.base import DESC
from app.models.user import User
from app.models.collect import CollectCreate, CollectUpdate
from app.tests.utils.utils import random_lower_string

from typing import Tuple

import pytest


@pytest.mark.asyncio
async def test_create_collect(
    db, user_and_password: Tuple[User, str], file: StarletteUploadFile
) -> None:
    name = random_lower_string()
    user = user_and_password[0]
    collect_in = CollectCreate(name=name, file=file, user_id=str(user.id))
    collect = await crud.collect.create(db, obj_in=collect_in)
    assert collect.name == name


@pytest.mark.asyncio
async def test_get_collect(
    db, user_and_password: Tuple[User, str], file: StarletteUploadFile
) -> None:
    user = user_and_password[0]
    name = random_lower_string()
    description = random_lower_string()
    collect_in = CollectCreate(
        name=name, description=description, user_id=str(user.id), file=file
    )
    collect = await crud.collect.create(db, obj_in=collect_in)
    collect2 = await crud.collect.get(db, id=collect.id)
    assert collect2
    assert collect.name == collect2.name
    assert jsonable_encoder(collect) == jsonable_encoder(collect2)


@pytest.mark.asyncio
async def test_get_collects(
    db, user_and_password: Tuple[User, str], file: StarletteUploadFile
) -> None:
    user = user_and_password[0]
    expect_result = []

    for _ in range(12):
        name = random_lower_string()
        description = random_lower_string()
        collect_in = CollectCreate(
            name=name, description=description, user_id=str(user.id), file=file
        )
        collect = await crud.collect.create(db, obj_in=collect_in)
        expect_result.insert(0, collect)

    collects = await crud.collect.get_many(
        db, filter={"user_id": str(user.id)}, sort=[("_id", DESC)]
    )

    assert len(collects) == 10
    assert expect_result[:10] == collects

    collects = await crud.collect.get_many(
        db, filter={"user_id": str(user.id)}, sort=[("_id", DESC)], page=1
    )

    assert len(collects) == 2
    assert expect_result[10:] == collects


@pytest.mark.asyncio
async def test_update_collect(
    db, user_and_password: Tuple[User, str], file: StarletteUploadFile
) -> None:
    user = user_and_password[0]
    old_name = random_lower_string()
    collect_in = CollectCreate(name=old_name, user_id=str(user.id), file=file)
    collect = await crud.collect.create(db, obj_in=collect_in)
    assert collect.name == old_name

    new_name = random_lower_string()
    collect_in = CollectUpdate(name=new_name)
    collect = await crud.collect.update(db, obj=collect, obj_in=collect_in)
    assert collect.name == new_name

    old_file_path = collect.file
    collect_in = CollectUpdate(file=file)
    collect = await crud.collect.update(db, obj=collect, obj_in=collect_in)
    assert not old_file_path.exists()

    description = random_lower_string()
    collect_in = CollectUpdate(description=description)
    collect = await crud.collect.update(db, obj=collect, obj_in=collect_in)
    assert collect.description == description


@pytest.mark.asyncio
async def test_delete_collect(
    db, user_and_password: Tuple[User, str], file: StarletteUploadFile
) -> None:
    user = user_and_password[0]
    name = random_lower_string()
    description = random_lower_string()
    collect_in = CollectCreate(
        name=name, description=description, user_id=str(user.id), file=file
    )
    collect = await crud.collect.create(db, obj_in=collect_in)

    deleted_collect = await crud.collect.delete(db, obj=collect)

    none_collect = await crud.collect.get(db, id=deleted_collect.id)
    assert none_collect is None
