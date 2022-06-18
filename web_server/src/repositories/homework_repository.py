from datetime import datetime

from sqlalchemy.orm import Session

from database.src import tables
from web_server.src.models.homework import Homework


class HomeworkRepository:
    @staticmethod
    def create_homework(homework: Homework, db: Session):
        homework_to_db = tables.Homework(
            name=homework.name,
            description=homework.description,
            publish_time=homework.publish_time,
            deadline=homework.deadline,
            checker=homework.checker
        )
        db.add(homework_to_db)
        db.commit()
        db.refresh(homework_to_db)
        return homework_to_db

    @staticmethod
    def get_all_homeworks(db: Session):
        current_time = datetime.now()
        return db.query(tables.Homework).filter(tables.Homework.publish_time <= current_time) \
            .order_by(tables.Homework.deadline).all()

    @staticmethod
    def get_homework(hw_id: int, db: Session):
        current_time = datetime.now()
        return db.query(tables.Homework).filter(tables.Homework.publish_time <= current_time) \
            .filter(tables.Homework.id == hw_id).first()
