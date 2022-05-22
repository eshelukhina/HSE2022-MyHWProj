from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from requests import Session
from starlette.responses import JSONResponse
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from database.src.database import Database
from web_server.src.services import homeworks_service, submitions_service

homework_router = APIRouter(prefix="/homeworks", tags=["Homeworks"])
templates = Jinja2Templates(directory="interface")


@homework_router.get('/', response_class=HTMLResponse)
def get_all_homeworks(request: Request, db: Session = Depends(Database.get_db)):
    status_code, content = homeworks_service.get_all_homeworks(db)
    return JSONResponse(status_code=status_code, content=jsonable_encoder(content))


@homework_router.get('/{id}/submitions', response_class=HTMLResponse)
def get_all_submitions_by_homework_id(request: Request, id: int, db: Session = Depends(Database.get_db)):
    status_code, content = submitions_service.get_all_submitions_by_homework_id(id, db)
    # return JSONResponse(status_code=status_code, content=jsonable_encoder(content))
    return templates.TemplateResponse("index.html", {"request": request, "id": id})
