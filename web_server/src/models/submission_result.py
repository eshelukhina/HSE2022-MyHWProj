from pydantic import BaseModel


class SubmissionResult(BaseModel):
    submission_id: int
    accepted: bool
    commentary: str
