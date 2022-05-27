import http
import json
import os
from typing import List, Tuple, Union

import pika
from fastapi.encoders import jsonable_encoder
from requests import Session

from database.src import crud, tables
from database.src.tables import SubmitionResult
from web_server.src import models
from web_server.src.models import submition


def get_all_submitions(db: Session) -> Tuple[int, List[tables.Submition]]:
    submissions = crud.get_all_submitions(db)
    return http.HTTPStatus.OK, submissions


def get_submition(id: int, db: Session) -> Tuple[int, Union[str, tables.Submition]]:
    submission = crud.get_submition(id, db)
    if submission is None:
        return http.HTTPStatus.NOT_FOUND, f"No submission with id: {id}"
    return http.HTTPStatus.OK, submission


def get_submition_result(result_id: int, db: Session) -> Tuple[int, Union[str, tables.SubmitionResult]]:
    if result_id is None:
        return http.HTTPStatus.OK, SubmitionResult(accepted=False, commentary="Submition not yet tested")
    submition_result = crud.get_submition_result(result_id, db)
    if submition_result is None:
        return http.HTTPStatus.NOT_FOUND, f"No submition result with id: {id}"
    return http.HTTPStatus.OK, submition_result


def add_submition_to_message_broker(submition: models.submition.Submition) -> None:
    amqp_host = "localhost" if os.environ.get('AMQP_HOST') is None else os.environ.get('AMQP_HOST')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=amqp_host))
    channel = connection.channel()
    channel.queue_declare("tasks")
    body = json.dumps(jsonable_encoder(submition)).encode("utf-8")
    channel.basic_publish(exchange="", routing_key="tasks", body=body)
    connection.close()


def add_homework_solution(homework_id: int,
                          submition: models.submition.Submition,
                          db: Session) -> Tuple[int, Union[str, int]]:
    check_homework = crud.get_student_homework(homework_id, db)
    if check_homework is None:
        return http.HTTPStatus.NOT_FOUND, f"No homework with id: {id}"
    submition.homework_id = homework_id
    submition.result_id = None
    submition = crud.create_homework_solution(submition, db)
    submition_to_message_broker = models.submition.Submition(
        id=submition.id,
        homework_id=submition.homework_id,
        result_id=submition.result_id,
        url=submition.url,
        submition_time=submition.submition_time
    )
    add_submition_to_message_broker(submition_to_message_broker)
    return http.HTTPStatus.OK, submition.id
