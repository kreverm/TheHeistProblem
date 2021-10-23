import re
import constants
import utils
import argparse
from operator import itemgetter

parser = argparse.ArgumentParser(description='Heist planner program')
parser.add_argument('-p', '--path', help=f"Path to log file. Default: {constants.SHIFT_LOG_PATH}", required=False,
                    default=constants.SHIFT_LOG_PATH)
args = vars(parser.parse_args())


class HeistPlanner:
    """
    Plans perfect heist time - gets a log of shifts, and calculates which guard slept them most and in which minute
    he is most likely to fall asleep
    """
    def __init__(self):
        self._log_path = args['path']
        self.__log_lines = None

    def __str__(self):
        return f"Log lines are: {self.__log_lines}"

    @property
    def log_path(self):
        return self._log_path

    @log_path.setter
    def log_path(self, path):
        self._log_path = path

    def read_log(self):
        """
        Uses context manager to open log file
        :return:
        """
        with utils.FileManager(self.log_path, 'r') as f:
            self.__log_lines = f.readlines()

    def parse_log(self):
        """
        Parses log content into a dictionary
        :rtype: dict
        :return: dict of {guard: time_slept}, dict of {guard: {minute1: time_slept_in_minute1, ...,
        minuteN: time_slept_minute_N}}
        """

        sorted_lines = sorted(self.__log_lines)
        total_minutes_slept_dict = {}
        sleep_frequency_dict = {}

        for line in sorted_lines:
            # Get time in minutes of each line
            time_in_minutes = int(re.search(constants.MINUTE_PATTERN, line).group(1))

            # If Guard in line - extract guard number
            if "Guard" in line:
                guard_number = int(re.search(constants.GUARD_PATTERN, line).group(1))

            # If falls asleep in line - extract time when felt asleep
            if "falls asleep" in line:
                start_sleeping = time_in_minutes

            # If wakes up in line - extract when finished sleeping
            if "wakes up" in line:
                stop_sleeping = time_in_minutes

                # Create two dicts - one with total time slept by each guard, second with sleeping
                # frequency every minute
                for i in range(start_sleeping, stop_sleeping):

                    # Initialize values of each dict if key doesnt exist
                    if guard_number not in total_minutes_slept_dict:
                        total_minutes_slept_dict[guard_number] = 0
                        sleep_frequency_dict[guard_number] = {}
                        sleep_frequency_dict[guard_number][i] = 0

                    if i not in sleep_frequency_dict[guard_number]:
                        sleep_frequency_dict[guard_number][i] = 0

                    total_minutes_slept_dict[guard_number] += 1
                    sleep_frequency_dict[guard_number][i] += 1

        return total_minutes_slept_dict, sleep_frequency_dict

    def run(self):
        key = itemgetter(1)

        time_slept, frequency = self.parse_log()
        # Find which guard slept the most
        max_time_slept = max(time_slept.items(), key=key)
        # Find in which minute guard from above slept the most
        most_frequent_minute = max(frequency[max_time_slept[0]].items(), key=key)
        # Print final message
        message = f"Guard #{max_time_slept[0]} is most likely to be asleep in 00:{most_frequent_minute[0]}"
        print(message)
        return message


def main():
    planner_obj = HeistPlanner()
    planner_obj.read_log()
    planner_obj.run()


if __name__ == '__main__':
    main()
