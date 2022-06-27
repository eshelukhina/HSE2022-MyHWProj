from typing import List

from fastapi import APIRouter, Depends, Request
from requests import Session
from starlette.templating import Jinja2Templates

from database.src.database import Database
from web_server.src.models.homework import Homework
from web_server.src.services.homeworks_service import HomeworkService

homework_router = APIRouter(prefix="/homeworks", tags=["Homeworks"])

templates = Jinja2Templates(directory="interface")


@homework_router.get('/')
def get_all_homeworks(request: Request, db: Session = Depends(Database.get_db)):
    homeworks: List[Homework] = HomeworkService.get_all_homeworks(db)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Домашние задания", "body": "homeworks", "homeworks": homeworks}
    )
