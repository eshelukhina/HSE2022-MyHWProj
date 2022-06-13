import json
import os

import pika
from pika.exceptions import ConnectionClosedByBroker, AMQPConnectionError, AMQPChannelError
from sqlalchemy.orm import Session

from database.src import crud
from database.src.database import engine
from web_server.src.models.submission_result import SubmissionResult


class ResultListener:

    def __init__(self):
        amqp_host = "localhost" if os.environ.get('AMQP_HOST') is None else os.environ.get('AMQP_HOST')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=amqp_host))
        self.channel = self.connection.channel()
        self.channel.queue_declare("results")
        self.session = Session(engine)

    def run(self) -> None:
        def callback(ch, method, properties, body):
            result: SubmissionResult = SubmissionResult(**json.loads(body))
            crud.create_submission_result(result, self.session)

        self.channel.basic_consume("results", callback, True)

        while True:
            try:
                self.channel.start_consuming()
            except (ConnectionClosedByBroker | AMQPChannelError | KeyboardInterrupt | AMQPConnectionError):
                self.session
                break
