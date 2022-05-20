import datetime

from pydantic import BaseModel


class Homework(BaseModel):
    id: int
    name: str
    description: str
    publish_time: datetime.datetime
    deadline: datetime.datetime
