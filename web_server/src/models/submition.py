import datetime
from typing import Union

from pydantic import BaseModel


class Submition(BaseModel):
    id: int
    homework_id: int
    result_id: Union[int, None]
    url: str
    submition_time: datetime.datetime
