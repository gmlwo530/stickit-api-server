from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer

from jwt import PyJWKError

from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
)

from app import crud
from app.core import config
from app.core.jwt import ALGORITHM
from app.db.database import get_database
from app.api.utils.exceptions import (
    HTTP_403_FORBIDDEN_DETAIL,
    HTTP_404_NOT_FOUND_DETAIL,
    HTTP_400_BAD_REQUEST_INACTIVE_USER,
    HTTP_403_FORBIDDEN_USER_ENOUGH_PRIVILEGES,
)
from app.models.token import TokenPayload
from app.models.user import UserInDB

import jwt

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")


async def get_current_user(token: str = Security(reusable_oauth2)):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWKError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail=HTTP_403_FORBIDDEN_DETAIL
        )

    db = get_database()
    user = await crud.user.get_by_username(db, username=token_data.username)

    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=HTTP_404_NOT_FOUND_DETAIL.format("User"),
        )
    return user


def get_current_active_user(current_user: UserInDB = Security(get_current_user)):
    if not crud.user.is_active(current_user):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=HTTP_400_BAD_REQUEST_INACTIVE_USER
        )
    return current_user


def get_current_active_superuser(current_user: UserInDB = Security(get_current_user)):
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=HTTP_403_FORBIDDEN_USER_ENOUGH_PRIVILEGES,
        )
    return current_user
