from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from starlette.status import HTTP_400_BAD_REQUEST

from app import crud
from app.core import config
from app.core.jwt import create_access_token
from app.db.database import get_database
from app.models.token import Token
from app.api.utils.exceptions import HTTP_400_BAD_REQUEST_INACTIVE_USER


router = APIRouter()


@router.post("/login/access-token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Get an access token for future requests.
    """
    db = get_database()

    user = await crud.user.authenticate(
        db, username=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
        )
    elif not crud.user.is_active(user):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=HTTP_400_BAD_REQUEST_INACTIVE_USER
        )

    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": create_access_token(
            data={"username": user.username}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
