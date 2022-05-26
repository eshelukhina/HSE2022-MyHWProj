from pydantic import BaseModel


class SubmitionResult(BaseModel):
    id: int
    accepted: bool
    commentary: str
