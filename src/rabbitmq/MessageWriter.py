import pika

from src.config.RabbitMQConfig import RabbitMQConfig


class MessageWriter:

    def __init__(self, rabbit_mq_config: RabbitMQConfig):
        self._parameters = rabbit_mq_config.connection_parameters

        self._connection = pika.BlockingConnection(self._parameters)

        self._channel = self._connection.channel()

    def writeMessage(self, exchange: str, routing_key: str, message,
                     properties: pika.BasicProperties = pika.BasicProperties(content_type="application/json")):
        self._channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message, properties=properties)

    def closeConnection(self):

        if self._channel is not None and self._channel.is_closed is False:
            self._channel.close()

        if self._connection is not None and self._connection.is_closed is False:
            self._connection.close()
