import http
from typing import List, Tuple, Any

from requests import Session

from database.src import crud
from web_server.src.models.submition import Submition


def get_all_submitions(db: Session) -> Tuple[int, List[Submition]]:
    submissions = crud.get_all_submitions(db)
    return http.HTTPStatus.OK, submissions


def get_submition(id: int, db: Session) -> Tuple[int, Any]:
    submission = crud.get_submition(id, db)
    if submission is None:
        return http.HTTPStatus.NOT_FOUND, f"No submission with id: {id}"
    return http.HTTPStatus.OK, submission


def get_all_submitions_by_homework_id(homework_id: int, db: Session) -> Tuple[int, List[Submition]]:
    submissions = crud.get_all_submitions_by_homework_id(homework_id, db)
    return http.HTTPStatus.OK, submissions


def add_homework_solution(homework_id, db: Session) -> Tuple[int, Any]:
    # TODO (return what?)
    check_homework = crud.get_student_homework(homework_id, db)
    if check_homework is None:
        return http.HTTPStatus.NOT_FOUND, f"No homework with id: {id}"
    homework_solution = crud.create_homework_solution(homework_id, db)
    return http.HTTPStatus.OK, homework_solution
