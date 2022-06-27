import http

import fastapi
import starlette.status
from fastapi import APIRouter, Depends, Request
from requests import Session
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from database.src.database import Database
from runner.src.checker import checker_dict
from web_server.src.models.homework import Homework
from web_server.src.services.teacher_service import TeacherService

teacher_router = APIRouter(prefix="/teacher", tags=["Teacher"])

templates = Jinja2Templates(directory="interface")


@teacher_router.get('/')
async def teacher_page(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Страница преподавателя", "body": "teacher_page"}
    )


@teacher_router.post('/homeworks')
def add_homework(homework: Homework, db: Session = Depends(Database.get_db)):
    if homework.checker not in checker_dict:
        return JSONResponse(
            status_code=http.HTTPStatus.BAD_REQUEST,
            content=f"Checker {homework.checker} is not defined."
        )
    TeacherService.add_homework(homework, db)
    return fastapi.responses.RedirectResponse("/homeworks", status_code=starlette.status.HTTP_302_FOUND)
