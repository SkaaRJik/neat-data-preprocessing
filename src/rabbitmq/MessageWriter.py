import pika

from src.config.RabbitMQConfig import RabbitMQConfig
import logging.config

logging.config.fileConfig('../resources/logging.conf')
LOGGER = logging.getLogger('exampleApp')

class MessageWriter:

    def __init__(self, rabbit_mq_config: RabbitMQConfig):
        self._parameters = rabbit_mq_config.connection_parameters

        self._connection = pika.BlockingConnection(self._parameters)

        self._channel = self._connection.channel()

    def writeMessage(self, exchange: str, routing_key: str, message,
                     properties: pika.BasicProperties = pika.BasicProperties(content_type="application/json")):
        try:
            self._channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message, properties=properties)
        except ConnectionError as error:
            LOGGER.error(error)
            self._reconnect()
            self._channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message, properties=properties)
        except BaseException as error:
            LOGGER.error(error)


    def closeConnection(self):

        if self._channel is not None and self._channel.is_closed is False:
            self._channel.close()

        if self._connection is not None and self._connection.is_closed is False:
            self._connection.close()

    def _reconnect(self):
        LOGGER.info('Trying to reconnect MessageWriter...')
        if(self._connection is not None):
            if(self._connection.is_open):
                self._connection.close()

        self._connection = pika.BlockingConnection(self._parameters)

        self._channel = self._connection.channel()
        LOGGER.info('MessageWriter reconnected!')