from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from src.services import homeworks_service, submitions_service

homework_router = APIRouter(prefix="/homeworks", tags=["Homeworks"])


@homework_router.get('/')
def get_all_homeworks():
    status_code, content = homeworks_service.get_all_homeworks()
    return JSONResponse(status_code=status_code, content=jsonable_encoder(content))


@homework_router.get('/{id}/submitions')
def get_all_submitions_by_homework_id(id: int):
    status_code, content = submitions_service.get_all_submitions_by_homework_id(id)
    return JSONResponse(status_code=status_code, content=jsonable_encoder(content))
