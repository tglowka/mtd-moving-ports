import json

from nftables.nftables import Nftables
from src.mtd.rules_generator import RulesGenerator


COMMANDS = "commands"
RULES = "rules"
NFTABLES = "nftables"


class NftablesController:
    def __init__(self, rules_generator: RulesGenerator, nftables: Nftables) -> None:
        self.__rules_generator = rules_generator
        self.__nftables = nftables

        self.__nftables_startup_commands = self.__rules_generator.get_nftables_startup_commands()
        self.__nftables_address_rules = []

        self.__nftables_json = {NFTABLES: []}

    def prepare_nftables_json(self) -> None:
        self.__nftables_address_rules = self.__rules_generator.generate_nftables_address_rules()

        self.__cleanup_nftables_json()

        self.__add_startup_commands_to_json()
        self.__add_address_rules_to_json()
        self.__validate_nftables_json()

    def apply_rules(self) -> None:
        rc, output, error = self.__nftables.json_cmd(self.__nftables_json)
        self.__validate_nftables_output(rc, output, error)

    def __cleanup_nftables_json(self):
        self.__nftables_json[NFTABLES] = []

    def __add_startup_commands_to_json(self) -> None:
        parsed_commands = json.loads(self.__nftables_startup_commands)
        self.__nftables_json[NFTABLES].extend(parsed_commands[COMMANDS])

    def __add_address_rules_to_json(self) -> None:
        for rules in self.__nftables_address_rules:
            parsed_rules = json.loads(rules)
            self.__nftables_json[NFTABLES].extend(parsed_rules[RULES])

    def __validate_nftables_json(self) -> None:
        self.__nftables.json_validate(self.__nftables_json)

    def __validate_nftables_output(self, rc, output, error) -> None:
        if rc != 0:
            print(f"Validate nftables output - error: {error}", flush=True)
            raise NftablesRcException()

        if len(output) != 0:
            print(f"Validate nftables output - error: {output}", flush=True)
            raise NftablesOutputException()


class NftablesRcException(Exception):
    pass


class NftablesOutputException(Exception):
    pass
