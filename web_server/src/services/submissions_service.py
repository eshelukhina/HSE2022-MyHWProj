import os
from typing import List, Tuple, Union, Optional

import pika
from requests import Session

from database.src import tables
from runner.src.checker import CheckerInfo
from web_server.src.models.homework import Homework
from web_server.src.models.submission import Submission
from web_server.src.repositories.submission_repository import SubmissionRepository


class SubmissionService:
    @staticmethod
    def get_all_submissions(db: Session) -> List[tables.Submission]:
        return SubmissionRepository.get_all_submissions(db)

    @staticmethod
    def get_submission(submission_id: int, db: Session) -> tables.Submission:
        return SubmissionRepository.get_submission(submission_id, db)

    @staticmethod
    def get_submission_result(submission_id: int, db: Session) -> Tuple[int, Union[str, tables.SubmissionResult]]:
        return SubmissionRepository.get_submission_result(submission_id, db)

    @staticmethod
    def add_check_info_to_message_broker(check_info: CheckerInfo) -> None:
        amqp_host = "localhost" if os.environ.get('AMQP_HOST') is None else os.environ.get('AMQP_HOST')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=amqp_host))
        channel = connection.channel()
        channel.queue_declare("tasks")
        body = check_info.json().encode("utf-8")
        channel.basic_publish(exchange="", routing_key="tasks", body=body)
        connection.close()

    @staticmethod
    def add_submission(homework: Homework,
                       submission: Submission,
                       db: Session) -> Optional[int]:
        submission.homework_id = homework.id
        submission.id = SubmissionRepository.create_submission(submission, db).id
        check_info_to_message_broker = CheckerInfo(
            homework_id=homework.id,
            homework_description=homework.description,
            homework_publish_time=homework.publish_time,
            homework_deadline=homework.deadline,
            homework_checker=homework.checker,
            submission=submission
        )
        SubmissionService.add_check_info_to_message_broker(check_info_to_message_broker)
        return submission.id
