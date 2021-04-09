import logging
import logging.config
import time
from pika.exchange_type import ExchangeType
import pika
from multiprocessing import Process
from src.config.RabbitMQConfig import RabbitMQConfig
from src.rabbitmq.MessageWriter import MessageWriter
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
        self._rabbit_mq_writer = MessageWriter(rabbit_mq_config)

        self._conn = pika.BlockingConnection(parameters=rabbit_mq_config.connection_parameters)

        self._chan = self._conn.channel()

        self._registrateExchangesAndTopics(rabbit_mq_config)
        self._process_list = []


        # If publish causes the connection to become blocked, then this conn.close()
        # would hang until the connection is unblocked, if ever. However, the
        # blocked_connection_timeout connection parameter would interrupt the wait,
        # resulting in ConnectionClosed exception from BlockingConnection (or the
        # on_connection_closed callback call in an asynchronous adapter)
        self._conn.close()

    def run_consumer(self, consumer):
        while True:
            try:
                consumer.run()
            except KeyboardInterrupt:
                consumer.stop()
                break
            self._maybe_reconnect(consumer)

    def run(self):

        for consumer in self._consumers:
            process = Process(target=self.run_consumer, args=(consumer,))
            self._process_list.append(process)
            process.start()


        # wait for all process to finish
        for process in self._process_list:
            process.join()

        self._rabbit_mq_writer.closeConnection()


    def add_consumer(self, consumer: Consumer):
        consumer.set_connection_params(self._rabbit_mq_config.connection_parameters)
        consumer.set_writer(self._rabbit_mq_writer)
        self._consumers.append(consumer)

    def _maybe_reconnect(self, consumer):
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
            self._reconnect_delay += 60
        if self._reconnect_delay >= 300:
            self._reconnect_delay = 300
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
    def _registrateExchangesAndTopics(self, rabbit_mq_config: RabbitMQConfig):
        topics_configs = [
            rabbit_mq_config.OUTPUT_VERIFICATION_RESULT_CONFIG,
            rabbit_mq_config.OUTPUT_NORMALIZATION_RESULT_CONFIG
        ]

        for config in topics_configs:
            self._chan.exchange_declare(exchange=config.get("exchange"), exchange_type=ExchangeType.direct, durable=True)
            self._chan.queue_declare(queue=config.get("queue"), durable=True)
            self._chan.queue_bind(queue=config.get("queue"), exchange=config.get("exchange"), routing_key=config.get("routingKey"))