import http

import fastapi
import starlette.status
from fastapi import APIRouter, Depends, Request
from requests import Session
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from database.src.database import Database
from web_server.src.models.homework import Homework
from web_server.src.services import teacher_service

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
    status_code, content = teacher_service.add_homework(homework, db)
    if status_code != http.HTTPStatus.OK:
        return JSONResponse(status_code=status_code, content=content)
    return fastapi.responses.RedirectResponse("/homeworks", status_code=starlette.status.HTTP_302_FOUND)
