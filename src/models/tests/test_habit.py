import unittest
from src.models.habit import Habit

class TestHabit(unittest.TestCase):

    def setUp(self):
        self.habit = Habit("Read", "2060-12-01, 10:00", "01:00:00", 1)

    def test_habit_creation(self):
        self.assertEqual(self.habit.get_name(), "Read")
        self.assertEqual(self.habit.get_duration(), "01:00:00")
        self.assertEqual(self.habit.get_status(), "UPCOMING")

    def test_set_name(self):
        self.habit.set_name("Study")
        self.assertEqual(self.habit.get_name(), "Study")

    def test_set_status(self):
        self.habit.set_status("DONE")
        self.assertEqual(self.habit.get_status(), "DONE")

    def test_stringify_datetime(self):
        result = self.habit.stringify_datetime("2060-01-01 10:30:45")
        self.assertEqual(result, "2060-01-01, 10:30")

    def test_next_day(self):
        h = Habit("Test","2060-01-01, 10:00","01:00:00")
        h.next_day()
        # next_day uses DateTimeHandler internally → just check day advanced
        self.assertIn("2060-01-02", str(h.get_start_datetime()))

    def test_weekday(self):
        h = Habit("Test","2060-01-01, 10:00","01:00:00")
        day = h.weekday()
        self.assertIsInstance(day, str)

    def test_habit_equality(self):
        h1 = Habit("Run","2060-01-01, 10:00","01:00:00",1)
        h2 = Habit("Run","2060-01-01, 10:00","01:00:00",1)
        self.assertEqual(h1, h2)

if __name__ == "__main__":
    unittest.main()
