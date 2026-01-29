import unittest
from ..handle_time import DateTimeHandler
from datetime import datetime, timedelta

class TestDateTimeHandler(unittest.TestCase):

    def test_set_valid_start_datetime(self):
        dt = DateTimeHandler()
        future = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d, %H:%M")
        msg, success = dt.set_start_datetime(future)
        self.assertTrue(success)

    def test_set_invalid_start_datetime(self):
        dt = DateTimeHandler()
        msg, success = dt.set_start_datetime("2020-01-01, 10:00")
        self.assertFalse(success)

    def test_duration_parsing(self):
        dt = DateTimeHandler()
        msg, success = dt.set_habit_session_duration("01:30:00")
        self.assertTrue(success)
        self.assertEqual(dt.get_duration(), "01:30:00")

    def test_status_mapping(self):
        dt = DateTimeHandler()
        start = datetime.now() - timedelta(hours=1)
        status = dt.map_time_to_status(
            start.strftime("%Y-%m-%d %H:%M:%S"),
            "02:00:00"
        )
        self.assertEqual(status, "ONGOING")

# if __name__ == "__main__":
#     unittest.main()
