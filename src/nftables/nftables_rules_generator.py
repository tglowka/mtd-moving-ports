import secrets
from typing import List, Set
from src.configs.configs import NftablesConfig


class NftablesRulesGenerator:
    def __init__(self, nftables_config: NftablesConfig) -> None:

        self.__NFT_SOURCE_ADDRESS_TOKEN = "{{SOURCE_ADDRESS}}"
        self.__NFT_DESTINATION_PORT_TOKEN = "\"{{DESTINATION_PORT}}\""
        self.__NFT_REDIRECTED_PORT_TOKEN = "\"{{REDIRECTED_PORT}}\""
        self.__NFT_PROTOCOL_TOKEN = "{{PROTOCOL}}"
        self.__protocol = 'tcp'

        self.__nftables_config = nftables_config

    def get_nftables_startup_commands(self) -> str:
        return self.__nftables_config.get_nft_startup_content()

    def generate_nftables_address_rules(self) -> List[str]:
        rules_list = []

        for ip, ports in self.__nftables_config.get_ports_to_shuffle_by_address().items():
            destination_ports = ports
            redirection_ports = self.__choose_closed_ports(len(ports))

            for destination_port, redirection_port in range(zip(destination_ports, redirection_ports)):
                rules_list.append(self.__get_template_with_replaced_tokens(
                    source_address=ip,
                    destination_port=destination_port,
                    redirected_port=redirection_port,
                    protocol=self.__protocol))

        return rules_list

    def __choose_closed_ports(self, count) -> Set[int]:
        closed_ports = set()
        max_port = self.__nftables_config.get_max_port_numer() + 1

        while(len(closed_ports) < count):
            port_number = secrets.randbelow(max_port)

            if (port_number == 0):
                continue

            if (self.__tcp_ports_contains(port_number)):
                continue

            closed_ports.add(port_number)

        return closed_ports

    def __tcp_ports_contains(self, port_number: int) -> bool:
        return port_number in self.__nftables_config.get_tcp_ports()

    def __get_template_with_replaced_tokens(self,
                                            source_address: str,
                                            destination_port: int,
                                            redirected_port: int,
                                            protocol: str) -> str:
        rules = self.__nftables_config.get_nft_address_rules_content() \
            .replace(self.__NFT_SOURCE_ADDRESS_TOKEN, source_address) \
            .replace(self.__NFT_DESTINATION_PORT_TOKEN, str(destination_port)) \
            .replace(self.__NFT_REDIRECTED_PORT_TOKEN, str(redirected_port)) \
            .replace(self.__NFT_PROTOCOL_TOKEN, protocol)

        return rules
