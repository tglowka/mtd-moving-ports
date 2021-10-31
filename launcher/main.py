import sys
import time
import argparse
import secrets
import datetime

parser = argparse.ArgumentParser()

parser.add_argument("--lower_boundary_seconds", "-l",
                    help="set the range lower boundary in seconds", type=int)
parser.add_argument("--uppper_boundary_seconds", "-u",
                    help="set the range upper boundary in seconds", type=int)
parser.add_argument("--file_path", "-f",
                    help="set the path to the file to modify")

args = parser.parse_args()

lower_boundary_seconds = args.lower_boundary_seconds
uppper_boundary_seconds = args.uppper_boundary_seconds

sleep_range = uppper_boundary_seconds - lower_boundary_seconds + 1

file_path = args.file_path

while(True):

    sleep_time_seconds = secrets.randbelow(sleep_range)
    sleep_time_seconds += lower_boundary_seconds

    time.sleep(sleep_time_seconds)

    log_message = "Proactive mtd launcher execution. Time: " + \
        datetime.datetime.utcnow().strftime("%d %m %Y %H:%M:%S")

    file = open(file_path, "a")
    file.write(log_message)
    file.write("\n")
    file.close()
