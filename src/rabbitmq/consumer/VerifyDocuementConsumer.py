import json
import logging.config
import pandas as pd
from pika.exchange_type import ExchangeType

from src.config.RabbitMQConfig import RabbitMQConfig
from src.excel.verification.dataset_verification import DatasetVerification
from src.excel.verification.dataset_verification_pandas import DatasetVerificationPandas
from src.rabbitmq.consumer.Consumer import Consumer
from src.samba.SambaWorker import SambaWorker

logging.config.fileConfig('../resources/logging.conf')
LOGGER = logging.getLogger('exampleApp')


class VerifyDocumentConsumer(Consumer):

    def __init__(self, rabbit_mq_config: RabbitMQConfig, queue: str, routing_key: str,
                 samba_worker: SambaWorker,
                 exchange: str = "", exchange_type: ExchangeType = ExchangeType.topic):
        self._dataset_verification: DatasetVerification = DatasetVerificationPandas()
        self._samba_worker = samba_worker
        super().__init__(rabbit_mq_config, queue, routing_key, exchange, exchange_type)

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
        decoded_body: dict = json.loads(body)

        project_id = decoded_body.get("projectId")
        file_name: str = decoded_body.get("fileName")
        file = self._samba_worker.download(file_name)
        legend_error_protocol, legend_info_protocol, legend_inc, headers_error_protocol, legend_header, \
            data_headers, values_error_protocol, legend_info_protocol, dataframe_to_save = self._dataset_verification.verify_excel(file)
        file.close()

        index_to_delete = file_name.rfind('.')

        if index_to_delete >= 0:
            file_name = '{0}.csv'.format(file_name[:index_to_delete])


        file = open('/tmp/{0}'.format(file_name), "wb")
        dataframe_to_save.to_csv(file, index=None, header=True, sep=";")
        self._samba_worker.upload(path_to_save='{0}'.format(file_name), file=file.name)
        file.close()
        # self._dataset_verification.verify_excel(file_name)
        # legend_error_protocol, legend_info_protocol, legend_inc, headers_error_protocol, legend_header, \
        # data_headers, values_error_protocol, legend_info_protocol, dataframe_to_save = dataset_verification.verify_excel(file_date_empty)


        # encoded_body = json.dumps(decoded_body)
        #
        # queueConfig = self._rabbit_mq_config.OUTPUT_VERIFICATION_RESULT_CONFIG
        #
        # self._rabbit_mq_writer.writeMessage(exchange=queueConfig.get("exchange"),
        #                                     routing_key=queueConfig.get("routingKey"),
        #                                     message=encoded_body)

        self.acknowledge_message(basic_deliver.delivery_tag)
