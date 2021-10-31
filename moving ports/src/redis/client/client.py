import redis
from src.redis.client.configuration import RedisClientConfiguration


class RedisClient:

    def __init__(self, redis_client_configuration: RedisClientConfiguration):
        self.__redis_connection = redis.Redis(host=redis_client_configuration.host,
                                             port=redis_client_configuration.port,
                                             db=redis_client_configuration.db,
                                             charset=redis_client_configuration.charset,
                                             decode_responses=redis_client_configuration.decode_responses)

    def get_connection(self):
        return self.__redis_connection
