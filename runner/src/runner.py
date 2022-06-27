import json
import os

import pika
from pika.exceptions import ConnectionClosedByBroker, AMQPChannelError
from sqlalchemy.orm import Session

from database.src.database import engine
from runner.src.checker import CheckerInfo, Checker, checker_dict
from web_server.src.models.submission_result import SubmissionResult
from web_server.src.repositories.submission_repository import SubmissionRepository


class Runner:

    def __init__(self) -> None:
        amqp_host = "localhost" if os.environ.get("AMQP_HOST") is None else os.environ.get("AMQP_HOST")
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=amqp_host))
        self.channel_to_consume = self.connection.channel()
        self.channel_to_produce = self.connection.channel()
        self.channel_to_consume.queue_declare(queue="tasks")
        self.channel_to_produce.queue_declare(queue="results")
        self.session = Session(engine)

    def run(self):
        def callback(ch, method, properties, body):
            info: CheckerInfo = CheckerInfo(**json.loads(body))
            checker: Checker = checker_dict[info.homework_checker]
            result: SubmissionResult = checker.check(info)
            SubmissionRepository.create_submission_result(result, self.session)

        self.channel_to_consume.basic_consume("tasks", callback, True)

        while True:
            try:
                self.channel_to_consume.start_consuming()
            except (ConnectionClosedByBroker | AMQPChannelError | KeyboardInterrupt):
                break
