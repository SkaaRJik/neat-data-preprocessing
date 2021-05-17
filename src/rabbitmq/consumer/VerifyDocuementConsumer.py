import json
import logging.config
import os

from pandas import DataFrame
from pika.exchange_type import ExchangeType

from src.config.RabbitMQConfig import RabbitMQConfig
from src.processing.verification.dataset_verification import DatasetVerification
from src.processing.verification.dataset_verification_pandas import DatasetVerificationPandas
from src.rabbitmq.consumer.Consumer import Consumer
from src.samba.SambaWorker import SambaWorker

logging.config.fileConfig('../resources/logging.conf')
LOGGER = logging.getLogger('exampleApp')


class VerifyDocumentConsumer(Consumer):

    def __init__(self, rabbit_mq_config: RabbitMQConfig, queue: str, routing_key: str,
                 samba_worker: SambaWorker,
                 exchange: str = "", exchange_type: ExchangeType = ExchangeType.direct):
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
        project_folder = decoded_body.get("projectFolder")
        file_path: str = decoded_body.get("filePath")
        username: str = decoded_body.get("username")

        only_filename_without_extension = self.eject_filename(file_path)

        try:
            dataframe_to_save: DataFrame = None
            file = self._samba_worker.download(file_path, 'ver-{0}-{1}'.format(username, only_filename_without_extension))
            legend_error_protocol, legend_info_protocol, legend_inc, legend_values, headers_error_protocol, legend_header, \
            data_headers, values_error_protocol, values_info_protocol, dataframe_to_save = self._dataset_verification.verify_excel(
                file)
            file.close()
            os.remove(file.name)

            temp_filename = '/tmp/{0}.csv'.format(project_id)
            path_to_save = f'{project_folder}/ver-{only_filename_without_extension}.csv'
            dataframe_to_save.to_csv(temp_filename, sep=';', index=False)


            self._samba_worker.upload(path_to_save=path_to_save, file=temp_filename)

            os.remove(temp_filename)
            errors = self.pack_error_protocols(legend_error_protocol=legend_error_protocol,
                                      headers_error_protocol=headers_error_protocol,
                                      values_error_protocol=values_error_protocol)

            verification_protocol = {
                "projectId": project_id,
                "errors": errors,
                "info": self.pack_info_protocols(legend_info_protocol=legend_info_protocol,
                                                 values_info_protocol=values_info_protocol),
                "verifiedFile": path_to_save,
                "legend": {
                    "header": legend_header,
                    "data": legend_values,
                    "increment": legend_inc
                },
                "logIsAllowed": None if errors is not None else (True if dataframe_to_save.values.min() > 0 else False),
                "headers": data_headers,
                "status": 'VERIFIED' if errors is None else 'VERIFICATION_ERROR'
            }

        except BaseException as ex:
            LOGGER.error('verification: username - {0}, filename - {1}'.format(username, file_path))
            LOGGER.exception(ex)
            verification_protocol = {
                "projectId": project_id,
                "errors": None,
                "info": None,
                "verifiedFile": None,
                "legend": None,
                "logIsAllowed": False,
                "headers": None,
                "status": 'VERIFICATION_SERVICE_ERROR'
            }

        encoded_body = json.dumps(verification_protocol, default=self.np_encoder)

        queue_config = self._rabbit_mq_config.OUTPUT_VERIFICATION_RESULT_CONFIG

        self._rabbit_mq_writer.writeMessage(exchange=queue_config.get("exchange"),
                                            routing_key=queue_config.get("routingKey"),
                                            message=encoded_body)

        self.acknowledge_message(basic_deliver.delivery_tag)



    @staticmethod
    def pack_error_protocols(legend_error_protocol, headers_error_protocol, values_error_protocol) -> dict:
        is_all_protocols_empty = (len(legend_error_protocol) == 0) and (len(headers_error_protocol) == 0) and len(
            values_error_protocol) == 0

        if is_all_protocols_empty:
            return None
        else:
            return {
                "legend_errors": legend_error_protocol,
                "header_errors": headers_error_protocol,
                "values_errors": values_error_protocol,
            }

    @staticmethod
    def pack_info_protocols(legend_info_protocol, values_info_protocol) -> dict:
        is_all_protocols_empty = (len(legend_info_protocol) == 0) and (len(values_info_protocol) == 0)

        if is_all_protocols_empty:
            return None
        else:
            return {
                "legend_info": legend_info_protocol,
                "values_info": values_info_protocol,
            }

