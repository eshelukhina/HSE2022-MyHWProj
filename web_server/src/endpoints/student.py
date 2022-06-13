import http

import fastapi
import starlette.status
from fastapi import APIRouter, Depends, Request
from requests import Session
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from database.src.database import Database
from database.src.tables import Homework
from web_server.src.models.submission import Submission
from web_server.src.services import homeworks_service, submissions_service

student_router = APIRouter(prefix="/student", tags=["Student"])

templates = Jinja2Templates(directory="interface")


@student_router.get('/')
async def student_page(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Страница студента", "body": "student_page"}
    )


@student_router.get('/homeworks/{id}')
async def get_student_homework_by_id(request: Request, id: int, db: Session = Depends(Database.get_db)):
    status_code, content = homeworks_service.get_homework_by_id(id, db)
    if status_code != http.HTTPStatus.OK or type(content) != Homework:
        return JSONResponse(status_code=status_code, content=content)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": f"Страница домашнего задания: {content.name}", "body": "homework", "hw": content}
    )


def check_url(url: str, prefix: str):
    if not url.startswith(prefix):
        return False
    rep = url.replace(prefix, "", 1).strip("/")
    splitted_url = rep.split("/")
    return len(splitted_url) == 2


@student_router.post('/homeworks/{id}')
async def add_homework_solution(id: int, submission: Submission, db: Session = Depends(Database.get_db)):
    if not check_url(submission.url, "https://github.com/"):
        return JSONResponse("Incorrect url", status_code=http.HTTPStatus.BAD_REQUEST)
    status_code, content = submissions_service.add_homework_solution(id, submission, db)
    if status_code != http.HTTPStatus.OK:
        return JSONResponse(status_code=status_code, content=content)
    return fastapi.responses.RedirectResponse("/submissions", status_code=starlette.status.HTTP_302_FOUND)
