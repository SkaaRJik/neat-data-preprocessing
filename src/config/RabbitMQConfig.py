import pika as pika


class RabbitMQConfig:

    def __init__(self, global_config):

        _PORT = "localhost"
        _HOST = 5672
        _USERNAME = "guest"
        _PASSWORD = "guest"
        _HEARTBEAT = 300
        _BLOCKED_CONNECTION_TIMEOUT = 150

        self._INPUT_VERIFICATION_DOCUMENT = {
            "exchange": global_config['rabbitmq']['input']['verificationDocument']['exchange'],
            "queue": global_config['rabbitmq']['input']['verificationDocument']['queueName'],
            "routingKey": global_config['rabbitmq']['input']['verificationDocument']['routingKey']
        }

        self._INPUT_NORMALIZE_DATA = {
            "exchange": global_config['rabbitmq']['input']['normalizeData']['exchange'],
            "queue": global_config['rabbitmq']['input']['normalizeData']['queueName'],
            "routingKey": global_config['rabbitmq']['input']['normalizeData']['routingKey']
        }

        self._OUTPUT_VERIFICATION_RESULT = {
            "exchange": global_config['rabbitmq']['output']['verificationResult']['exchange'],
            "queue": global_config['rabbitmq']['output']['verificationResult']['queueName'],
            "routingKey": global_config['rabbitmq']['output']['verificationResult']['routingKey']
        }

        self._OUTPUT_NORMALIZATION_RESULT = {
            "exchange": global_config['rabbitmq']['output']['normalizationResult']['exchange'],
            "queue": global_config['rabbitmq']['output']['normalizationResult']['queueName'],
            "routingKey": global_config['rabbitmq']['output']['normalizationResult']['routingKey']
        }



        self._HOST = global_config['rabbitmq']['host'] if global_config['rabbitmq']['host'] else _HOST
        self._PORT = global_config['rabbitmq']['port'] if global_config['rabbitmq']['port'] else _PORT
        self._USERNAME = global_config['rabbitmq']['username'] if global_config['rabbitmq']['username'] else _USERNAME
        self._PASSWORD = global_config['rabbitmq']['password'] if global_config['rabbitmq']['password'] else _PASSWORD

        self._HEARTBEAT = global_config['rabbitmq']['heartbeat'] if global_config['rabbitmq']['heartbeat'] else _HEARTBEAT
        self._BLOCKED_CONNECTION_TIMEOUT = global_config['rabbitmq']['blocked_connection_timeout'] if global_config['rabbitmq']['blocked_connection_timeout'] else _BLOCKED_CONNECTION_TIMEOUT

        credentials = pika.PlainCredentials(username=self._USERNAME, password=self._PASSWORD)
        self._connection_parameters = pika.ConnectionParameters(host=self._HOST, port=self._PORT,
                                                                credentials=credentials, heartbeat=self._HEARTBEAT,
                                                                blocked_connection_timeout=self._BLOCKED_CONNECTION_TIMEOUT)

    @property
    def connection_parameters(self):
        return self._connection_parameters

    @property
    def INPUT_VERIFICATION_DOCUMENT_CONFIG(self):
        return self._INPUT_VERIFICATION_DOCUMENT

    @property
    def INPUT_NORMALIZE_DATA_CONFIG(self):
        return self._INPUT_NORMALIZE_DATA

    @property
    def OUTPUT_VERIFICATION_RESULT_CONFIG(self):
        return self._OUTPUT_VERIFICATION_RESULT

    @property
    def OUTPUT_NORMALIZATION_RESULT_CONFIG(self):
        return self._OUTPUT_NORMALIZATION_RESULT


