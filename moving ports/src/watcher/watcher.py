import time
import json

from src.redis.pubsub.publisher import RedisPublisher
from src.watcher.configuration import LogfilesWatcherConfiguration
from watchdog.events import RegexMatchingEventHandler
from watchdog.observers import Observer


class LogfilesWatcher:

    def __init__(self,
                 logfiles_watcher_configuration: LogfilesWatcherConfiguration,
                 redis_publisher: RedisPublisher):
        self.__directory_to_watch = logfiles_watcher_configuration.directory_to_watch
        self.__regexes = logfiles_watcher_configuration.regexes
        self.__ignore_regexes = logfiles_watcher_configuration.ignore_regexes
        self.__ignore_directories = logfiles_watcher_configuration.ignore_directories
        self.__case_sensitive = logfiles_watcher_configuration.case_sensitive
        self.__go_recursively = logfiles_watcher_configuration.go_recursively
        self.__event_handler = None
        self.__observer = None
        self.__redis_publisher = redis_publisher

    def __setup_event_handler(self):
        self.__event_handler = RegexMatchingEventHandler(
            regexes=self.__regexes,
            ignore_regexes=self.__ignore_regexes,
            ignore_directories=self.__ignore_directories,
            case_sensitive=self.__case_sensitive)

        self.__event_handler.on_modified = self.__on_modified

    def __setup_observer(self):
        self.__observer = Observer()
        self.__observer.schedule(event_handler=self.__event_handler,
                                 path=self.__directory_to_watch,
                                 recursive=self.__go_recursively)

    def start_observer(self):
        self.__setup_event_handler()
        self.__setup_observer()

        try:
            self.__observer.start()
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.__observer.stop()
            self.__observer.join()

    def __on_modified(self, event):
        message_timestamp = time.time()
        local_time = time.ctime(message_timestamp)

        self.__redis_publisher.publish(json.dumps(
            {"message": f"Modified, {event.src_path}", "local time": local_time}))
