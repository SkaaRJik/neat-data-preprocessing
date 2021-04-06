import yaml
import logging
import logging.config
from src.config.RabbitMQConfig import RabbitMQConfig
from src.config.SambaConfig import SambaConfig
from src.rabbitmq.RabbitMQWorker import RabbitMQWorker
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
        verificationInputConfig = rabbitMqConfig.INPUT_VERIFICATION_DOCUMENT_CONFIG
        consumer = VerifyDocumentConsumer(rabbit_mq_config=rabbitMqConfig, queue=verificationInputConfig.get("queue"),
                            routing_key=verificationInputConfig.get("routingKey"),
                            exchange=verificationInputConfig.get("exchange"), samba_worker=sambaWorker)
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
    correct_file = '../resources/data.xlsx'
    # file_date_empty = '../resources/data1.xlsx'
    file_number_empty = '../resources/data2.xlsx'


# dataset_verification = DatasetVerificationPandas()
# dataset_verification.verify_excel(correct_file)
# legend_error_protocol, legend_info_protocol, legend_inc, headers_error_protocol, legend_header, \
# data_headers, values_error_protocol, legend_info_protocol, dataframe_to_save = dataset_verification.verify_excel(file_date_empty)
# #dataset_verification.verify_excel(file_number_empty)

if __name__ == "__main__":
    main()
