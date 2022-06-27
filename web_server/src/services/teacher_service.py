from requests import Session

from web_server.src.models.homework import Homework
from web_server.src.repositories.homework_repository import HomeworkRepository


class TeacherService:
    @staticmethod
    def add_homework(homework: Homework, db: Session) -> Homework:
        return HomeworkRepository.create_homework(homework, db)
