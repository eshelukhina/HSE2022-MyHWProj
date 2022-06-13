import datetime
from typing import Union

from pydantic import BaseModel


class Submission(BaseModel):
    id: int
    homework_id: int
    result_id: Union[int, None]
    url: str
    submission_time: datetime.datetime
