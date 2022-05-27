import http
from typing import Tuple

from requests import Session

from database.src import crud
from web_server.src.models.homework import Homework


def add_homework(homework: Homework, db: Session) -> Tuple[int, int]:
    return http.HTTPStatus.OK, crud.create_homework(homework, db).id
