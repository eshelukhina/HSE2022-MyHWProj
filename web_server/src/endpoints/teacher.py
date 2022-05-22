from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from requests import Session
from starlette.responses import JSONResponse

from database.src.database import Database
from web_server.src.models.homework import Homework
from web_server.src.services import teacher_service

teacher_router = APIRouter(prefix="/teacher", tags=["Teacher"])


@teacher_router.post('/homeworks')
def add_homework(homework: Homework, db: Session = Depends(Database.get_db)):
    status_code, content = teacher_service.add_homework(homework, db)
    return JSONResponse(status_code=status_code, content=jsonable_encoder(content))
