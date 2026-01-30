import unittest
from src.models.status import HabitStatus

class TestHabitStatus(unittest.TestCase):

    def test_get_status_valid(self):
        self.assertEqual(HabitStatus.get_status("done"), HabitStatus.DONE)
        self.assertEqual(HabitStatus.get_status("MISSED"), HabitStatus.MISSED)

    def test_status_value(self):
        self.assertEqual(HabitStatus.DONE.value, "DONE")

if __name__ == "__main__":
    unittest.main()
