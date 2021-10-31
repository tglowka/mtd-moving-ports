from src.configs.reader import ConfigurationReader

REDIS_CLIENT_CONFIGURATION = "redis_client_configuration"
HOST = "host"
PORT = "port"
DB = "db"
CHARSET = "charset"
DECODE_RESPONSES = "decode_responses"


class RedisClientConfiguration:

    def __init__(self,
                 configuration_reader: ConfigurationReader):
        self.__redis_client_configuration = configuration_reader.get_configuration_json()[
            REDIS_CLIENT_CONFIGURATION]
        self.host = self.__redis_client_configuration[HOST]
        self.port = self.__redis_client_configuration[PORT]
        self.db = self.__redis_client_configuration[DB]
        self.charset = self.__redis_client_configuration[CHARSET]
        self.decode_responses = self.__redis_client_configuration[DECODE_RESPONSES]
