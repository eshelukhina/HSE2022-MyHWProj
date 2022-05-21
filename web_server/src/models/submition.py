import datetime

from pydantic import BaseModel

from web_server.src.models.submition_result import SubmitionResult


class Submition(BaseModel):
    id: int
    homework_id: int
    submition_time: datetime.datetime
    result_id: SubmitionResult
