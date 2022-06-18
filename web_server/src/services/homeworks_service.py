from typing import List, Optional

from requests import Session

from web_server.src.models.homework import Homework
from web_server.src.repositories.homework_repository import HomeworkRepository


class HomeworkService:
    @staticmethod
    def get_homework_by_id(hw_id: int, db: Session) -> Optional[Homework]:
        return HomeworkRepository.get_homework(hw_id, db)

    @staticmethod
    def get_all_homeworks(db: Session) -> List[Homework]:
        return HomeworkRepository.get_all_homeworks(db)
