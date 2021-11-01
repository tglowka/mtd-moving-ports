import secrets
from typing import List, Set
from src.configs.configuration import MtdControllerConfiguration

NFT_SOURCE_ADDRESS_TOKEN = "{{SOURCE_ADDRESS}}"
NFT_DESTINATION_PORT_TOKEN = "\"{{DESTINATION_PORT}}\""
NFT_REDIRECTED_PORT_TOKEN = "\"{{REDIRECTED_PORT}}\""
NFT_PROTOCOL_TOKEN = "{{PROTOCOL}}"


class RulesGenerator:
    def __init__(self,
                 mtd_controller_configuration: MtdControllerConfiguration) -> None:
        self.__max_port_number = mtd_controller_configuration.get_max_port_numer()
        self.__all_used_ports_by_protocol = mtd_controller_configuration.get_all_used_ports_by_protocol()
        self.__ports_to_shuffle_by_address_and_protocol = mtd_controller_configuration.get_ports_to_shuffle_by_address_and_protocol()
        self.__nft_startup_template = mtd_controller_configuration.get_nft_startup_file_content_as_string()
        self.__nft_address_rules_template = mtd_controller_configuration.get_nft_address_rules_content_as_string()

    def get_nftables_startup_commands(self) -> str:
        return self.__nft_startup_template

    def generate_nftables_address_rules(self) -> List[str]:
        rules_list = []

        for address, ports_by_protocol in self.__ports_to_shuffle_by_address_and_protocol.items():
            for protocol, ports in ports_by_protocol.items():
                copied_ports_set = ports.copy()

                closed_ports_count = len(copied_ports_set)
                closed_ports = self.__choose_closed_ports(
                    count=closed_ports_count, protocol=protocol)

                for i in range(closed_ports_count):

                    destination_port = copied_ports_set.pop()
                    redirected_port = closed_ports.pop()

                    rules_list.append(self.__get_template_with_replaced_tokens(
                        source_address=address,
                        destination_port=destination_port,
                        redirected_port=redirected_port,
                        protocol=protocol))

        return rules_list

    def __choose_closed_ports(self,
                              count,
                              protocol) -> Set[int]:
        closed_ports = set()

        while(len(closed_ports) < count):
            port_number = secrets.randbelow(self.__max_port_number + 1)

            if (port_number == 0):
                continue

            if (self.__check_all_used_ports_contains(protocol=protocol,
                                                     port_number=port_number)):
                continue

            closed_ports.add(port_number)

        return closed_ports

    def __check_all_used_ports_contains(self,
                                        protocol: str,
                                        port_number: int) -> bool:
        contains = (protocol in self.__all_used_ports_by_protocol and
                    port_number in self.__all_used_ports_by_protocol[protocol])
        return contains

    def __get_template_with_replaced_tokens(self,
                                            source_address: str,
                                            destination_port: int,
                                            redirected_port: int,
                                            protocol: str) -> str:
        rules = ""

        rules = self.__nft_address_rules_template \
            .replace(NFT_SOURCE_ADDRESS_TOKEN, source_address) \
            .replace(NFT_DESTINATION_PORT_TOKEN, str(destination_port)) \
            .replace(NFT_REDIRECTED_PORT_TOKEN, str(redirected_port)) \
            .replace(NFT_PROTOCOL_TOKEN, protocol)

        return rules
