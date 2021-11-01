import unittest
from unittest.mock import patch

from src.redis.pubsub.configuration import RedisPubSubConfiguration


class Test_RedisPubSubConfiguration(unittest.TestCase):

    @patch('src.configs.reader.ConfigurationReader')
    def test_check_configuration_objects(self, mock_configuration_reader):
        """
        Checks the redis pubsub configuration json objects.

        """
        # Arrange
        expected_subscriber_channel_names = [
            "test_channel_1",
            "test_channel_2"
        ]
        expected_publisher_channel_name = "test_channel_1"

        mock_configuration_reader.get_configuration_json.return_value = {
            "redis_pub_sub_configuration": {
                "subscriber_channel_names": expected_subscriber_channel_names,
                "publisher_channel_name": expected_publisher_channel_name
            }
        }

        redis_pubsub_configuration = RedisPubSubConfiguration(
            configuration_reader=mock_configuration_reader)

        # Act
        actual_subscriber_channel_names = redis_pubsub_configuration.subscriber_channel_names
        actual_publisher_channel_name = redis_pubsub_configuration.publisher_channel_name

        # Assert
        self.assertEqual(actual_subscriber_channel_names,
                         expected_subscriber_channel_names)
        self.assertEqual(actual_publisher_channel_name,
                         expected_publisher_channel_name)


if __name__ == '__main__':
    unittest.main()
