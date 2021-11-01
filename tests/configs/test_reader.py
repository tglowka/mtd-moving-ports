import unittest

from unittest.mock import patch
from jsonschema.exceptions import ValidationError
from src.configs.reader import ConfigurationReader


class Test_ConfigurationReader(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.invalid_configuration_json = {
            "redis_client_configuration": {
                "host": "127.0.0.1",
                "port": 6379,
                "db": 0,
                "charset": "utf-8",
                "decode_responses": True
            },
            "redis_subscriber_configuration": {
                "subscriber_channel_names": [
                    "test_channel_1",
                    "test_channel_2"
                ]
            },
            "mtd_controller_configuration": {
                "nft_startup_script_path": "/home/tglowka2/Desktop/msc/msc/src/configs/setup/nft_startup.nft",
                "nft_address_rules_script_path": "/home/tglowka2/Desktop/msc/msc/src/configs/setup/nft_address_rules.nft",
                "max_port_number": 1300,
                "watched_addresses": [
                    {
                        "address": "192.168.1.120",
                        "ports_to_ignore": []
                    },
                    {
                        "address": "192.168.1.200",
                        "ports_to_ignore": [
                            {
                                "port": 80,
                                "protocol": "tcp"
                            }
                        ]
                    }
                ]
            }
        }
        self.valid_configuration_json = {
            "redis_client_configuration": {
                "host": "127.0.0.1",
                "port": 6379,
                "db": 0,
                "charset": "utf-8",
                "decode_responses": True
            },
            "redis_subscriber_configuration": {
                "subscriber_channel_names": [
                    "test_channel_1",
                    "test_channel_2"
                ]
            },
            "mtd_controller_configuration": {
                "nft_startup_script_path": "/home/tglowka2/Desktop/msc/msc/src/configs/setup/nft_startup.nft",
                "nft_address_rules_script_path": "/home/tglowka2/Desktop/msc/msc/src/configs/setup/nft_address_rules.nft",
                "max_port_number": 1300,
                "all_used_ports": [
                    {
                        "port": 21,
                        "protocol": "tcp"
                    },
                    {
                        "port": 22,
                        "protocol": "tcp"
                    },
                    {
                        "port": 80,
                        "protocol": "tcp"
                    },
                    {
                        "port": 1250,
                        "protocol": "tcp"
                    },
                    {
                        "port": 1300,
                        "protocol": "tcp"
                    }
                ],
                "watched_addresses": [
                    {
                        "address": "192.168.1.120",
                        "ports_to_ignore": []
                    },
                    {
                        "address": "192.168.1.200",
                        "ports_to_ignore": [
                            {
                                "port": 80,
                                "protocol": "tcp"
                            }
                        ]
                    }
                ]
            }
        }

    def setUp(self):
        self.configuration_reader = ConfigurationReader()

    @patch('src.configs.reader.json')
    def test_read_and_validate_validConfigurationFileNoErrorExpected(self, mock_json):

        # Arrange
        mock_json.load.return_value = self.valid_configuration_json

        # Act
        self.configuration_reader.read_and_validate_configuration_file()

    @patch('src.configs.reader.json')
    def test_read_and_validate_configuration_file_invalidConfigurationFileThrowError(self, mock_json):

        # Arrange
        mock_json.load.return_value = self.invalid_configuration_json

        # Act
        try:
            self.configuration_reader.read_and_validate_configuration_file()
        except ValidationError:
            pass
        else:
            self.fail('ValidationError not raised')

    @patch('src.configs.reader.json')
    def test_get_configuration_json_readAndValidateConfigFileReturnNotEmptyJson(self, mock_json):

        # Arrange
        mock_json.load.return_value = self.valid_configuration_json
        expected_configruation_json = self.valid_configuration_json

        # Act
        self.configuration_reader.read_and_validate_configuration_file()
        actual_configuration_json = self.configuration_reader.get_configuration_json()

        # Assert
        self.assertEqual(actual_configuration_json,
                         expected_configruation_json)

    def test_get_configuration_json_notReadAndValidateConfigFileReturnEmptyJson(self):

        # Arrange
        expected_configuration_json = {}

        # Act
        actual_configuration_json = self.configuration_reader.get_configuration_json()

        # Assert
        self.assertEqual(actual_configuration_json,
                         expected_configuration_json)


if __name__ == '__main__':
    unittest.main()
