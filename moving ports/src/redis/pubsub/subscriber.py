from src.mtd.controller import MtdController
from src.redis.client.client import RedisClient
from src.redis.pubsub.configuration import RedisPubSubConfiguration


class RedisSubscriber:

    def __init__(self,
                 redis_client: RedisClient,
                 redis_pub_sub_configuration: RedisPubSubConfiguration,
                 mtd_controller: MtdController):
        self.__redis_connection = redis_client.get_connection()
        self.__channels = redis_pub_sub_configuration.subscriber_channel_names
        self.__mtd_controller = mtd_controller

    def subscribe(self):
        pub_sub = self.__redis_connection.pubsub()
        pub_sub.subscribe(self.__channels)
        try:
            for message in pub_sub.listen():
                print(f"Subscriber: {message}", flush=True)
                if(message["type"] == "message"):
                    self.__mtd_controller.apply_rules()

        except KeyboardInterrupt:
            pub_sub.unsubscribe()
