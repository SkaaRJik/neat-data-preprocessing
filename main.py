import sys
sys.path.insert(0, 'src')
import logging.config
import traceback

import yaml

from src.config.RabbitMQConfig import RabbitMQConfig
from src.config.SambaConfig import SambaConfig
from src.rabbitmq.RabbitMQWorker import RabbitMQWorker
from src.rabbitmq.consumer.NormalizationDataConsumer import NormalizationDataConsumer
from src.rabbitmq.consumer.ReportResultConsumer import ReportResultConsumer
from src.rabbitmq.consumer.VerifyDocuementConsumer import VerifyDocumentConsumer
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


    except KeyboardInterrupt:
        pass
    except BaseException as error:
        traceback.print_exc()
        LOGGER.exception(error)

    finally:
        if rabbit_mq_worker is not None:
            rabbit_mq_worker.close_connection()
        if samba_worker is not None:
            samba_worker.close()


if __name__ == "__main__":
    main()

