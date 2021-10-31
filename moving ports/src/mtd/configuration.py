from typing import Dict, Set
from src.configs.reader import ConfigurationReader

MTD_CONTROLLER_CONFIGURATION = "mtd_controller_configuration"
ALL_USED_PORTS = "all_used_ports"
WATCHED_ADDRESSES = "watched_addresses"
NFT_STARTUP_SCRIPT_PATH = "nft_startup_script_path"
NFT_ADDRESS_RULES_SCRIPT_PATH = "nft_address_rules_script_path"
MAX_PORT_NUMBER = "max_port_number"
ADDRESS = "address"
PORT = "port"
PORTS_TO_IGNORE = "ports_to_ignore"
PROTOCOL = "protocol"
TCP = "TCP"
UDP = "UDP"


class MtdControllerConfiguration:

    def __init__(self,
                 configuration_reader: ConfigurationReader) -> None:
        self.__mtd_controller_configuration = configuration_reader.get_configuration_json()[
            MTD_CONTROLLER_CONFIGURATION]

        self.__all_used_ports = self.__mtd_controller_configuration[ALL_USED_PORTS]
        self.__watched_addresses = self.__mtd_controller_configuration[WATCHED_ADDRESSES]
        self.__nft_startup_script_path = self.__mtd_controller_configuration[
            NFT_STARTUP_SCRIPT_PATH]
        self.__nft_address_rules_script_path = self.__mtd_controller_configuration[
            NFT_ADDRESS_RULES_SCRIPT_PATH]
        self.__max_port_number = self.__mtd_controller_configuration[MAX_PORT_NUMBER]

    def get_max_port_numer(self) -> int:
        return self.__max_port_number

    def get_all_used_ports_by_protocol(self) -> Dict[str, Set[int]]:
        all_used_ports = {}
        all_used_ports = self.__get_grouped_ports_by_protocol(
            port_protocol_pair_list=self.__all_used_ports)

        return all_used_ports

    def get_watched_addresses_by_address_and_protocol(self) -> Dict[str, Dict[str, Set[int]]]:
        watched_addresses = {}

        for watched_address in self.__watched_addresses:
            address = watched_address[ADDRESS]

            if address not in watched_addresses:
                watched_addresses[address] = {}

            ports_to_ignore = watched_address[PORTS_TO_IGNORE]

            grouped_ports_by_protocol = self.__get_grouped_ports_by_protocol(
                port_protocol_pair_list=ports_to_ignore)

            for protocol, ports in grouped_ports_by_protocol.items():
                if protocol not in watched_addresses[address]:
                    watched_addresses[address][protocol] = set()

                watched_addresses[address][protocol] |= ports

        return watched_addresses

    def get_ports_to_shuffle_by_address_and_protocol(self) -> Dict[str, Dict[str, Set[int]]]:
        ports_to_shuffle = {}

        watched_addresses_by_address_and_protocol = self.get_watched_addresses_by_address_and_protocol()
        all_used_ports_by_protocol = self.get_all_used_ports_by_protocol()

        for address, ignored_ports_by_protocol in watched_addresses_by_address_and_protocol.items():
            if address not in ports_to_shuffle:
                ports_to_shuffle[address] = {}

            for protocol, all_used_ports in all_used_ports_by_protocol.items():
                if protocol not in ports_to_shuffle[address]:
                    ports_to_shuffle[address][protocol] = set()

                if protocol in ignored_ports_by_protocol:
                    ports_to_shuffle[address][protocol] |= (
                        all_used_ports - ignored_ports_by_protocol[protocol])
                else:
                    ports_to_shuffle[address][protocol] |= all_used_ports

        return ports_to_shuffle

    def get_nft_startup_file_content_as_string(self) -> str:
        file_content = self.__read_script_file(
            file_path=self.__nft_startup_script_path)

        return file_content

    def get_nft_address_rules_content_as_string(self) -> str:
        file_content = self.__read_script_file(
            file_path=self.__nft_address_rules_script_path)

        return file_content

    def __get_grouped_ports_by_protocol(self, port_protocol_pair_list) -> Dict[str, Set[int]]:
        grouped_ports = {}

        for port_protocol_pair in port_protocol_pair_list:
            protocol = port_protocol_pair[PROTOCOL]
            port = port_protocol_pair[PORT]

            if(protocol not in grouped_ports):
                grouped_ports[protocol] = set()

            grouped_ports[protocol].add(port)

        return grouped_ports

    def __read_script_file(self, file_path) -> str:
        file_content = ""

        with open(file_path) as file:
            file_content = file.read()

        return file_content
