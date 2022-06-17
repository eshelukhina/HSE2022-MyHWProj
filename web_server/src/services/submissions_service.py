import http
import os
from typing import List, Tuple, Union

import pika
from requests import Session

from database.src import tables
from database.src.tables import SubmissionResult
from runner.src.checker import CheckerInfo
from web_server.src.repositories.HomeworkRepository import HomeworkRepository
from web_server.src.repositories.SubmissionRepository import SubmissionRepository
from web_server.src import models
from web_server.src.models.submission import Submission


class SubmissionService:
    @staticmethod
    def get_all_submissions(db: Session) -> Tuple[int, List[tables.Submission]]:
        submissions = SubmissionRepository.get_all_submissions(db)
        return http.HTTPStatus.OK, submissions

    @staticmethod
    def get_submission(submission_id: int, db: Session) -> Tuple[int, Union[str, tables.Submission]]:
        submission = SubmissionRepository.get_submission(submission_id, db)
        if submission is None:
            return http.HTTPStatus.NOT_FOUND, f"No submission with id: {submission_id}"
        return http.HTTPStatus.OK, submission

    @staticmethod
    def get_submission_result(submission_id: int, db: Session) -> Tuple[int, Union[str, tables.SubmissionResult]]:
        submission_result = SubmissionRepository.get_submission_result(submission_id, db)
        if submission_result is None:
            return http.HTTPStatus.OK, SubmissionResult(accepted=False, commentary="Submission not yet tested")
        return http.HTTPStatus.OK, submission_result

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
    def add_submission(homework_id: int,
                       submission: models.submission.Submission,
                       db: Session) -> Tuple[int, Union[str, int]]:
        homework = HomeworkRepository.get_homework(homework_id, db)
        if homework is None:
            return http.HTTPStatus.NOT_FOUND, f"No homework with id: {id}"
        submission.homework_id = homework_id
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
        return http.HTTPStatus.OK, submission.id
