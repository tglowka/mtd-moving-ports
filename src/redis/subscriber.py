import redis

from src.configs.configuration import RedisClientConfiguration, RedisSubscriberConfiguration


class RedisSubscriber:

    def __init__(self,
                 redis_subscriber_configuration: RedisSubscriberConfiguration,
                 redis_client_configuration: RedisClientConfiguration):
        self.__redis_connection = redis.Redis(host=redis_client_configuration.host,
                                              port=redis_client_configuration.port,
                                              db=redis_client_configuration.db,
                                              charset=redis_client_configuration.charset,
                                              decode_responses=redis_client_configuration.decode_responses)

        self.__channels = redis_subscriber_configuration.subscriber_channel_names

    def subscribe(self,
                  func: object) -> None:
        subscriber = self.__redis_connection.pubsub()
        subscriber.subscribe(self.__channels)

        try:
            for message in subscriber.listen():
                print(f"Subscriber: {message}", flush=True)
                if(message["type"] == "message"):
                    func()

        except KeyboardInterrupt:
            subscriber.unsubscribe()
