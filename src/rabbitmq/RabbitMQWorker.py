import logging
import logging.config
import time

from src.config import RabbitMQConfig
from src.rabbitmq.consumer.Consumer import Consumer

logging.config.fileConfig('../resources/logging.conf')
LOGGER = logging.getLogger('exampleApp')


class RabbitMQWorker:
    """This is an example consumer that will reconnect if the nested
    ExampleConsumer indicates that a reconnect is necessary.
    """

    def __init__(self, rabbit_mq_config: RabbitMQConfig):
        self._reconnect_delay = 0
        self._rabbit_mq_config = rabbit_mq_config;
        self._consumers: list[Consumer] = []

    def run(self):
        while True:
            try:
                for consumer in self._consumers:
                    consumer.run()
            except KeyboardInterrupt:
                for consumer in self._consumers:
                    consumer.stop()
                break
            self._maybe_reconnect()

    def add_consumer(self, consumer: Consumer):
        consumer.set_connection_params(self._rabbit_mq_config.get_connection_parameters())
        self._consumers.append(consumer)

    def _maybe_reconnect(self):
        for consumer in self._consumers:
            if consumer.should_reconnect:
                consumer.stop()
                reconnect_delay = self._get_reconnect_delay(consumer)
                LOGGER.info('Reconnecting after %d seconds', reconnect_delay)
                time.sleep(reconnect_delay)
                consumer.reset()

    def _get_reconnect_delay(self, consumer):
        if consumer.was_consuming:
            self._reconnect_delay = 0
        else:
            self._reconnect_delay += 1
        if self._reconnect_delay > 30:
            self._reconnect_delay = 30
        return self._reconnect_delay

    def close_connection(self):
        for consumer in self._consumers:
            consumer.stop()

    # def __init__(self, rabbitMqConfig: RabbitMQConfig):
    #     self._rabbitMqConfig = rabbitMqConfig
    #
    #     self._connection = pika.BlockingConnection(parameters=self._rabbitMqConfig.get_connection_parameters())
    #     self._channel = self._connection.channel()
    #     self._channel.exchange_declare(exchange=self._RABBITMQ_INPUT_EXCHANGE)
    #     self._channel.queue_declare(exchange=self._RABBITMQ_INPUT_VERIFICATION_DOCUMENT_QUEUE)
    #
    # def add_callback_for_queue(self, callback, queue):
    #     self._channel.basic_consume(on_message_callback=callback, queue=queue)
    #
    #
    #
    # def run(self):
    #     self._channel.start_consuming()
    #
    # def stop(self):
    #     self._channel.stop_consuming()
    #
    # def close_connection(self):
    #     self.stop()
    #     self._connection.close()
