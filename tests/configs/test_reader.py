import unittest

from unittest.mock import patch
from jsonschema.exceptions import ValidationError
from src.main import SCHEMA_PATH
from src.configs.reader import ConfigReader


class Test_ConfigReader(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.invalid_configuration_json = {
            "redis_connection_configuration": {
                "host": "127.0.0.1",
                "port": 6379,
                "db": 0,
                "charset": "utf-8",
                "decode_responses": True
            },
            "redis_subscriber_configuration": {
                "subscriber_channel_names": ["test_channel_1", "test_channel_2"]
            },
            "nftables_service_configuration": {
                "nft_startup_script_path": "./src/configs/setup/nft_startup_commands.json",
                "nft_address_rules_script_path": "./src/configs/setup/nft_address_rules.json",
                "max_port_number": 1050,
                "tcp_ports": [80, 22],
                "XXXXXXXXXXXXXXXXXXXXXXXXXXX": [
                    {
                        "ip": "192.168.23.130",
                        "tcp_ignore": [80]
                    }
                ]
            }
        }

        self.valid_configuration_json = {
            "redis_connection_configuration": {
                "host": "127.0.0.1",
                "port": 6379,
                "db": 0,
                "charset": "utf-8",
                "decode_responses": True
            },
            "redis_subscriber_configuration": {
                "subscriber_channel_names": ["test_channel_1", "test_channel_2"]
            },
            "nftables_service_configuration": {
                "nft_startup_script_path": "./src/configs/setup/nft_startup_commands.json",
                "nft_address_rules_script_path": "./src/configs/setup/nft_address_rules.json",
                "max_port_number": 1050,
                "tcp_ports": [80, 22],
                "watched_addresses": [
                    {
                        "ip": "192.168.23.130",
                        "tcp_ignore": [80]
                    }
                ]
            }
        }

    def test_read_and_validate_configuration_file_invalidConfigurationFileThrowError(self):

        # Arrange
        # mock_json.load.return_value = self.invalid_configuration_json

        # Act
        try:
            ConfigReader(
                "./tests/configs/invalid_configuration.json", SCHEMA_PATH)
        except ValidationError:
            pass
        else:
            self.fail('ValidationError not raised')

    def test_get_configuration_json_readAndValidateConfigFileReturnNotEmptyJson(self):

        # Arrange
        expected = self.valid_configuration_json

        # Act
        config = ConfigReader(
            "./tests/configs/valid_configuration.json", SCHEMA_PATH)
        actual = config.get_config()

        # Assert
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
