import unittest
from unittest.mock import patch

from src.mtd.nftables_controller import NftablesController, NftablesOutputException, NftablesRcException


class Test_NftablesController(unittest.TestCase):

    @patch('nftables.nftables.Nftables')
    @patch('src.mtd.rules_generator.RulesGenerator')
    def test_prepare_nftables_json_1(self, mock_rules_generator, mock_nftables):
        """
        Prepare for valid startup commands and valid address rules. No exception expected
        """
        # Arrange
        valid_nftables_startup_commands = '{"commands": [{"flush": {"ruleset": null}}]}'
        valid_nftables_address_rules = ['''{
            "rules": [
                {
                    "add": {
                        "rule": {
                            "family": "ip",
                            "table": "nat",
                            "chain": "prerouting",
                            "expr": [
                                {
                                    "match": {
                                        "op": "==",
                                        "left": {
                                            "payload": {
                                                "protocol": "ip",
                                                "field": "saddr"
                                            }
                                        },
                                        "right": "{{SOURCE_ADDRESS}}"
                                    }
                                },
                                {
                                    "match": {
                                        "op": "==",
                                        "left": {
                                            "payload": {
                                                "protocol": "{{PROTOCOL}}",
                                                "field": "dport"
                                            }
                                        },
                                        "right": "{{DESTINATION_PORT}}"
                                    }
                                },
                                {
                                    "redirect": {
                                        "port": "{{REDIRECTED_PORT}}"
                                    }
                                }
                            ]
                        }
                    }
                }]}''']

        mock_rules_generator.get_nftables_startup_commands.return_value = valid_nftables_startup_commands
        mock_rules_generator.generate_nftables_address_rules.return_value = valid_nftables_address_rules

        nftables_controller = NftablesController(
            rules_generator=mock_rules_generator, nftables=mock_nftables)
        # Act
        nftables_controller.prepare_nftables_json()
        nftables_controller.prepare_nftables_json()

    @patch('nftables.nftables.Nftables')
    @patch('src.mtd.rules_generator.RulesGenerator')
    def test_prepare_nftables_json_2(self, mock_rules_generator, mock_nftables):
        """
        Prepare for invalid startup commands string. Commands object expected in string. KeyError exception thrown.
        """
        # Arrange
        invalid_nftables_startup_commands = '{"invalid_name": [{"flush": {"ruleset": null}}]}'
        valid_nftables_address_rules = ['''{
            "rules": [
                {
                    "add": {
                        "rule": {
                            "family": "ip",
                            "table": "nat",
                            "chain": "prerouting",
                            "expr": [
                                {
                                    "match": {
                                        "op": "==",
                                        "left": {
                                            "payload": {
                                                "protocol": "ip",
                                                "field": "saddr"
                                            }
                                        },
                                        "right": "{{SOURCE_ADDRESS}}"
                                    }
                                },
                                {
                                    "match": {
                                        "op": "==",
                                        "left": {
                                            "payload": {
                                                "protocol": "{{PROTOCOL}}",
                                                "field": "dport"
                                            }
                                        },
                                        "right": "{{DESTINATION_PORT}}"
                                    }
                                },
                                {
                                    "redirect": {
                                        "port": "{{REDIRECTED_PORT}}"
                                    }
                                }
                            ]
                        }
                    }
                }]}''']

        mock_rules_generator.get_nftables_startup_commands.return_value = invalid_nftables_startup_commands
        mock_rules_generator.generate_nftables_address_rules.return_value = valid_nftables_address_rules

        nftables_controller = NftablesController(
            rules_generator=mock_rules_generator, nftables=mock_nftables)

        # Act
        try:
            nftables_controller.prepare_nftables_json()
        except KeyError:
            pass
        else:
            self.fail('KeyError not raised')

    @patch('nftables.nftables.Nftables')
    @patch('src.mtd.rules_generator.RulesGenerator')
    def test_prepare_nftables_json_3(self, mock_rules_generator, mock_nftables):
        """
        Prepare for invalid address rules list of strings. Rules object expected in string. KeyError exception thrown.
        """
        # Arrange
        valid_nftables_startup_commands = '{"commands": [{"flush": {"ruleset": null}}]}'
        invalid_nftables_address_rules = ['''{
            "invalid_name": [
                {
                    "add": {
                        "rule": {
                            "family": "ip",
                            "table": "nat",
                            "chain": "prerouting",
                            "expr": [
                                {
                                    "match": {
                                        "op": "==",
                                        "left": {
                                            "payload": {
                                                "protocol": "ip",
                                                "field": "saddr"
                                            }
                                        },
                                        "right": "{{SOURCE_ADDRESS}}"
                                    }
                                },
                                {
                                    "match": {
                                        "op": "==",
                                        "left": {
                                            "payload": {
                                                "protocol": "{{PROTOCOL}}",
                                                "field": "dport"
                                            }
                                        },
                                        "right": "{{DESTINATION_PORT}}"
                                    }
                                },
                                {
                                    "redirect": {
                                        "port": "{{REDIRECTED_PORT}}"
                                    }
                                }
                            ]
                        }
                    }
                }]}''']

        mock_rules_generator.get_nftables_startup_commands.return_value = valid_nftables_startup_commands
        mock_rules_generator.generate_nftables_address_rules.return_value = invalid_nftables_address_rules

        nftables_controller = NftablesController(
            rules_generator=mock_rules_generator, nftables=mock_nftables)

        # Act
        try:
            nftables_controller.prepare_nftables_json()
        except KeyError:
            pass
        else:
            self.fail('KeyError not raised')

    @patch('nftables.nftables.Nftables')
    @patch('src.mtd.rules_generator.RulesGenerator')
    def test_apply_rules_1(self, mock_rules_generator, mock_nftables):
        """
        Rules application return retrun code 0 and output as empty string. No exception expected.
        """
        # Arrange
        mock_nftables.json_cmd.return_value = 0, "", None

        nftables_controller = NftablesController(
            rules_generator=mock_rules_generator, nftables=mock_nftables)

        # Act
        nftables_controller.apply_rules()

    @patch('nftables.nftables.Nftables')
    @patch('src.mtd.rules_generator.RulesGenerator')
    def test_apply_rules_2(self, mock_rules_generator, mock_nftables):
        """
        Rules application return retrun code != 0 and output as empty string. NftablesRcException exception thrown.
        """
        # Arrange
        mock_nftables.json_cmd.return_value = 1, "", None

        nftables_controller = NftablesController(
            rules_generator=mock_rules_generator, nftables=mock_nftables)

        # Act
        try:
            nftables_controller.apply_rules()
        except NftablesRcException:
            pass
        else:
            self.fail('NftablesRcException not raised')

    @patch('nftables.nftables.Nftables')
    @patch('src.mtd.rules_generator.RulesGenerator')
    def test_apply_rules_3(self, mock_rules_generator, mock_nftables):
        """
        Rules application return retrun code 0 and output as not empty string. NftablesOutputException exception thrown.
        """
        # Arrange
        mock_nftables.json_cmd.return_value = 0, "not empty", None

        nftables_controller = NftablesController(
            rules_generator=mock_rules_generator, nftables=mock_nftables)

        # Act
        try:
            nftables_controller.apply_rules()
        except NftablesOutputException:
            pass
        else:
            self.fail('NftablesOutputException not raised')


if __name__ == '__main__':
    unittest.main()
