from pydantic import BaseModel


class SubmitionResult(BaseModel):
    accepted: bool
    commentary: str
