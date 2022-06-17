import http
from typing import List, Tuple, Any

from requests import Session

from web_server.src.models.homework import Homework
from web_server.src.repositories.HomeworkRepository import HomeworkRepository


class HomeworkService:
    @staticmethod
    def get_homework_by_id(hw_id: int, db: Session) -> Tuple[int, Any]:
        homework = HomeworkRepository.get_homework(hw_id, db)
        if homework is None:
            return http.HTTPStatus.NOT_FOUND, f"No homework with id: {hw_id}"
        return http.HTTPStatus.OK, homework

    @staticmethod
    def get_all_homeworks(db: Session) -> Tuple[int, List[Homework]]:
        return http.HTTPStatus.OK, HomeworkRepository.get_all_homeworks(db)
