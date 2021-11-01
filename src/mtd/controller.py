from nftables.nftables import Nftables
from redis.subscriber import RedisSubscriber
from src.mtd.nftables_controller import NftablesController
from src.mtd.rules_generator import RulesGenerator
from src.configs.configuration import MtdControllerConfiguration


class MtdController:

    def __init__(self,
                 mtd_controller_configuration: MtdControllerConfiguration,
                 redis_subscriber: RedisSubscriber):
        rules_generator = RulesGenerator(
            mtd_controller_configuration=mtd_controller_configuration)

        self.__nftables_controller = NftablesController(
            rules_generator=rules_generator, nftables=Nftables())

        self.__redis_subscriber = redis_subscriber

    def apply_rules(self):
        self.__nftables_controller.prepare_nftables_json()
        self.__nftables_controller.apply_rules()

    def start(self):
        self.__redis_subscriber.subscribe(func=self.apply_rules)
