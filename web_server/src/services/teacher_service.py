import http
from typing import Tuple, Union

from requests import Session

from database.src import crud
from runner.src.checker import checker_dict
from web_server.src.models.homework import Homework


def add_homework(homework: Homework, db: Session) -> Tuple[int, Union[str, int]]:
    if homework.checker not in checker_dict:
        return http.HTTPStatus.BAD_REQUEST, f"Checker {homework.checker} is not defined."
    return http.HTTPStatus.OK, crud.create_homework(homework, db).id
