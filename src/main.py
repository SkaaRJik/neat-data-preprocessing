import yaml
import logging
import logging.config
from src.config.RabbitMQConfig import RabbitMQConfig
from src.rabbitmq.RabbitMQWorker import RabbitMQWorker
from src.rabbitmq.consumer.VerifyDocuementConsumer import VerifyDocumentConsumer

logging.config.fileConfig('../resources/logging.conf')
LOGGER = logging.getLogger("infoLogger")

with open('../resources/application-dev.yml') as f:
    global_config = yaml.safe_load(f)

rabbitMqConfig: RabbitMQConfig = RabbitMQConfig(global_config)


def onNewVerifyDocument(obj):
    print(obj)


def on_message(_unused_channel, basic_deliver, properties, body):
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


# self.acknowledge_message(basic_deliver.delivery_tag)

def main():
    rabbitMqWorker: RabbitMQWorker = None
    try:
        rabbitMqWorker: RabbitMQWorker = RabbitMQWorker(rabbitMqConfig)
        consumer = VerifyDocumentConsumer(queue=rabbitMqConfig.RABBITMQ_INPUT_VERIFICATION_DOCUMENT_QUEUE,
                            routing_key=rabbitMqConfig.RABBITMQ_INPUT_VERIFICATION_DOCUMENT_ROUTING_KEY,
                            exchange=rabbitMqConfig.RABBITMQ_INPUT_EXCHANGE)
        rabbitMqWorker.add_consumer(consumer)
        rabbitMqWorker.run()
    except BaseException as error:
        print(error)
    finally:
        if rabbitMqWorker is not None:
            rabbitMqWorker.close_connection()
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
