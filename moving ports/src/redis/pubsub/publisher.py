from src.redis.client.client import RedisClient
from src.redis.pubsub.configuration import RedisPubSubConfiguration
from datetime import datetime


class RedisPublisher:

    def __init__(self,
                 redis_client: RedisClient,
                 redis_pub_sub_configuration: RedisPubSubConfiguration):
        self.__redis_connection = redis_client.get_connection()
        self.__channel = redis_pub_sub_configuration.publisher_channel_name

    def publish(self, message):
        self.__redis_connection.publish(self.__channel, message)
        print(f"Publisher: {message}", flush=True)
