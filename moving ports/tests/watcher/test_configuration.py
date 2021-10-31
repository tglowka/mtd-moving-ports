import unittest
from unittest.mock import patch

from src.watcher.configuration import LogfilesWatcherConfiguration


class Test_LogfilesWatcherConfiguration(unittest.TestCase):

    @patch('src.configs.reader.ConfigurationReader')
    def test_check_configuration_objects(self, mock_configuration_reader):
        """
        Checks the logfiles watcher configuration json objects.

        """
        # Arrange
        expected_directory_to_watch = "/test/dir"
        expected_regexes = ["^test*"]
        expected_ignore_regexes = ["^.*test$"]
        expected_ignore_directories = True
        expected_case_sensitive = False
        expected_go_recursively = True

        mock_configuration_reader.get_configuration_json.return_value = {
            "logfiles_watcher_configuration": {
                "directory_to_watch": expected_directory_to_watch,
                "regexes": expected_regexes,
                "ignore_regexes": expected_ignore_regexes,
                "ignore_directories": expected_ignore_directories,
                "case_sensitive": expected_case_sensitive,
                "go_recursively": expected_go_recursively
            }
        }

        logfiles_watcher_configuration = LogfilesWatcherConfiguration(
            configuration_reader=mock_configuration_reader)

        # Act

        actual_directory_to_watch = logfiles_watcher_configuration.directory_to_watch
        actual_regexes = logfiles_watcher_configuration.regexes
        actual_ignore_regexes = logfiles_watcher_configuration.ignore_regexes
        actual_ignore_directories = logfiles_watcher_configuration.ignore_directories
        actual_case_sensitive = logfiles_watcher_configuration.case_sensitive
        actual_go_recursively = logfiles_watcher_configuration.go_recursively

        # Assert
        self.assertEqual(expected_directory_to_watch,
                         actual_directory_to_watch)
        self.assertEqual(actual_regexes, expected_regexes)
        self.assertEqual(actual_ignore_regexes, expected_ignore_regexes)
        self.assertEqual(actual_ignore_directories,
                         expected_ignore_directories)
        self.assertEqual(actual_case_sensitive, expected_case_sensitive)
        self.assertEqual(actual_go_recursively, expected_go_recursively)


if __name__ == '__main__':
    unittest.main()
