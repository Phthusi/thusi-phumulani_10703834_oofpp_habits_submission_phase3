import unittest
from ..view.analytics_habit_view import HabitAnalytics

class TestAnalytics(unittest.TestCase):
    def test_longest_streak(self):
        analytics = HabitAnalytics()
        habits = [
            (1, None, "A", None, None, "DONE"),
            (2, None, "A", None, None, "DONE"),
            (3, None, "A", None, None, "MISSED"),
            (4, None, "A", None, None, "DONE"),
        ]
        self.assertEqual(analytics.longest_streak(habits), 2)

    def test_completion_rate(self):
        analytics = HabitAnalytics()
        habits = [
            (1,None,"A",None,None,"DONE"),
            (2,None,"A",None,None,"DONE"),
            (3,None,"A",None,None,"MISSED"),
        ]
        self.assertEqual(analytics.completion_rate(habits), "66.66666666666666%")

if __name__ == "__main__":
    unittest.main()
