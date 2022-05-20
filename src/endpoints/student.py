from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from src.services import submitions_service, homeworks_service

student_router = APIRouter(prefix="/student", tags=["Student"])


@student_router.get('/homeworks/{id}')
def get_student_homework_by_id(id: int):
    status_code, content = homeworks_service.get_homework_by_id(id)
    return JSONResponse(status_code=status_code, content=jsonable_encoder(content))


@student_router.post('/homeworks/{id}')
def add_homework_solution(id: int):
    status_code, content = submitions_service.add_homework_solution(id)
    return JSONResponse(status_code=status_code, content=jsonable_encoder(content))
