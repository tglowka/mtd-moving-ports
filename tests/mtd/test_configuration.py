import unittest
from unittest import mock
from unittest.mock import mock_open, patch
from configs.configs import MtdControllerConfiguration


class Test_MtdControllerConfiguration(unittest.TestCase):

    @patch('src.configs.reader.ConfigurationReader')
    def test_get_max_port_numer(self, mock_configuration_reader):
        """
        Returns max_port_number read from configuration file.
        """
        # Arrange
        expected_max_port_number = 1300
        mock_configuration_reader.get_configuration_json.return_value = {
            "mtd_controller_configuration": {
                "nft_startup_script_path": "",
                "nft_address_rules_script_path": "",
                "all_used_ports": [],
                "max_port_number": expected_max_port_number,
                "watched_addresses": []
            }
        }

        mtd_controller_configuration = MtdControllerConfiguration(
            configuration_reader=mock_configuration_reader)

        # Act
        actual_max_port_number = mtd_controller_configuration.get_max_port_numer()

        # Assert
        self.assertEqual(actual_max_port_number, expected_max_port_number)

    @patch('src.configs.reader.ConfigurationReader')
    def test_get_all_used_ports_by_protocol(self, mock_configuration_reader):
        """
        Returns port sets grouped by protocol from all_used_ports read from configuration file.
        """
        # Arrange
        expected_all_used_ports_by_protocol = {
            "tcp": {21, 22},
            "udp": {33}
        }

        all_used_ports = [
            {"port": 21, "protocol": "tcp"},
            {"port": 33, "protocol": "udp"},
            {"port": 22, "protocol": "tcp"}
        ]
        mock_configuration_reader.get_configuration_json.return_value = {
            "mtd_controller_configuration": {
                "nft_startup_script_path": "",
                "nft_address_rules_script_path": "",
                "all_used_ports": all_used_ports,
                "max_port_number": "",
                "watched_addresses": ""
            }
        }

        mtd_controller_configuration = MtdControllerConfiguration(
            configuration_reader=mock_configuration_reader)

        # Act
        actual_all_used_ports_by_protocol = mtd_controller_configuration.get_all_used_ports_by_protocol()

        # Assert
        self.assertEqual(actual_all_used_ports_by_protocol,
                         expected_all_used_ports_by_protocol)

    @patch('src.configs.reader.ConfigurationReader')
    def test_get_watched_addresses_by_address_and_protocol(self, mock_configuration_reader):
        """
        Returns port sets gruped by address and protocol from watched_addresses read from configuration file.
        """
        # Arrange
        expected_watched_addresses_by_address_protocol = {
            "192.168.1.120": {
                "udp": {33, 44},
                "tcp": {33}
            },
            "192.168.1.200": {
                "tcp": {21, 22},
                "udp": {333}
            }
        }

        watched_addresses = [
            {
                "address": "192.168.1.120",
                "ports_to_ignore": [
                    {"port": 33, "protocol": "udp"},
                    {"port": 33, "protocol": "tcp"}]
            },
            {
                "address": "192.168.1.200",
                "ports_to_ignore": [
                    {"port": 21, "protocol": "tcp"},
                    {"port": 22, "protocol": "tcp"},
                    {"port": 333, "protocol": "udp"}]
            },
            {
                "address": "192.168.1.120",
                "ports_to_ignore": [
                    {"port": 33, "protocol": "udp"},
                    {"port": 44, "protocol": "udp"}]
            },
        ]
        mock_configuration_reader.get_configuration_json.return_value = {
            "mtd_controller_configuration": {
                "nft_startup_script_path": "",
                "nft_address_rules_script_path": "",
                "all_used_ports": [],
                "max_port_number": "",
                "watched_addresses": watched_addresses
            }
        }

        mtd_controller_configuration = MtdControllerConfiguration(
            configuration_reader=mock_configuration_reader)

        # Act
        actual_watched_addresses_by_address_protocol = mtd_controller_configuration.get_watched_addresses_by_address_and_protocol()

        # Assert
        self.assertEqual(actual_watched_addresses_by_address_protocol,
                         expected_watched_addresses_by_address_protocol)

    @patch('src.configs.reader.ConfigurationReader')
    def test_get_ports_to_shuffle_by_address_and_protocol_1(self, mock_configuration_reader):
        """
        Returns port to shuffle sets gruped by address and protocol from all_used_ports and watched_addresses read from configuration file. watched_address has one protocol type, all_used_ports has two.
        """
        expected_ports_to_shuffle_by_address_and_protocol = {
            "192.168.1.120": {
                "tcp": {21, 22, 443, 8080},
                "udp": {33, 44, 55, 333},
            },
            "192.168.1.200": {
                "tcp": {33, 443, 8080},
                "udp": {33, 44, 55}
            }
        }

        all_used_ports = [{"port": 21, "protocol": "tcp"},
                          {"port": 22, "protocol": "tcp"},
                          {"port": 33, "protocol": "tcp"},
                          {"port": 443, "protocol": "tcp"},
                          {"port": 8080, "protocol": "tcp"},
                          {"port": 33, "protocol": "udp"},
                          {"port": 44, "protocol": "udp"},
                          {"port": 55, "protocol": "udp"},
                          {"port": 333, "protocol": "udp"}]

        watched_addresses = [
            {
                "address": "192.168.1.120",
                "ports_to_ignore": [
                    {"port": 33, "protocol": "tcp"}
                ]
            },
            {
                "address": "192.168.1.200",
                "ports_to_ignore": [
                    {"port": 21, "protocol": "tcp"},
                    {"port": 22, "protocol": "tcp"},
                    {"port": 333, "protocol": "udp"}]
            }
        ]

        mock_configuration_reader.get_configuration_json.return_value = {
            "mtd_controller_configuration": {
                "nft_startup_script_path": "",
                "nft_address_rules_script_path": "",
                "all_used_ports": all_used_ports,
                "max_port_number": "",
                "watched_addresses": watched_addresses
            }
        }

        mtd_controller_configuration = MtdControllerConfiguration(
            configuration_reader=mock_configuration_reader)

        # Act
        actual_ports_to_shuffle_by_address_and_protocol = mtd_controller_configuration.get_ports_to_shuffle_by_address_and_protocol()

        # Assert
        self.assertEqual(actual_ports_to_shuffle_by_address_and_protocol,
                         expected_ports_to_shuffle_by_address_and_protocol)

    @patch('src.configs.reader.ConfigurationReader')
    def test_get_ports_to_shuffle_by_address_and_protocol_3(self, mock_configuration_reader):
        """
        Returns port to shuffle sets gruped by address and protocol from all_used_ports and watched_addresses read from configuration file. watched_address has no ports_to_ignore.
        """
        expected_ports_to_shuffle_by_address_and_protocol = {
            "192.168.1.120": {
                "tcp": {21, 22, 33, 443, 8080},
                "udp": {33, 44, 55, 333},
            },
            "192.168.1.200": {
                "tcp": {33, 443, 8080},
                "udp": {33, 44, 55}
            }
        }

        all_used_ports = [{"port": 21, "protocol": "tcp"},
                          {"port": 22, "protocol": "tcp"},
                          {"port": 33, "protocol": "tcp"},
                          {"port": 443, "protocol": "tcp"},
                          {"port": 8080, "protocol": "tcp"},
                          {"port": 33, "protocol": "udp"},
                          {"port": 44, "protocol": "udp"},
                          {"port": 55, "protocol": "udp"},
                          {"port": 333, "protocol": "udp"}]

        watched_addresses = [
            {
                "address": "192.168.1.120",
                "ports_to_ignore": []
            },
            {
                "address": "192.168.1.200",
                "ports_to_ignore": [
                    {"port": 21, "protocol": "tcp"},
                    {"port": 22, "protocol": "tcp"},
                    {"port": 333, "protocol": "udp"}]
            }
        ]

        mock_configuration_reader.get_configuration_json.return_value = {
            "mtd_controller_configuration": {
                "nft_startup_script_path": "",
                "nft_address_rules_script_path": "",
                "all_used_ports": all_used_ports,
                "max_port_number": "",
                "watched_addresses": watched_addresses
            }
        }

        mtd_controller_configuration = MtdControllerConfiguration(
            configuration_reader=mock_configuration_reader)

        # Act
        actual_ports_to_shuffle_by_address_and_protocol = mtd_controller_configuration.get_ports_to_shuffle_by_address_and_protocol()

        # Assert
        self.assertEqual(actual_ports_to_shuffle_by_address_and_protocol,
                         expected_ports_to_shuffle_by_address_and_protocol)

    @patch('src.configs.reader.ConfigurationReader')
    def test_get_ports_to_shuffle_by_address_and_protocol_2(self, mock_configuration_reader):
        """
        Returns port to shuffle sets gruped by address and protocol from all_used_ports and watched_addresses read from configuration file. Duplicated watched_address.
        """
        expected_ports_to_shuffle_by_address_and_protocol = {
            "192.168.1.120": {
                "tcp": {21, 22, 443, 8080},
                "udp": {55, 333},
            },
            "192.168.1.200": {
                "tcp": {33, 443, 8080},
                "udp": {33, 44, 55}
            }
        }

        all_used_ports = [{"port": 21, "protocol": "tcp"},
                          {"port": 22, "protocol": "tcp"},
                          {"port": 33, "protocol": "tcp"},
                          {"port": 443, "protocol": "tcp"},
                          {"port": 8080, "protocol": "tcp"},
                          {"port": 33, "protocol": "udp"},
                          {"port": 44, "protocol": "udp"},
                          {"port": 55, "protocol": "udp"},
                          {"port": 333, "protocol": "udp"}]

        watched_addresses = [
            {
                "address": "192.168.1.120",
                "ports_to_ignore": [
                    {"port": 33, "protocol": "udp"},
                    {"port": 33, "protocol": "tcp"}
                ]
            },
            {
                "address": "192.168.1.200",
                "ports_to_ignore": [
                    {"port": 21, "protocol": "tcp"},
                    {"port": 22, "protocol": "tcp"},
                    {"port": 333, "protocol": "udp"}]
            },
            {
                "address": "192.168.1.120",
                "ports_to_ignore": [
                    {"port": 33, "protocol": "udp"},
                    {"port": 44, "protocol": "udp"}]
            },
        ]

        mock_configuration_reader.get_configuration_json.return_value = {
            "mtd_controller_configuration": {
                "nft_startup_script_path": "",
                "nft_address_rules_script_path": "",
                "all_used_ports": all_used_ports,
                "max_port_number": "",
                "watched_addresses": watched_addresses
            }
        }

        mtd_controller_configuration = MtdControllerConfiguration(
            configuration_reader=mock_configuration_reader)

        # Act
        actual_ports_to_shuffle_by_address_and_protocol = mtd_controller_configuration.get_ports_to_shuffle_by_address_and_protocol()

        # Assert
        self.assertEqual(actual_ports_to_shuffle_by_address_and_protocol,
                         expected_ports_to_shuffle_by_address_and_protocol)

    @patch("builtins.open", new_callable=mock_open, read_data="nft file content1")
    @patch('src.configs.reader.ConfigurationReader')
    def test_get_nft_startup_file_content_as_string(self, mock_configuration_reader, mock_open):
        """
        Returns file content as string from nft_startup_script_path read from configuration file.
        """
        # Arrange
        expected_nft_startup_script_path = "/test/nft_startup_script_path"
        mock_configuration_reader.get_configuration_json.return_value = {
            "mtd_controller_configuration": {
                "nft_startup_script_path": expected_nft_startup_script_path,
                "nft_address_rules_script_path": "",
                "all_used_ports": [],
                "max_port_number": "",
                "watched_addresses": []
            }
        }

        mtd_controller_configuration = MtdControllerConfiguration(
            configuration_reader=mock_configuration_reader)

        # Act
        actual_nft_startup_file_content_as_string = mtd_controller_configuration.get_nft_startup_file_content_as_string()

        # Assert
        self.assertEqual(actual_nft_startup_file_content_as_string,
                         "nft file content1")
        mock_open.assert_called_with(expected_nft_startup_script_path)

    @patch("builtins.open", new_callable=mock_open, read_data="nft file content2")
    @patch('src.configs.reader.ConfigurationReader')
    def test_get_nft_address_rules_content_as_string(self, mock_configuration_reader, mock_open):
        """
        Returns file content as string from nft_address_rules_script_path read from configuration file.
        """
        # Arrange
        expected_nft_address_rules_script_path = "/test/nft_address_rules_script_path"

        mock_configuration_reader.get_configuration_json.return_value = {
            "mtd_controller_configuration": {
                "nft_startup_script_path": expected_nft_address_rules_script_path,
                "nft_address_rules_script_path": "",
                "all_used_ports": [],
                "max_port_number": "",
                "watched_addresses": []
            }
        }

        mtd_controller_configuration = MtdControllerConfiguration(
            configuration_reader=mock_configuration_reader)
        # Act
        actual_nft_startup_file_content_as_string = mtd_controller_configuration.get_nft_startup_file_content_as_string()

        # Assert
        self.assertEqual(actual_nft_startup_file_content_as_string,
                         "nft file content2")
        mock_open.assert_called_with(expected_nft_address_rules_script_path)


if __name__ == '__main__':
    unittest.main()
