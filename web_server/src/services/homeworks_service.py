import http
from typing import List, Tuple, Any

from requests import Session

from database.src import crud
from web_server.src.models.homework import Homework


def get_homework_by_id(id: int, db: Session) -> Tuple[int, Any]:
    homework = crud.get_student_homework(id, db)
    if homework is None:
        return http.HTTPStatus.NOT_FOUND, f"No homework with id: {id}"
    return http.HTTPStatus.OK, homework


def get_all_homeworks(db : Session) -> Tuple[int, List[Homework]]:
    return http.HTTPStatus.OK, crud.get_all_homeworks(db)
