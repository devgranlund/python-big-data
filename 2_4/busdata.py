import sys
import logging
import urllib.request
import time

# Author: tuomas.granlund@solita.fi
# 12.11.2017


def generate_bus_data(read_interval_in_seconds, time_to_read_in_seconds):
    counter = 0
    while counter < time_to_read_in_seconds:
        d = urllib.request.urlopen('http://data.itsfactory.fi/journeys/api/1/vehicle-activity').read()
        s = str(d, "utf-8")
        if counter > 0:
            logging.debug(',')
        logging.debug(s)
        time.sleep(read_interval_in_seconds)
        counter = counter + read_interval_in_seconds


if __name__ == '__main__':
    logging.basicConfig(filename=sys.argv[1], format='%(message)s', level=logging.DEBUG)
    logging.debug('[')
    generate_bus_data(int(sys.argv[2]), int(sys.argv[3]))
    logging.debug(']')
