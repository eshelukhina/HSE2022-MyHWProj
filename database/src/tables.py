from sqlalchemy import Column, Integer, String, DateTime, Boolean

from database.src.database import Model


class Homework(Model):
    __tablename__ = "homeworks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    publish_time = Column(DateTime)
    deadline = Column(DateTime)
    checker = Column(String)


class Submission(Model):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    homework_id = Column(Integer)
    url = Column(String)
    submission_time = Column(DateTime)


class SubmissionResult(Model):
    __tablename__ = "submission_results"

    submission_id = Column(Integer, primary_key=True, index=True)
    accepted = Column(Boolean)
    commentary = Column(String)
