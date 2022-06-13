import http

from fastapi import APIRouter, Depends
from fastapi import Request
from requests import Session
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from database.src.database import Database
from web_server.src.services import submissions_service

submissions_router = APIRouter(prefix="/submissions", tags=["Submissions"])

templates = Jinja2Templates(directory="interface")


@submissions_router.get('/')
def get_all_submissions(request: Request, db: Session = Depends(Database.get_db)):
    status_code, content = submissions_service.get_all_submissions(db)
    print(content)
    if status_code != http.HTTPStatus.OK:
        return JSONResponse(status_code=status_code, content=content)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Результаты", "body": "submissions", "submissions": content}
    )


@submissions_router.get('/{id}')
def get_submission(request: Request, id: int, db: Session = Depends(Database.get_db)):
    status_code, content = submissions_service.get_submission(id, db)
    if status_code != http.HTTPStatus.OK:
        return JSONResponse(status_code=status_code, content=content)
    submission = content
    status_code, content = submissions_service.get_submission_result(submission.id, db)
    if status_code != http.HTTPStatus.OK:
        return JSONResponse(status_code=status_code, content=content)
    submission_result = content
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": f"Результат посылки: {submission.id}",
            "body": "submission",
            "submission": submission,
            "submission_result": submission_result
        }
    )
