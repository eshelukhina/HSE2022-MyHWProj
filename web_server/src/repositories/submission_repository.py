from datetime import datetime

from sqlalchemy.orm import Session

from database.src import tables
from web_server.src.models.submission import Submission
from web_server.src.models.submission_result import SubmissionResult


class SubmissionRepository:
    @staticmethod
    def create_submission(submission: Submission, db: Session):
        submission_to_db = tables.Submission(
            homework_id=submission.homework_id,
            url=submission.url,
            submission_time=datetime.now()
        )
        db.add(submission_to_db)
        db.commit()
        db.refresh(submission_to_db)
        return submission_to_db

    @staticmethod
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

    @staticmethod
    def get_submission(submission_id: int, db: Session):
        return db.query(tables.Submission).filter(tables.Submission.id == submission_id).first()

    @staticmethod
    def get_submission_result(submission_id: int, db: Session):
        return db.query(tables.SubmissionResult).filter(tables.SubmissionResult.submission_id == submission_id).first()

    @staticmethod
    def get_all_submissions(db: Session):
        return db.query(tables.Submission).order_by(tables.Submission.submission_time).all()
