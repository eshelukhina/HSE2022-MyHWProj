import os

import pika
from pika.exceptions import ConnectionClosedByBroker, AMQPChannelError

from web_server.src.models.submition import Submition
from web_server.src.models.submition_result import SubmitionResult


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
            self.channel_to_produce.basic_publish(exchange="", routing_key="results", body=body)

        self.channel_to_consume.basic_consume("tasks", callback, True)

        while True:
            try:
                self.channel_to_consume.start_consuming()
            except (ConnectionClosedByBroker | AMQPChannelError | KeyboardInterrupt):
                break

    def __check_submition__(self, submition: Submition) -> SubmitionResult:
        pass

    def add_result_to_queue(self, submition: Submition) -> None:
        pass
