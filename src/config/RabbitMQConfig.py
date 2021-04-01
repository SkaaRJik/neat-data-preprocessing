import pika as pika


class RabbitMQConfig:

    def __init__(self, global_config):
        _RABBITMQ_INPUT_EXCHANGE = 'data-preprocessing-service'
        _RABBITMQ_INPUT_VERIFICATION_DOCUMENT_QUEUE = 'data-verification'
        _RABBITMQ_INPUT_VERIFICATION_DOCUMENT_ROUTING_KEY = 'data'
        _RABBITMQ_OUTPUT_EXCHANGE = 'user-queries-service'
        _RABBITMQ_OUTPUT_VERIFICATION_RESULT_QUEUE = 'verification-result'
        _RABBITMQ_OUTPUT_VERIFICATION_ROUTING_KEY = 'verification-result'
        _HOST = 5672
        _PORT = 'localhost'
        _USERNAME = ''
        _PASSWORD = ''

        self._RABBITMQ_INPUT_EXCHANGE = global_config['rabbitmq']['input']['exchange'] if \
        global_config['rabbitmq']['input']['exchange'] else _RABBITMQ_INPUT_EXCHANGE
        self._RABBITMQ_INPUT_VERIFICATION_DOCUMENT_QUEUE = \
        global_config['rabbitmq']['input']['queues']['verificationDocument']['queueName'] if \
        global_config['rabbitmq']['input']['queues']['verificationDocument'][
            'queueName'] else _RABBITMQ_INPUT_VERIFICATION_DOCUMENT_QUEUE
        self._RABBITMQ_INPUT_VERIFICATION_DOCUMENT_ROUTING_KEY = \
        global_config['rabbitmq']['input']['queues']['verificationDocument']['routingKey'] if \
        global_config['rabbitmq']['input']['queues']['verificationDocument'][
            'routingKey'] else _RABBITMQ_INPUT_VERIFICATION_DOCUMENT_ROUTING_KEY
        self._RABBITMQ_OUTPUT_EXCHANGE = global_config['rabbitmq']['output']['exchange'] if \
        global_config['rabbitmq']['output']['exchange'] else _RABBITMQ_OUTPUT_EXCHANGE
        self._RABBITMQ_OUTPUT_VERIFICATION_RESULT_QUEUE = \
        global_config['rabbitmq']['output']['queues']['verificationResult']['queueName'] if \
        global_config['rabbitmq']['output']['queues']['verificationResult'][
            'queueName'] else _RABBITMQ_OUTPUT_VERIFICATION_RESULT_QUEUE
        self._RABBITMQ_OUTPUT_VERIFICATION_ROUTING_KEY = \
        global_config['rabbitmq']['output']['queues']['verificationResult']['routingKey'] if \
        global_config['rabbitmq']['output']['queues']['verificationResult'][
            'routingKey'] else _RABBITMQ_OUTPUT_VERIFICATION_ROUTING_KEY
        self._HOST = global_config['rabbitmq']['host'] if global_config['rabbitmq']['host'] else _HOST
        self._PORT = global_config['rabbitmq']['port'] if global_config['rabbitmq']['port'] else _PORT
        self._USERNAME = global_config['rabbitmq']['username'] if global_config['rabbitmq']['username'] else _USERNAME
        self._PASSWORD = global_config['rabbitmq']['password'] if global_config['rabbitmq']['password'] else _PASSWORD

        credentials = pika.PlainCredentials(username=self._USERNAME, password=self._PASSWORD)
        self._connection_parameters = pika.ConnectionParameters(host=self._HOST, port=self._PORT,
                                                                credentials=credentials)

    def get_connection_parameters(self):
        return self._connection_parameters

    @property
    def RABBITMQ_INPUT_EXCHANGE(self):
        return self._RABBITMQ_INPUT_EXCHANGE

    @property
    def RABBITMQ_INPUT_VERIFICATION_DOCUMENT_QUEUE(self):
        return self._RABBITMQ_INPUT_VERIFICATION_DOCUMENT_QUEUE

    @property
    def RABBITMQ_INPUT_VERIFICATION_DOCUMENT_ROUTING_KEY(self):
        return self._RABBITMQ_INPUT_VERIFICATION_DOCUMENT_ROUTING_KEY

    @property
    def RABBITMQ_OUTPUT_EXCHANGE(self):
        return self._RABBITMQ_OUTPUT_EXCHANGE

    @property
    def RABBITMQ_OUTPUT_VERIFICATION_RESULT_QUEUE(self):
        return self._RABBITMQ_OUTPUT_VERIFICATION_RESULT_QUEUE

    @property
    def RABBITMQ_OUTPUT_VERIFICATION_ROUTING_KEY(self):
        return self._RABBITMQ_OUTPUT_VERIFICATION_ROUTING_KEY
