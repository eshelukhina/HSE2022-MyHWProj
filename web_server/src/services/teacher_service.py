import http
from typing import Tuple, Union

from requests import Session

from runner.src.checker import checker_dict
from web_server.src.models.homework import Homework
from web_server.src.repositories.HomeworkRepository import HomeworkRepository


class TeacherService:
    @staticmethod
    def add_homework(homework: Homework, db: Session) -> Tuple[int, Union[str, int]]:
        if homework.checker not in checker_dict:
            return http.HTTPStatus.BAD_REQUEST, f"Checker {homework.checker} is not defined."
        return http.HTTPStatus.OK, HomeworkRepository.create_homework(homework, db).id
