from fastapi import APIRouter

from app.api.api_v1.endpoints import users, login, collects

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(collects.router, prefix="/collects", tags=["collect"])
