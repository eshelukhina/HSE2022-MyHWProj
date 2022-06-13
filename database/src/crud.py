from datetime import datetime

from sqlalchemy.orm import Session

from database.src import tables
from web_server.src.models.homework import Homework
from web_server.src.models.submission import Submission
from web_server.src.models.submission_result import SubmissionResult


def get_submission(id: int, db: Session):
    return db.query(tables.Submission).filter(tables.Submission.id == id).first()


def get_submission_result(submission_id: int, db: Session):
    return db.query(tables.SubmissionResult).filter(tables.SubmissionResult.submission_id == submission_id).first()


def create_submission_result(result: SubmissionResult, db: Session):
    result_to_db = tables.SubmissionResult(
        submission_id=result.submission_id,
        accepted=result.accepted,
        commentary=result.commentary
    )
    db.add(result_to_db)
    db.commit()
    db.refresh(result_to_db)
    return result_to_db


def get_all_submissions(db: Session):
    return db.query(tables.Submission).order_by(tables.Submission.submission_time).all()


def get_all_homeworks(db: Session):
    current_time = datetime.utcnow()
    return db.query(tables.Homework).filter(tables.Homework.publish_time <= current_time) \
        .order_by(tables.Homework.deadline).all()


def get_student_homework(id: int, db: Session):
    current_time = datetime.utcnow()
    return db.query(tables.Homework).filter(tables.Homework.publish_time <= current_time) \
        .filter(tables.Homework.id == id).first()


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


def create_homework_solution(submission: Submission, db: Session):
    submission_to_db = tables.Submission(
        homework_id=submission.homework_id,
        url=submission.url,
        submission_time=datetime.utcnow()
    )
    db.add(submission_to_db)
    db.commit()
    db.refresh(submission_to_db)
    return submission_to_db
