from fastapi import APIRouter, Depends, status, File, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Form
from fastapi.responses import JSONResponse

from app import crud
from app.crud.base import DESC
from app.db.database import get_database
from app.models.user import UserInDB
from app.models.collect import Collect, CollectCreate, CollectUpdate
from app.api.utils.exceptions import (
    HTTP_403_FORBIDDEN_USER_PERMISSION,
    HTTP_404_NOT_FOUND_DETAIL,
)
from app.api.utils.security import get_current_active_user

from typing import List, Optional

router = APIRouter()


@router.get("/{id}", response_model=Collect)
async def read_collect(
    *, id: str, current_user: UserInDB = Depends(get_current_active_user)
):
    db = get_database()
    collect = await crud.collect.get(db, id)

    if collect is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=HTTP_404_NOT_FOUND_DETAIL.format("Collect"),
        )

    if collect.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=HTTP_403_FORBIDDEN_USER_PERMISSION,
        )

    return collect


@router.get("/", response_model=List[Collect])
async def read_collects(
    *, page: int = 0, current_user: UserInDB = Depends(get_current_active_user)
):
    return await crud.collect.get_many(
        get_database(),
        filter={"user_id": str(current_user.id)},
        sort=[("_id", DESC)],
        page=page,
    )


@router.post("/", response_model=Collect, status_code=status.HTTP_201_CREATED)
async def create_collect(
    *,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user: UserInDB = Depends(get_current_active_user)
):
    db = get_database()
    collect_in = CollectCreate(
        user_id=current_user.id, name=name, description=description, file=file
    )

    collect = await crud.collect.create(db, obj_in=collect_in)

    return collect


@router.put("/{id}", response_model=Collect, status_code=status.HTTP_201_CREATED)
async def update_collect(
    *,
    id: str,
    name: str = Form(None),
    description: str = Form(None),
    file: UploadFile = File(None),
    current_user: UserInDB = Depends(get_current_active_user)
):
    db = get_database()

    collect = await crud.collect.get(db, id)

    if collect is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=HTTP_404_NOT_FOUND_DETAIL.format("Collect"),
        )

    if collect.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=HTTP_403_FORBIDDEN_USER_PERMISSION,
        )

    collect_in = CollectUpdate(
        user_id=current_user.id, name=name, description=description, file=file
    )

    updated_collect = await crud.collect.update(db, obj=collect, obj_in=collect_in)

    return updated_collect


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collect(
    *, id: str, current_user: UserInDB = Depends(get_current_active_user)
):
    db = get_database()

    collect = await crud.collect.get(db, id)

    if collect is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=HTTP_404_NOT_FOUND_DETAIL.format("Collect"),
        )

    if collect.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=HTTP_403_FORBIDDEN_USER_PERMISSION,
        )

    await crud.collect.delete(db, obj=collect)

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
