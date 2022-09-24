from typing import Dict, Set, List
from src.configs.reader import ConfigReader


class NftablesConfig:

    def __init__(self, config_reader: ConfigReader) -> None:
        self.__NFTABLES_SERVICE_CONFIGURATION = "nftables_service_configuration"
        self.__TCP_PORTS = "tcp_ports"
        self.__WATCHED_ADDRESSES = "watched_addresses"
        self.__NFT_STARTUP_SCRIPT_PATH = "nft_startup_script_path"
        self.__NFT_ADDRESS_RULES_SCRIPT_PATH = "nft_address_rules_script_path"
        self.__MAX_PORT_NUMBER = "max_port_number"
        self.__IP = "ip"
        self.__TCP_IGNORE = "tcp_ignore"

        config = config_reader.get_config()
        self.__nftables_config = config[self.__NFTABLES_SERVICE_CONFIGURATION]

    def get_max_port_numer(self) -> int:
        return self.__nftables_config[self.__MAX_PORT_NUMBER]

    def get_tcp_ports(self) -> Set[int]:
        return set(self.__nftables_config[self.__TCP_PORTS])

    def get_watched_addresses_by_address(self) -> Dict[str, Set[int]]:
        watched_addresses = {}
        addresses = self.__nftables_config[self.__WATCHED_ADDRESSES]

        for address in addresses:
            ip = address[self.__IP]
            ports_to_ignore = set(address[self.__TCP_IGNORE])
            watched_addresses[ip] = ports_to_ignore

        return watched_addresses

    def get_ports_to_shuffle_by_address(self) -> Dict[str, Set[int]]:
        results = {}

        watched_addresses = self.get_watched_addresses_by_address()
        tcp_ports = self.get_tcp_ports()

        for ip, ports_to_ignore in watched_addresses:
            results[ip] = tcp_ports - ports_to_ignore

        return results

    def get_nft_startup_content(self) -> str:
        return self.__read_file_as_string(self.__nftables_config[self.__NFT_STARTUP_SCRIPT_PATH])

    def get_nft_address_rules_content(self) -> str:
        return self.__read_file_as_string(self.__nftables_config[self.__NFT_ADDRESS_RULES_SCRIPT_PATH])

    def __read_file_as_string(self, file_path) -> str:
        file_content = ""

        with open(file_path) as file:
            file_content = file.read()

        return file_content


class RedisConnectionConfig:
    def __init__(self, config_reader: ConfigReader):

        self.__REDIS_CONNECTION_CONFIGURATION = "redis_connection_configuration"
        self.__HOST = "host"
        self.__PORT = "port"
        self.__DB = "db"
        self.__CHARSET = "charset"
        self.__DECODE_RESPONSES = "decode_responses"

        config = config_reader.get_config()
        self.__redis_config = config[self.__REDIS_CONNECTION_CONFIGURATION]

    def get_host(self) -> str:
        return self.__redis_config[self.__HOST]

    def get_port(self) -> int:
        return self.__redis_config[self.__PORT]

    def get_db(self) -> int:
        return self.__redis_config[self.__DB]

    def get_charset(self) -> str:
        return self.__redis_config[self.__CHARSET]

    def get_decode_responses(self) -> bool:
        return self.__redis_config[self.__DECODE_RESPONSES]


class RedisSubscriberConfig:

    def __init__(self, config_reader: ConfigReader):

        self.__REDIS_SUBSCRIBER_CONFIGURATION = "redis_subscriber_configuration"
        self.__SUBSCRIBER_CHANNEL_NAMES = "subscriber_channel_names"

        config = config_reader.get_config()
        self.__redis_config = config[self.__REDIS_SUBSCRIBER_CONFIGURATION]

    def get_subscriber_channel_names(self) -> List[str]:
        return self.__redis_config[self.__SUBSCRIBER_CHANNEL_NAMES]
