import json
import logging.config
import os

from pika.exchange_type import ExchangeType

from src.config.RabbitMQConfig import RabbitMQConfig
from src.processing.normalization.dataset_normalizer_factory import DatasetNormalizerFactory
from src.processing.report.ReportPredictionResultsExcelMaker import ReportPredictionResultsExcelMaker
from src.rabbitmq.consumer.Consumer import Consumer
from src.samba.SambaWorker import SambaWorker

logging.config.fileConfig('../resources/logging.conf')
LOGGER = logging.getLogger('exampleApp')


class ReportResultConsumer(Consumer):

    def __init__(self, rabbit_mq_config: RabbitMQConfig, queue: str, routing_key: str,
                 samba_worker: SambaWorker,
                 exchange: str = "", exchange_type: ExchangeType = ExchangeType.direct):
        self._samba_worker = samba_worker
        self._dataset_normalizer_factory = DatasetNormalizerFactory()
        self._reportMaker = ReportPredictionResultsExcelMaker()
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




        experiment_result_id = decoded_body.get("experimentResultId")
        model = decoded_body.get("model")
        train_errors = decoded_body.get("trainErrors")
        test_errors = decoded_body.get("testErrors")
        prediction_error = decoded_body.get("predictionError")
        prediction_result_file_path = decoded_body.get("predictionResultFile")
        window_train_statistic = decoded_body.get("windowTrainStatistic")

        experiment_id = decoded_body.get("experimentId")
        project_id = decoded_body.get("projectId")
        project_folder = decoded_body.get("projectFolder")
        source_file_path: str = decoded_body.get("verifiedFile")
        columns = decoded_body.get("columns")
        legend = decoded_body.get("legend")
        neat_settings = decoded_body.get("neatSettings")

        normalization_method = decoded_body.get("normalizationMethod")
        enable_log_transform = decoded_body.get("enableLogTransform")
        prediction_period = decoded_body.get("predictionPeriod")
        prediction_window_size = decoded_body.get("predictionWindowSize")
        train_end_index = decoded_body.get("trainEndIndex")
        test_end_index = decoded_body.get("testEndIndex")
        normalization_statistic = decoded_body.get("normalizationStatistic")

        report_response = {
            'experimentId': experiment_id,
            'experimentResultId': experiment_result_id,
            'projectId': project_id,
            'status': 'REPORT_SERVICE_ERROR',
            'predictionReportFile': None,
            'predictionResult': None,
        }









        try:
            pass

            temp = f'source-{project_id}-{experiment_id}.csv'
            source_file = self._samba_worker.download(source_file_path, temp)
            temp = f'results-{project_id}-{experiment_id}.csv'
            result_file = self._samba_worker.download(prediction_result_file_path, temp)


            report_file, predicted_results = self._reportMaker.makeExcelReport(source_file.name,
                                        result_file.name,
                                        train_errors,
                                        test_errors,
                                        prediction_error,
                                        window_train_statistic,
                                        columns,
                                        legend,
                                        neat_settings,
                                        normalization_method,
                                        enable_log_transform,
                                        prediction_period,
                                        prediction_window_size,
                                        train_end_index,
                                        test_end_index,
                                        normalization_statistic
                                        )
            path_to_save = f'{project_folder}/report-{experiment_id}.xlsx'
            self._samba_worker.upload(path_to_save=path_to_save, file=report_file)

            report_response = {
                'experimentId': experiment_id,
                'experimentResultId': experiment_result_id,
                'projectId': project_id,
                'status': 'DONE',
                'predictionReportFile': path_to_save,
                'predictionResult': predicted_results,
            }

            result_file.close()
            source_file.close()
            os.remove(result_file.name)
            os.remove(source_file.name)
            os.remove(report_file)

            # temp = 'norm-{0}-{1}.csv'.format(experiment_id, only_filename_without_extension)
            # file = self._samba_worker.download(file_path, temp)
            # data_normalizer: DatasetNormalizer = dataset_normalizer_factory.getNormalizer(normalization_name)
            #
            # if data_normalizer is None:
            #     raise WrongNormalizationMethodException('{0} - method not found'.format(normalization_name))
            # file.close()
            # dataframe_to_save: DataFrame = data_normalizer.normalize(file.name, log_data)
            #
            # path_to_save = f'{project_folder}/norm-{experiment_id}.csv'
            # temp_name = f'/tmp/norm-{username}-{experiment_id}.csv'
            # file.close()
            # dataframe_to_save.to_csv(temp_name, index=None, header=True, sep=";")
            #
            # self._samba_worker.upload(path_to_save=path_to_save, file=temp_name)
            #
            # os.remove(temp_name)
            #
            # normalization_protocol = {
            #     "experimentId": experiment_id,
            #     "normalizedDatasetFilename": path_to_save,
            #     "statistic": self._calculate_spreading_statistic(dataframe_to_save.values, 10),
            #     "status": "NORMALIZED"
            # }
        except BaseException as ex:
            LOGGER.error('reportConsumer: on_message - {0}'.format(body))
            LOGGER.exception(ex)
            # normalization_protocol = {
            #     "experimentId": experiment_id,
            #     "normalizedDatasetFilename": None,
            #     "normalizationStatistic": None,
            #     "status": "NORMALIZATION_SERVICE_ERROR"
            # }

        encoded_body = json.dumps(report_response)

        queue_config = self._rabbit_mq_config.OUTPUT_REPORT_RESULT_CONFIG

        self._rabbit_mq_writer.writeMessage(exchange=queue_config.get("exchange"), routing_key=queue_config.get("routingKey"), message=encoded_body)

        self.acknowledge_message(basic_deliver.delivery_tag)





