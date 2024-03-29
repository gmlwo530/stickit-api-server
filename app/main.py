from fastapi import FastAPI
from starlette.responses import JSONResponse

from app.api.api_v1.api import api_router
from app.core import config
from app.db.database import close_connection

from app.backend_pre_start import backend_pre_start


app = FastAPI(title="Pixhelves API Docs", description="Pixhelves API", version="0.0.1")


@app.on_event("startup")
def startup():
    backend_pre_start()


@app.on_event("shutdown")
def shutdown():
    close_connection()


app.include_router(api_router, prefix=config.API_V1_STR)


@app.get("/")
async def get_index():
    return JSONResponse(content={"Hello": "World!"})
