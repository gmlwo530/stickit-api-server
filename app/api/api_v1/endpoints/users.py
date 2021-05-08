from fastapi import APIRouter, Depends, HTTPException

from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from app import crud
from app.db.database import get_database
from app.models.user import User, UserCreate, UserInDB
from app.api.utils.security import get_current_active_user
from app.api.utils.exceptions import HTTP_403_FORBIDDEN_USER_ENOUGH_PRIVILEGES

router = APIRouter()


@router.post("/", response_model=User)
async def create_user(
    *,
    user_in: UserCreate,
):
    db = get_database()

    user = await crud.user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
        )

    user = await crud.user.create(db, obj_in=user_in)
    return user


@router.get("/{username}", response_model=User)
async def read_user(
    username: str, current_user: UserInDB = Depends(get_current_active_user)
):
    db = get_database()

    user = await crud.user.get_by_username(db, username=username)
    if user == current_user:
        return user
    if not crud.user.is_superuser:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            deatil=HTTP_403_FORBIDDEN_USER_ENOUGH_PRIVILEGES,
        )

    return user
