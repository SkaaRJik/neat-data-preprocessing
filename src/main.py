import json

import yaml
import logging
import logging.config
from src.config.RabbitMQConfig import RabbitMQConfig
from src.config.SambaConfig import SambaConfig
from src.processing.normalization.dataset_standard_normalizer import DatasetStandardNormalizer
from src.processing.verification.dataset_verification_pandas import DatasetVerificationPandas
from src.processing.report.ReportPredictionResultsExcelMaker import ReportPredictionResultsExcelMaker

from src.processing.normalization.dataset_min_max_normalizer import DatasetMinMaxNormalizer
from src.processing.normalization.dataset_normalizer import DatasetNormalizer
from src.rabbitmq.RabbitMQWorker import RabbitMQWorker
from src.rabbitmq.consumer.NormalizationDataConsumer import NormalizationDataConsumer
from src.rabbitmq.consumer.ReportResultConsumer import ReportResultConsumer
from src.rabbitmq.consumer.VerifyDocuementConsumer import VerifyDocumentConsumer
import traceback

from src.samba.SambaWorker import SambaWorker

logging.config.fileConfig('../resources/logging.conf')
LOGGER = logging.getLogger("infoLogger")

with open('../resources/application-dev.yml') as f:
    global_config = yaml.safe_load(f)

rabbitMqConfig: RabbitMQConfig = RabbitMQConfig(global_config)
sambaConfig: SambaConfig = SambaConfig(global_config)


def main():
    rabbit_mq_worker: RabbitMQWorker = None
    samba_worker: SambaWorker = None
    try:
        rabbit_mq_worker: RabbitMQWorker = RabbitMQWorker(rabbitMqConfig)
        samba_worker: SambaWorker = SambaWorker(sambaConfig)
        samba_worker.connect()

        config = rabbitMqConfig.INPUT_VERIFICATION_DOCUMENT_CONFIG
        consumer = VerifyDocumentConsumer(rabbit_mq_config=rabbitMqConfig, queue=config.get("queue"),
                            routing_key=config.get("routingKey"),
                            exchange=config.get("exchange"), samba_worker=samba_worker)
        rabbit_mq_worker.add_consumer(consumer)

        config = rabbitMqConfig.INPUT_NORMALIZE_DATA_CONFIG
        consumer = NormalizationDataConsumer(rabbit_mq_config=rabbitMqConfig, queue=config.get("queue"),
                                          routing_key=config.get("routingKey"),
                                          exchange=config.get("exchange"), samba_worker=samba_worker)
        rabbit_mq_worker.add_consumer(consumer)

        config = rabbitMqConfig.INPUT_REPORT_CONFIG
        consumer = ReportResultConsumer(
            rabbit_mq_config=rabbitMqConfig, queue=config.get("queue"),
            routing_key=config.get("routingKey"),
            exchange=config.get("exchange"), samba_worker=samba_worker
        )
        rabbit_mq_worker.add_consumer(consumer)

        rabbit_mq_worker.run()






        # rabbitMqWorker.run()



        # jsonReport = ''
        # with open('../resources/test.json') as f:
        #     jsonReport = f.read()
        #
        #
        # decoded_body: dict = json.loads(jsonReport)
        #
        # experiment_result_id = decoded_body.get("experimentResultId")
        # model = decoded_body.get("model")
        # train_errors = decoded_body.get("trainErrors")
        # test_errors = decoded_body.get("testErrors")
        # prediction_error = decoded_body.get("predictionError")
        # prediction_result_file_path = decoded_body.get("predictionResultFile")
        # window_train_statistic = decoded_body.get("windowTrainStatistic")
        #
        # experiment_id = decoded_body.get("experimentId")
        # project_id = decoded_body.get("projectId")
        # project_folder = decoded_body.get("projectFolder")
        # source_file_path: str = decoded_body.get("verifiedFile")
        # columns = decoded_body.get("columns")
        # legend = decoded_body.get("legend")
        # neat_settings = decoded_body.get("neatSettings")
        #
        # normalization_method = decoded_body.get("normalizationMethod")
        # enable_log_transform = decoded_body.get("enableLogTransform")
        # prediction_period = decoded_body.get("predictionPeriod")
        # prediction_window_size = decoded_body.get("predictionWindowSize")
        # train_end_index = decoded_body.get("trainEndIndex")
        # test_end_index = decoded_body.get("testEndIndex")
        # normalization_statistic = decoded_body.get("normalizationStatistic")
        #
        #
        #
        # temp = f'source-{project_id}-{experiment_id}.csv'
        # source_file = sambaWorker.download(source_file_path, temp)
        # temp = f'results-{project_id}-{experiment_id}.csv'
        # result_file = sambaWorker.download(prediction_result_file_path, temp)
        #
        # reportMaker = ReportPredictionResultsExcelMaker()
        # reportMaker.makeExcelReport(source_file.name,
        #                             result_file.name,
        #                             train_errors,
        #                             test_errors,
        #                             prediction_error,
        #                             window_train_statistic,
        #                             columns,
        #                             legend,
        #                             neat_settings,
        #                             normalization_method,
        #                             enable_log_transform,
        #                             prediction_period,
        #                             prediction_window_size,
        #                             train_end_index,
        #                             test_end_index,
        #                             normalization_statistic
        #                             )


    except BaseException as error:
        traceback.print_exc()
        LOGGER.exception(error)
    finally:
        if rabbit_mq_worker is not None:
            rabbit_mq_worker.close_connection()
        if samba_worker is not None:
            samba_worker.close()

    # normalization_file = '../resources/data.csv'
    # normalization_data: DatasetNormalizer = DatasetStandardNormalizer()
    # normalization_data.normalize(normalization_file)


    # dataset_verification = DatasetVerificationPandas()
    # correct_file = '../resources/data.xlsx'
    # # # file_date_empty = '../resources/dataError.xlsx'
    # # file_number_empty = '../resources/data2.xlsx'
    #
    # # dataset_verification.verify_excel(correct_file)
    # legend_error_protocol, legend_info_protocol, legend_inc, legend_values, headers_error_protocol, legend_header, \
    # data_headers, values_error_protocol, values_info_protocol, dataframe_to_save = dataset_verification.verify_excel(
    #     correct_file)
    # verification_protocol = {
    #     "projectId": 1,
    #     "errors": VerifyDocumentConsumer.pack_error_protocols(legend_error_protocol=legend_error_protocol,
    #                                          headers_error_protocol=headers_error_protocol,
    #                                          values_error_protocol=values_error_protocol),
    #     "info": VerifyDocumentConsumer.pack_info_protocols(legend_info_protocol=legend_info_protocol,
    #                                       values_info_protocol=values_info_protocol),
    #     "verifiedFile": '/tmp/{0}'.format("file_name.csv"),
    #     "legend": {
    #         "header": legend_header,
    #         "data": legend_values,
    #         "increment": legend_inc
    #     },
    #     "headers": data_headers,
    # }
    #
    # encoded_body = json.dumps(verification_protocol)
    # print(encoded_body)

# dataset_verification = DatasetVerificationPandas()
# dataset_verification.verify_excel(correct_file)
# legend_error_protocol, legend_info_protocol, legend_inc, headers_error_protocol, legend_header, \
# data_headers, values_error_protocol, legend_info_protocol, dataframe_to_save = dataset_verification.verify_excel(file_date_empty)
# #dataset_verification.verify_excel(file_number_empty)

if __name__ == "__main__":
    main()
