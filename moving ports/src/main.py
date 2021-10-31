import sys

from src.configs.reader import ConfigurationReader
from src.mtd.configuration import MtdControllerConfiguration
from src.mtd.controller import MtdController
from src.redis.client.client import RedisClient
from src.redis.client.configuration import RedisClientConfiguration
from src.redis.pubsub.configuration import RedisPubSubConfiguration
from src.redis.pubsub.publisher import RedisPublisher
from src.redis.pubsub.subscriber import RedisSubscriber
from src.watcher.configuration import LogfilesWatcherConfiguration
from src.watcher.watcher import LogfilesWatcher


def main(mode: str):
    # Configuration
    configuration_reader = ConfigurationReader()
    configuration_reader.read_and_validate_configuration_file()

    # Mtd
    mtd_controller_configuration = MtdControllerConfiguration(
        configuration_reader=configuration_reader)

    mtd_controller = MtdController(
        mtd_controller_configuration=mtd_controller_configuration)

    # Redis
    redis_client_configuration = RedisClientConfiguration(
        configuration_reader=configuration_reader)

    redis_pub_sub_configuration = RedisPubSubConfiguration(
        configuration_reader=configuration_reader)

    redis_client = RedisClient(
        redis_client_configuration=redis_client_configuration)

    redis_publisher = RedisPublisher(
        redis_client=redis_client,
        redis_pub_sub_configuration=redis_pub_sub_configuration)

    redis_subscriber = RedisSubscriber(
        redis_client=redis_client,
        redis_pub_sub_configuration=redis_pub_sub_configuration,
        mtd_controller=mtd_controller)

    # Watcher
    logfiles_watcher_configuration = LogfilesWatcherConfiguration(
        configuration_reader=configuration_reader)

    # Watcher
    logfiles_watcher = LogfilesWatcher(
        logfiles_watcher_configuration=logfiles_watcher_configuration,
        redis_publisher=redis_publisher)

    if(mode == 'watcher'):
        logfiles_watcher.start_observer()
    if(mode == 'sub'):
        redis_subscriber.subscribe()


if __name__ == "__main__":
    mode = sys.argv[1]
    main(mode)
