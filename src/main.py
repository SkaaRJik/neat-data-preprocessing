import json

import yaml
import logging
import logging.config
from src.config.RabbitMQConfig import RabbitMQConfig
from src.config.SambaConfig import SambaConfig
from src.processing.normalization.dataset_standard_normalizer import DatasetStandardNormalizer
from src.processing.verification.dataset_verification_pandas import DatasetVerificationPandas

from src.processing.normalization.dataset_min_max_normalizer import DatasetMinMaxNormalizer
from src.processing.normalization.dataset_normalizer import DatasetNormalizer
from src.rabbitmq.RabbitMQWorker import RabbitMQWorker
from src.rabbitmq.consumer.NormalizationDataConsumer import NormalizationDataConsumer
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
    rabbitMqWorker: RabbitMQWorker = None
    sambaWorker: SambaWorker = None
    try:
        rabbitMqWorker: RabbitMQWorker = RabbitMQWorker(rabbitMqConfig)
        sambaWorker: SambaWorker = SambaWorker(sambaConfig)
        sambaWorker.connect()

        config = rabbitMqConfig.INPUT_VERIFICATION_DOCUMENT_CONFIG
        consumer = VerifyDocumentConsumer(rabbit_mq_config=rabbitMqConfig, queue=config.get("queue"),
                            routing_key=config.get("routingKey"),
                            exchange=config.get("exchange"), samba_worker=sambaWorker)
        rabbitMqWorker.add_consumer(consumer)

        config = rabbitMqConfig.INPUT_NORMALIZE_DATA_CONFIG
        consumer = NormalizationDataConsumer(rabbit_mq_config=rabbitMqConfig, queue=config.get("queue"),
                                          routing_key=config.get("routingKey"),
                                          exchange=config.get("exchange"), samba_worker=sambaWorker)
        rabbitMqWorker.add_consumer(consumer)
        rabbitMqWorker.run()


    except BaseException as error:
        traceback.print_exc()
        LOGGER.exception(error)
    finally:
        if rabbitMqWorker is not None:
            rabbitMqWorker.close_connection()
        if sambaWorker is not None:
            sambaWorker.close()

    # normalization_file = '../resources/data.csv'
    # normalization_data: DatasetNormalizer = DatasetStandardNormalizer()
    # normalization_data.normalize(normalization_file)


    # dataset_verification = DatasetVerificationPandas()
    # correct_file = '../resources/data.xlsx'
    # # # file_date_empty = '../resources/data1.xlsx'
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
