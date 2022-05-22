import os
from typing import Union

import pika
from fastapi import Depends
from pika.exceptions import ConnectionClosedByBroker, AMQPConnectionError, AMQPChannelError
from sqlalchemy.orm import Session

from database.src.database import Database
from web_server.src.models.submition import Submition


class ResultListener:

    def __init__(self):
        amqp_host = "localhost" if os.environ.get('AMQP_HOST') is None else os.environ.get('AMQP_HOST')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=amqp_host))
        self.channel = self.connection.channel()
        self.channel.queue_declare("results")

    def run(self) -> None:
        def callback(ch, method, properties, body):
            pass

        while True:
            try:
                self.channel.basic_consume("results", callback, True)
                self.channel.start_consuming()
            except (Union[ConnectionClosedByBroker, AMQPChannelError, KeyboardInterrupt]):
                break
            except AMQPConnectionError:
                continue

    def accept(self, submition: Submition, db: Session = Depends(Database.get_db)):
        pass
