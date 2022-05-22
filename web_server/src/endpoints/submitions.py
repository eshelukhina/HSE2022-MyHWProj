from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from requests import Session
from starlette.responses import JSONResponse

from database.src.database import Database
from web_server.src.services import submitions_service

submitions_router = APIRouter(prefix="/submitions", tags=["Submitions"])


@submitions_router.get('/')
def get_all_submitions(db: Session = Depends(Database.get_db)):
    status_code, content = submitions_service.get_all_submitions(db)
    return JSONResponse(status_code=status_code, content=jsonable_encoder(content))


@submitions_router.get('/{id}')
def get_submition(id: int,db: Session = Depends(Database.get_db)):
    status_code, content = submitions_service.get_submition(id, db)
    return JSONResponse(status_code=status_code, content=jsonable_encoder(content))
