from http import HTTPStatus

import fastapi
import starlette.status
from fastapi import APIRouter, Depends, Request
from requests import Session
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from database.src.database import Database
from web_server.src.models.submission import Submission
from web_server.src.services.homeworks_service import HomeworkService
from web_server.src.services.submissions_service import SubmissionService

student_router = APIRouter(prefix="/student", tags=["Student"])

templates = Jinja2Templates(directory="interface")


@student_router.get('/')
async def student_page(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Страница студента", "body": "student_page"}
    )


@student_router.get('/homeworks/{hw_id}')
async def get_student_homework_by_id(request: Request, hw_id: int, db: Session = Depends(Database.get_db)):
    homework = HomeworkService.get_homework_by_id(hw_id, db)
    if homework is None:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content=f"No homework with id: {hw_id}"
        )
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": f"Страница домашнего задания: {homework.name}", "body": "homework",
         "hw": homework}
    )


def check_url(url: str, prefix: str):
    if not url.startswith(prefix):
        return False
    rep = url.replace(prefix, "", 1).strip("/")
    splitted_url = rep.split("/")
    return len(splitted_url) == 2


@student_router.post('/homeworks/{hw_id}')
async def add_homework_solution(hw_id: int, submission: Submission, db: Session = Depends(Database.get_db)):
    if not check_url(submission.url, "https://github.com/"):
        return JSONResponse("Incorrect url", status_code=HTTPStatus.BAD_REQUEST)
    homework = HomeworkService.get_homework_by_id(hw_id, db)
    if homework is None:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content=f"homework with id {hw_id} is not found")
    SubmissionService.add_submission(homework, submission, db)
    return fastapi.responses.RedirectResponse("/submissions", status_code=starlette.status.HTTP_302_FOUND)
