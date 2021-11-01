import time
import argparse
import secrets
import datetime
import redis

parser = argparse.ArgumentParser()

parser.add_argument("--lower_boundary_seconds", "-l",
                    help="set the range lower boundary in seconds", type=int)
parser.add_argument("--uppper_boundary_seconds", "-u",
                    help="set the range upper boundary in seconds", type=int)
parser.add_argument("--file_path", "-f",
                    help="set the path to the file to modify")

args = parser.parse_args()

redis_connection = redis.Redis(host="127.0.0.1",
                               port=6379,
                               db=0,
                               charset="utf-8",
                               decode_responses=True)


def main():
    lower_boundary_seconds = args.lower_boundary_seconds
    uppper_boundary_seconds = args.uppper_boundary_seconds

    sleep_range = uppper_boundary_seconds - lower_boundary_seconds + 1

    while(True):

        sleep_time_seconds = secrets.randbelow(sleep_range)
        sleep_time_seconds += lower_boundary_seconds

        time.sleep(sleep_time_seconds)

        message = "Launcher execution. Time: " + \
            datetime.datetime.utcnow().strftime("%d %m %Y %H:%M:%S")

        publish(message)


def publish(self, message):
    self.__redis_connection.publish(self.__channel, message)
    print(f"Publisher: {message}", flush=True)


if __name__ == "__main__":
    main()
