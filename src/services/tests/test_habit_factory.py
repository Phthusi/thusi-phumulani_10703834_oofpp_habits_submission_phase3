import unittest
import os
from services.habit_factory import HabitFactory
from models.habit import Habit

class TestHabitFactory(unittest.TestCase):

    def setUp(self):
        # use test database
        self.factory = HabitFactory()
    
    def test_add_and_get_habit(self):
        habit = Habit(name="Test Habit", start_datetime="2023-12-01, 10:00", duration="01:00:00")
        success = self.factory.add_habit(habit)
        self.assertTrue(success)

        habits = self.factory.get_habits()
        names = [h[2] for h in habits]
        self.assertIn("Test Habit", names)

    def test_delete_habit(self):
        habit = Habit(name="Delete Habit",start_datetime="2023-12-01, 10:00", duration="01:00:00")
        self.factory.add_habit(habit)
        habits = self.factory.get_habits()
        hid = habits[-1][0]
        self.factory.delete_habit(habit)
        self.assertNotIn(hid, [h[0] for h in self.factory.get_habits()])

if __name__ == "__main__":
    unittest.main()
