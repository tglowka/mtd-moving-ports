import unittest
from unittest.mock import mock_open, patch

from src.mtd.rules_generator import NFT_DESTINATION_PORT_TOKEN, NFT_PROTOCOL_TOKEN, NFT_REDIRECTED_PORT_TOKEN, NFT_SOURCE_ADDRESS_TOKEN

from src.configs.reader import ConfigurationReader
from src.mtd.configuration import MtdControllerConfiguration
from src.mtd.rules_generator import RulesGenerator

NFT_ADDRESS_RULES = "add rule ip nat prerouting ip saddr {{SOURCE_ADDRESS}} {{PROTOCOL}} dport \"{{DESTINATION_PORT}}\" redirect to :\"{{REDIRECTED_PORT}}\""


class Test_RulesGenerator(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="startup\nfile\ncontent")
    @patch('src.configs.reader.ConfigurationReader')
    def test_get_nftables_startup_commands(self, mock_configuration_reader, mock_open):
        """
        Returns nft_startup_commands as string.
        """
        # Arrange
        mock_configuration_reader.get_configuration_json.return_value = {
            "mtd_controller_configuration": {
                "nft_startup_script_path": "",
                "nft_address_rules_script_path": "",
                "all_used_ports": [],
                "max_port_number": "",
                "watched_addresses": []
            }
        }

        mtd_controller_configuration = MtdControllerConfiguration(
            configuration_reader=mock_configuration_reader)

        rules_generator = RulesGenerator(
            mtd_controller_configuration=mtd_controller_configuration)

        # Act
        actual_nft_startup_commands = rules_generator.get_nftables_startup_commands()

        # Assert
        self.assertEqual("startup\nfile\ncontent",
                         actual_nft_startup_commands)

    @patch("src.mtd.rules_generator.secrets")
    @patch("builtins.open", new_callable=mock_open, read_data=NFT_ADDRESS_RULES)
    @patch("src.configs.reader.ConfigurationReader")
    def test_generate_nftables_address_rules(self, mock_configuration_reader, mock_open, mock_secrets):
        """
        Returns nft_address_rules as 3 elements list.
        """
        # Arrange
        expected_nft_address_rules = []

        # Generate all combinations of address,destination_port,redirected_port.
        # That's because behind the scene sets and dicts are used hence the usage order is unknown.
        for destination_port in [22, 33]:
            for redirected_port in [1, 2, 3]:
                rule = NFT_ADDRESS_RULES.replace(f"{NFT_SOURCE_ADDRESS_TOKEN}", "192.168.1.120") \
                    .replace(f"{NFT_DESTINATION_PORT_TOKEN}", str(destination_port)) \
                    .replace(f"{NFT_REDIRECTED_PORT_TOKEN}", str(redirected_port)) \
                    .replace(f"{NFT_PROTOCOL_TOKEN}", "tcp")
                expected_nft_address_rules.append(rule)

        for destination_port in [33]:
            for redirected_port in [1, 2, 3]:
                rule = NFT_ADDRESS_RULES.replace(f"{NFT_SOURCE_ADDRESS_TOKEN}", "192.168.1.200") \
                    .replace(f"{NFT_DESTINATION_PORT_TOKEN}", str(destination_port)) \
                    .replace(f"{NFT_REDIRECTED_PORT_TOKEN}", str(redirected_port)) \
                    .replace(f"{NFT_PROTOCOL_TOKEN}", "tcp")
                expected_nft_address_rules.append(rule)

        all_used_ports = [{"port": 22, "protocol": "tcp"},
                          {"port": 33, "protocol": "tcp"}]

        watched_addresses = [
            {
                "address": "192.168.1.120",
                "ports_to_ignore": []
            },
            {
                "address": "192.168.1.200",
                "ports_to_ignore": [
                    {"port": 22, "protocol": "tcp"}]
            }
        ]

        mock_configuration_reader.get_configuration_json.return_value = {
            "mtd_controller_configuration": {
                "nft_startup_script_path": "",
                "nft_address_rules_script_path": "",
                "all_used_ports": all_used_ports,
                "max_port_number": 1300,
                "watched_addresses": watched_addresses
            }
        }

        mock_secrets.randbelow.side_effect = [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

        mtd_controller_configuration = MtdControllerConfiguration(
            configuration_reader=mock_configuration_reader)

        rules_generator = RulesGenerator(
            mtd_controller_configuration=mtd_controller_configuration)

        # Act
        actual_nft_adress_rules = rules_generator.generate_nftables_address_rules()

        # Assert

        # convert previously generated combination, i.e. expected_nft_address_rules,
        # and actual_nft_adress_rules to sets to easily find out whether
        # actual_nft_adress_rules elements are in expected_nft_address_rules
        intersection = set.intersection(
            set(expected_nft_address_rules), set(actual_nft_adress_rules))
        self.assertEqual(3,
                         len(intersection))


if __name__ == '__main__':
    unittest.main()
