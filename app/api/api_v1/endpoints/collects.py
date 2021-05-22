from app.db.database import get_database
from fastapi import APIRouter, Depends, status, File, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Form

from app import crud
from app.models.user import UserInDB
from app.models.collect import Collect, CollectCreate
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
async def read_collects(*, skip: int = 0, limit: int = 50):
    pass


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


@router.put("/{id}", response_model=Collect)
async def update_collect(
    *,
    name: str = Form(None),
    description: str = Form(None),
    file: UploadFile = File(None)
):
    pass


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collect(*, id: str):
    pass
