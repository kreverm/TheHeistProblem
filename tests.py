import sys
import unittest
import constants
from main import HeistPlanner


class TestHeistPlanner(unittest.TestCase):
    def setUp(self):
        print(sys.argv[0])

    def test_good_path(self):
        """
        Good path test - valid file with valid path
        :return:
        """
        obj = HeistPlanner()
        obj.read_log()
        result = obj.run()
        assert result == "Guard #10 is most likely to be asleep in 00:24"

    def test_negative_log_path(self):
        """
        Negative test - wrong path given
        :return:
        """
        obj = HeistPlanner()
        obj.log_path = "C:\\asdasdasd\\asdasd"

        with self.assertRaises(FileNotFoundError):
            obj.read_log()

    def test_negative_file_contents(self):
        """
        Negative test - bad file content
        :return:
        """
        obj = HeistPlanner()
        obj.log_path = constants.CURRENT_DIR_PATH + "\\test_log_file"
        with self.assertRaises(AttributeError):
            obj.read_log()
            obj.run()


if __name__ == "__main__":
    unittest.main()
