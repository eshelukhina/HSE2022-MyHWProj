from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from src.services import submitions_service

submitions_router = APIRouter(prefix="/submitions", tags=["Submitions"])


@submitions_router.get('/')
def get_all_submitions():
    status_code, content = submitions_service.get_all_submitions()
    return JSONResponse(status_code=status_code, content=jsonable_encoder(content))


@submitions_router.get('/{id}')
def get_submition(id: int):
    status_code, content = submitions_service.get_submition(id)
    return JSONResponse(status_code=status_code, content=jsonable_encoder(content))
