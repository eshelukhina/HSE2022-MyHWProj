from datetime import datetime

from fastapi import Depends
from sqlalchemy.orm import Session

from database.src import tables
from database.src.database import Database
from web_server.src.models.homework import Homework


def get_submition(id: int, db: Session):
    return db.query(tables.Submition).filter(tables.Submition.id == id).first()


def get_all_submitions(db: Session):
    return db.query(tables.Submition).all()


def get_all_homeworks(db: Session):
    current_time = datetime.utcnow()
    return db.query(tables.Homeworks).filter(tables.Homeworks.publish_time >= current_time) \
        .order_by(tables.Homeworks.deadline).all()


def get_all_submitions_by_homework_id(id: int, db: Session):
    return db.query(tables.Submition).filter(tables.Submition.homework_id == id). \
        order_by(tables.Submition.submition_time).all()


def get_student_homework(id: int, db: Session):
    current_time = datetime.utcnow()
    return db.query(tables.Homeworks).filter(tables.Homeworks.publish_time >= current_time) \
        .filter(tables.Homeworks.id == id).first()


def create_homework(homework: Homework, db: Session):
    db.add(homework)
    db.commit()
    db.refresh(homework)
    return homework


def create_homework_solution(id: int, db: Session):
    # TODO
    pass
