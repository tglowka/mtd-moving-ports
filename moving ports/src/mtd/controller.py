from nftables.nftables import Nftables
from src.mtd.nftables_controller import NftablesController
from src.mtd.rules_generator import RulesGenerator
from src.mtd.configuration import MtdControllerConfiguration


class MtdController:

    def __init__(self,
                 mtd_controller_configuration: MtdControllerConfiguration):
        self.__mtd_controller_configuration = mtd_controller_configuration
        self.__rules_generator = RulesGenerator(
            mtd_controller_configuration=self.__mtd_controller_configuration)
        self.__nftables_controller = NftablesController(
            rules_generator=self.__rules_generator, nftables=Nftables())

    def apply_rules(self):
        self.__nftables_controller.prepare_nftables_json()
        self.__nftables_controller.apply_rules()
