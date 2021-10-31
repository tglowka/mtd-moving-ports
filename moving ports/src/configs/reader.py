import json
from typing import Dict
import jsonschema

CONFIGURATION_FILE_PATH = "./src/configs/setup/configuration.json"
CONFIGURATION_SCHEMA_FILE_PATH = "./src/configs/setup/configuration_schema.json"


class ConfigurationReader:

    def __init__(self) -> None:
        self.__configuration_json = {}
        self.__configuration_schema_json = {}

        self.__read_configuration_schema_file()

    def get_configuration_json(self) -> Dict:
        return self.__configuration_json

    def read_and_validate_configuration_file(self) -> None:
        with open(CONFIGURATION_FILE_PATH) as file:
            self.__configuration_json = json.load(file)

        self.__validate_configuration_json()

    def __read_configuration_schema_file(self) -> None:
        with open(CONFIGURATION_SCHEMA_FILE_PATH) as file:
            self.__configuration_schema_json = json.load(file)

    def __validate_configuration_json(self) -> None:
        jsonschema.validate(instance=self.__configuration_json,
                            schema=self.__configuration_schema_json)
