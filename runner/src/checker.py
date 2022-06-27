import datetime

from pydantic import BaseModel

from web_server.src.models.submission import Submission
from web_server.src.models.submission_result import SubmissionResult


class CheckerInfo(BaseModel):
    homework_id: int
    homework_description: str
    homework_publish_time: datetime.datetime
    homework_deadline: datetime.datetime
    homework_checker: str
    submission: Submission


class Checker:
    def check(self, info: CheckerInfo) -> SubmissionResult:
        pass


class GradleTestChecker(Checker):
    def check(self, info: CheckerInfo) -> SubmissionResult:
        return SubmissionResult(submission_id=info.submission.id, accepted=True, commentary="Nice work")


checker_dict = {
    'gradle_test': GradleTestChecker()
}
