from sqlalchemy import Column, Integer, String, DateTime

from database.src.database import Model
from web_server.src.models.submition_result import SubmitionResult


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
    submition_time = Column(DateTime)
    result = Column(SubmitionResult)
