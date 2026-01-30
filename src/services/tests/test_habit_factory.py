import unittest

from src.services.habit_factory import HabitFactory


# --- Fake DatabaseInterface replacement ---
class FakeDB:
    def __init__(self):
        self.data = [
            (1, "code", "Coding", "2025-01-01", "01:00:00", "DONE"),
            (2, "read", "Reading", "2025-01-02", "01:00:00", "UPCOMING")
        ]

    def get_all_habits(self):
        return self.data

    def add_habit(self, habit):
        return ("success", 3)

    def update_habit(self, table, id, **kwargs):
        return ("success", None)

    def delete_habit(self, habit):
        return ("success", None)

    def get_habit(self, id):
        for h in self.data:
            if h[0] == id:
                return h
        return ("error", "not found")

    def get_habits_by_status(self, status):
        return [h for h in self.data if h[5] == status]

    def get_name_with_text(self, name):
        return [h for h in self.data if name.lower() in h[2].lower()]


class TestHabitFactory(unittest.TestCase):

    def setUp(self):
        self.factory = HabitFactory()
        # Replace real DB with fake one
        self.factory.db = FakeDB()

    def test_id_exists_true(self):
        self.assertTrue(self.factory.id_exists(1))

    def test_id_exists_false(self):
        self.assertFalse(self.factory.id_exists(99))

    def test_get_habits(self):
        habits = self.factory.get_habits()
        self.assertEqual(len(habits), 2)

    def test_get_habit_found(self):
        habit = self.factory.get_habit(1)
        self.assertEqual(habit[2], "Coding")

    def test_get_habits_by_status(self):
        result = self.factory.get_habits_by_status("DONE")
        self.assertEqual(len(result), 1)

    def test_get_name_with_text(self):
        result = self.factory.get_name_with_text("read")
        self.assertEqual(result[0][2], "Reading")


if __name__ == "__main__":
    unittest.main()
