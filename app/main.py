from fastapi import FastAPI


from app.api.api_v1.api import api_router
from app.core import config
from app.db.database import get_database, close_connection

app = FastAPI()


@app.on_event("startup")
def startup():
    get_database()


@app.on_event("shutdown")
def shutdown():
    close_connection()


app.include_router(api_router, prefix=config.API_V1_STR)
