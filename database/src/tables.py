from sqlalchemy import Column, Integer, String, DateTime, Boolean

from database.src.database import Model


class Homeworks(Model):
    __tablename__ = "homeworks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    publish_time = Column(DateTime)
    deadline = Column(DateTime)


class Submition(Model):
    __tablename__ = "submition"

    id = Column(Integer, primary_key=True, index=True)
    homework_id = Column(Integer)
    result_id = Column(Integer)
    submition_time = Column(DateTime)


class SubmitionResult(Model):
    __tablename__ = "submition_result"

    id = Column(Integer, primary_key=True, index=True)
    accepted = Column(Boolean)
    commentary = Column(String)
