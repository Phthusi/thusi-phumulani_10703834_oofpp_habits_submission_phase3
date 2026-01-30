import unittest
from datetime import datetime, timedelta
from ..handle_time import DateTimeHandler

class TestDateTimeHandler(unittest.TestCase):

    def setUp(self):
        self.handler = DateTimeHandler()

    # ---- Start datetime tests ----

    def test_set_start_datetime_valid_future(self):
        future = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d, %H:%M")
        msg, success = self.handler.set_start_datetime(future)
        self.assertTrue(success)
        self.assertIn("SUCCESSFUL", msg)

    def test_set_start_datetime_past(self):
        past = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d, %H:%M")
        msg, success = self.handler.set_start_datetime(past)
        self.assertFalse(success)
        self.assertIn("UNSUCCESSFUL", msg)

    def test_set_start_datetime_invalid_format(self):
        msg, success = self.handler.set_start_datetime("2025/10/10")
        self.assertFalse(success)

    # ---- Duration tests ----

    def test_set_duration_valid(self):
        msg, success = self.handler.set_habit_session_duration("01:30:00")
        self.assertTrue(success)
        self.assertEqual(self.handler.get_duration(), "01:30:00")

    def test_set_duration_invalid(self):
        msg, success = self.handler.set_habit_session_duration("1 hour")
        self.assertFalse(success)

    # ---- Weekday test ----

    def test_get_weekday(self):
        future = "2099-12-31, 12:00"
        self.handler.set_start_datetime(future)
        weekday = self.handler.get_weekday()
        self.assertIn(weekday, ['mon','tue','wed','thurs','fri','sat','sun'])

    # ---- Status mapping tests ----

    def test_map_time_to_status_upcoming(self):
        future_dt = (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
        status = self.handler.map_time_to_status(future_dt, "01:00:00")
        self.assertEqual(status, "UPCOMING")

    def test_map_time_to_status_ongoing(self):
        start = (datetime.now() - timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
        status = self.handler.map_time_to_status(start, "01:00:00")
        self.assertEqual(status, "ONGOING")

    def test_map_time_to_status_missed(self):
        start = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
        status = self.handler.map_time_to_status(start, "00:10:00")
        self.assertEqual(status, "MISSED")


if __name__ == "__main__":
    unittest.main()
