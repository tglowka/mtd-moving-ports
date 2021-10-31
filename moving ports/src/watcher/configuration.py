from src.configs.reader import ConfigurationReader

LOGFILES_WATCHER_CONFIGURATION = "logfiles_watcher_configuration"
DIRECTORY_TO_WATCH = "directory_to_watch"
REGEXES = "regexes"
IGNORE_REGEXES = "ignore_regexes"
IGNORE_DIRECTORIES = "ignore_directories"
CASE_SENSITIVE = "case_sensitive"
GO_RECURSIVELY = "go_recursively"


class LogfilesWatcherConfiguration:

    def __init__(self,
                 configuration_reader: ConfigurationReader):
        self.__logfiles_watcher_configuration = configuration_reader.get_configuration_json()[
            LOGFILES_WATCHER_CONFIGURATION]
        self.directory_to_watch = self.__logfiles_watcher_configuration[DIRECTORY_TO_WATCH]
        self.regexes = self.__logfiles_watcher_configuration[REGEXES]
        self.ignore_regexes = self.__logfiles_watcher_configuration[IGNORE_REGEXES]
        self.ignore_directories = self.__logfiles_watcher_configuration[IGNORE_DIRECTORIES]
        self.case_sensitive = self.__logfiles_watcher_configuration[CASE_SENSITIVE]
        self.go_recursively = self.__logfiles_watcher_configuration[GO_RECURSIVELY]
