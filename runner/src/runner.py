import json
import os

import pika
from pika.exceptions import ConnectionClosedByBroker, AMQPChannelError

from runner.src.checker import CheckerInfo, Checker, checker_dict
from web_server.src.models.submission_result import SubmissionResult


class Runner:

    def __init__(self) -> None:
        amqp_host = "localhost" if os.environ.get("AMQP_HOST") is None else os.environ.get("AMQP_HOST")
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=amqp_host))
        self.channel_to_consume = self.connection.channel()
        self.channel_to_produce = self.connection.channel()
        self.channel_to_consume.queue_declare(queue="tasks")
        self.channel_to_produce.queue_declare(queue="results")

    def run(self):
        def callback(ch, method, properties, body):
            info: CheckerInfo = CheckerInfo(**json.loads(body))
            checker: Checker = checker_dict[info.homework_checker]
            result: SubmissionResult = checker.check(info)
            self.channel_to_produce.basic_publish(
                exchange="",
                routing_key="results",
                body=result.json().encode("utf-8")
            )

        self.channel_to_consume.basic_consume("tasks", callback, True)

        while True:
            try:
                self.channel_to_consume.start_consuming()
            except (ConnectionClosedByBroker | AMQPChannelError | KeyboardInterrupt):
                break
