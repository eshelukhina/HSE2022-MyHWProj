import http
from typing import Tuple, Any

from requests import Session

from database.src import crud
from web_server.src.models.homework import Homework


def add_homework(homework: Homework, db : Session) -> Tuple[int, Any]:
    # TODO (return what?)
    homework_id = homework.id
    check_homework = crud.get_student_homework(homework_id, db)
    if check_homework is not None:
        return http.HTTPStatus.CONFLICT, f"Homework with id: {homework_id} already exists"
    return http.HTTPStatus.OK, crud.create_homework(homework, db)
