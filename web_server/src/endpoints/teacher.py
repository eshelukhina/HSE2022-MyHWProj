from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from web_server.src.models.homework import Homework
from web_server.src.services import teacher_service

teacher_router = APIRouter(prefix="/teacher", tags=["Teacher"])


@teacher_router.post('/homeworks')
def add_homework(homework: Homework):
    status_code, content = teacher_service.add_homework(homework)
    return JSONResponse(status_code=status_code, content=jsonable_encoder(content))
