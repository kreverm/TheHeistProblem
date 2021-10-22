import os

# Constants
CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = "shift_log.txt"
SHIFT_LOG_PATH = CURRENT_DIR_PATH + "\\" + FILE_NAME
MINUTE_PATTERN = r':(\d+)'
GUARD_PATTERN = r'#(\d+)'
