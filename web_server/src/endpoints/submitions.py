import http

from fastapi import APIRouter, Depends
from fastapi import Request
from requests import Session
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from database.src.database import Database
from web_server.src.services import submitions_service

submitions_router = APIRouter(prefix="/submitions", tags=["Submitions"])

templates = Jinja2Templates(directory="interface")


@submitions_router.get('/')
def get_all_submitions(request: Request, db: Session = Depends(Database.get_db)):
    status_code, content = submitions_service.get_all_submitions(db)
    if status_code != http.HTTPStatus.OK:
        return JSONResponse(status_code=status_code, content=content)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Результаты", "body": "submitions", "submitions": content}
    )


@submitions_router.get('/{id}')
def get_submition(request: Request, id: int, db: Session = Depends(Database.get_db)):
    status_code, content = submitions_service.get_submition(id, db)
    if status_code != http.HTTPStatus.OK:
        return JSONResponse(status_code=status_code, content=content)
    submition = content
    status_code, content = submitions_service.get_submition_result(submition.result_id, db)
    if status_code != http.HTTPStatus.OK:
        return JSONResponse(status_code=status_code, content=content)
    submition_result = content
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": f"Результат посылки: {submition.id}",
            "body": "submition",
            "submition": submition,
            "submition_result": submition_result
        }
    )
