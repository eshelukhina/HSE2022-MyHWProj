from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from requests import Session
from starlette.responses import JSONResponse

from database.src.database import Database
from web_server.src.services import homeworks_service, submitions_service

student_router = APIRouter(prefix="/student", tags=["Student"])


@student_router.get('/homeworks/{id}')
def get_student_homework_by_id(id: int, db: Session = Depends(Database.get_db)):
    status_code, content = homeworks_service.get_homework_by_id(id, db)
    return JSONResponse(status_code=status_code, content=jsonable_encoder(content))


@student_router.post('/homeworks/{id}')
def add_homework_solution(id: int, db: Session = Depends(Database.get_db)):
    status_code, content = submitions_service.add_homework_solution(id, db)
    return JSONResponse(status_code=status_code, content=jsonable_encoder(content))
