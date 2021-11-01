from src.configs.reader import ConfigurationReader
from src.configs.configuration import MtdControllerConfiguration
from src.mtd.controller import MtdController
from src.configs.configuration import RedisClientConfiguration
from src.configs.configuration import RedisSubscriberConfiguration
from src.redis.subscriber import RedisSubscriber


def main():
    # Configuration
    configuration_reader = setup_configuration_reader()

    redis_subscriber = setup_redis(configuration_reader=configuration_reader)

    mtd_controller = setup_mtd_controller(configuration_reader=configuration_reader,
                                          redis_subscriber=redis_subscriber)

    mtd_controller.start()


def setup_configuration_reader() -> ConfigurationReader:
    configuration_reader = ConfigurationReader()
    configuration_reader.read_and_validate_configuration_file()

    return configuration_reader


def setup_mtd_controller(configuration_reader: ConfigurationReader,
                         redis_subscriber: RedisSubscriber) -> MtdController:
    mtd_controller_configuration = MtdControllerConfiguration(
        configuration_reader=configuration_reader)
    mtd_controller = MtdController(
        mtd_controller_configuration=mtd_controller_configuration,
        redis_subscriber=redis_subscriber)

    return mtd_controller


def setup_redis(configuration_reader: ConfigurationReader) -> RedisSubscriber:
    redis_client_configuration = RedisClientConfiguration(
        configuration_reader=configuration_reader)

    redis_subscriber_configuration = RedisSubscriberConfiguration(
        configuration_reader=configuration_reader)

    redis_subscriber = RedisSubscriber(redis_client_configuration=redis_client_configuration,
                                       redis_subscriber_configuration=redis_subscriber_configuration)

    return redis_subscriber


if __name__ == "__main__":
    main()
