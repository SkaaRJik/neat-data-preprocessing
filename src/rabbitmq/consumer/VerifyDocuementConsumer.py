from pika.exchange_type import ExchangeType

from src.rabbitmq.consumer.Consumer import Consumer
import logging.config

logging.config.fileConfig('../resources/logging.conf')
LOGGER = logging.getLogger('exampleApp')

class VerifyDocumentConsumer(Consumer):

    def __init__(self, queue: str, routing_key: str,
                 exchange: str = "", exchange_type: ExchangeType = ExchangeType.topic):
        super().__init__(queue, routing_key, exchange, exchange_type)

    def on_message(self, _unused_channel, basic_deliver, properties, body):
        """Invoked by pika when a message is delivered from RabbitMQ. The
        channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.
        :param pika.channel.Channel _unused_channel: The channel object
        :param pika.Spec.Basic.Deliver: basic_deliver method
        :param pika.Spec.BasicProperties: properties
        :param bytes body: The message body
        """

        LOGGER.info('Received message # %s from %s: %s',
                    basic_deliver.delivery_tag, properties.app_id, body)
        self.acknowledge_message(basic_deliver.delivery_tag)