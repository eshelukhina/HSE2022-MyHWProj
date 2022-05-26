from datetime import datetime

from sqlalchemy.orm import Session

from database.src import tables
from database.src.tables import Submition
from web_server.src.models.homework import Homework


def get_submition(id: int, db: Session):
    return db.query(tables.Submition).filter(tables.Submition.id == id).first()


def get_all_submitions(db: Session):
    return db.query(tables.Submition).all()


def get_all_homeworks(db: Session):
    current_time = datetime.utcnow()
    return db.query(tables.Homework).filter(tables.Homework.publish_time <= current_time) \
        .order_by(tables.Homework.deadline).all()


def get_all_submitions_by_homework_id(id: int, db: Session):
    return db.query(tables.Submition).filter(tables.Submition.homework_id == id). \
        order_by(tables.Submition.submition_time).all()


def get_student_homework(id: int, db: Session):
    current_time = datetime.utcnow()
    return db.query(tables.Homework).filter(tables.Homework.publish_time <= current_time) \
        .filter(tables.Homework.id == id).first()


def create_homework(homework: Homework, db: Session):
    db.add(homework)
    db.commit()
    db.refresh(homework)
    return homework


def create_homework_solution(submition: Submition, db: Session):
    submition_to_db = tables.Submition(
        homework_id=submition.homework_id,
        url=submition.url,
        submition_time=datetime.utcnow()
    )
    db.add(submition_to_db)
    db.commit()
    db.refresh(submition_to_db)
    return submition_to_db
