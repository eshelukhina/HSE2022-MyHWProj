import http

from fastapi import APIRouter, Depends
from fastapi import Request
from requests import Session
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from database.src.database import Database
from web_server.src.models.submission_result import SubmissionResult
from web_server.src.services.submissions_service import SubmissionService

submissions_router = APIRouter(prefix="/submissions", tags=["Submissions"])

templates = Jinja2Templates(directory="interface")


@submissions_router.get('/')
def get_all_submissions(request: Request, db: Session = Depends(Database.get_db)):
    submissions = SubmissionService.get_all_submissions(db)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Результаты", "body": "submissions", "submissions": submissions}
    )


@submissions_router.get('/{id}')
def get_submission(request: Request, id: int, db: Session = Depends(Database.get_db)):
    submission = SubmissionService.get_submission(id, db)
    if submission is None:
        return JSONResponse(status_code=http.HTTPStatus.NOT_FOUND, content=f"No submission with id: {id}")
    submission_result = SubmissionService.get_submission_result(submission.id, db)
    if submission_result is None:
        submission_result = SubmissionResult(accepted=False, commentary="Submission not yet tested")
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
