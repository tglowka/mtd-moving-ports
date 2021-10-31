from src.configs.reader import ConfigurationReader

REDIS_PUB_SUB_CONFIGURATION = "redis_pub_sub_configuration"
SUBSCRIBER_CHANNEL_NAMES = "subscriber_channel_names"
PUBLISHER_CHANNEL_NAME = "publisher_channel_name"


class RedisPubSubConfiguration:

    def __init__(self,
                 configuration_reader: ConfigurationReader):
        self.__redis_pub_sub_configuration = configuration_reader.get_configuration_json()[
            REDIS_PUB_SUB_CONFIGURATION]
        self.subscriber_channel_names = self.__redis_pub_sub_configuration[
            SUBSCRIBER_CHANNEL_NAMES]
        self.publisher_channel_name = self.__redis_pub_sub_configuration[
            PUBLISHER_CHANNEL_NAME]
