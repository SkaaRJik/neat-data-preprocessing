import json
import logging.config
from decimal import Decimal

from numpy import ndarray
from pandas import DataFrame
from pika.exchange_type import ExchangeType

from src.config.RabbitMQConfig import RabbitMQConfig
from src.exceptions.WrongNormalizationMethodException import WrongNormalizationMethodException
from src.processing.normalization.dataset_normalizer import DatasetNormalizer
from src.processing.normalization.dataset_normalizer_factory import dataset_normalizer_factory
from src.rabbitmq.consumer.Consumer import Consumer
from src.samba.SambaWorker import SambaWorker

logging.config.fileConfig('../resources/logging.conf')
LOGGER = logging.getLogger('exampleApp')


class NormalizationDataConsumer(Consumer):

    def __init__(self, rabbit_mq_config: RabbitMQConfig, queue: str, routing_key: str,
                 samba_worker: SambaWorker,
                 exchange: str = "", exchange_type: ExchangeType = ExchangeType.topic):
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
        normalization_name: str = decoded_body.get("normalizationMethod")
        username: str = decoded_body.get("username")
        log_data: bool = decoded_body.get("log")

        only_filename_without_extension = self.eject_filename(file_name)





        try:
            temp = '{0}-{1}.csv'.format(username, only_filename_without_extension)
            file = self._samba_worker.download(file_name, temp)
            data_normalizer: DatasetNormalizer = dataset_normalizer_factory.getNormalizer(normalization_name)

            if data_normalizer is None:
                raise WrongNormalizationMethodException('{0} - method not found'.format(normalization_name))
            file.close()
            dataframe_to_save: DataFrame = data_normalizer.normalize(file.name, log_data)


            index_from_delete = file_name.rfind('/')



            path_to_save = '/{0}/normalized/{1}.csv'.format(username, only_filename_without_extension)
            temp_name = '/tmp/normalized-{0}-{1}.csv'.format(username,only_filename_without_extension)
            dataframe_to_save.to_csv(temp_name, index=None, header=True, sep=";")
            self._samba_worker.upload(path_to_save=path_to_save, file=temp_name)


            normalization_protocol = {
                "projectId": project_id,
                "normalizedDatasetFilename": path_to_save,
                "statistic": self._calculate_spreading_statistic(dataframe_to_save.values, 10),
                "status": "Normalized"
            }
        except BaseException as ex:
            LOGGER.error('normalization: normalizedDatasetFilename - {0}'.format(file_name))
            LOGGER.exception(ex)
            normalization_protocol = {
                "projectId": project_id,
                "normalizedDatasetFilename": None,
                "statistic": None,
                "status": "Service_Error"
            }

        encoded_body = json.dumps(normalization_protocol)

        queue_config = self._rabbit_mq_config.OUTPUT_NORMALIZATION_RESULT_CONFIG

        self._rabbit_mq_writer.writeMessage(exchange=queue_config.get("exchange"),
                                            routing_key=queue_config.get("routingKey"),
                                            message=encoded_body)




        self.acknowledge_message(basic_deliver.delivery_tag)

    @staticmethod
    def _calculate_spreading_statistic(dataframe: ndarray, chart_spaces: int) -> dict:

        max_range = Decimal('{0:.2f}'.format(dataframe.max()))
        min_range = Decimal('{0:.2f}'.format(dataframe.min()))
        spaces = chart_spaces - 1
        step = Decimal('{0:.2f}'.format((max_range - min_range) / spaces))

        statistic = []
        for i in range(0, chart_spaces):
            statistic.append(0)

        for column in dataframe:
            for value in column:
                current = min_range
                for i in range(0, chart_spaces):
                    if value >= current and value < current + step:
                        statistic[i] += 1
                        break
                    current = current + step

        protocol = {}
        current = min_range
        for i in range(0, spaces):
            protocol['[ {0:.2f}-{1:.2f} )'.format(current, current + step)] = statistic[i] / dataframe.size
            current = current + step
        protocol['[ {0:.2f}-{1:.2f} ]'.format(current, max_range)] = statistic[spaces] / dataframe.size
        return protocol



